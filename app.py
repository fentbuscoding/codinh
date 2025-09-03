"""
Interactive Button Speedrun Challenge - Enhanced Version 2.0

A multi-user real-time button clicking game built with Flask and Socket.IO
with improved architecture, error handling, and performance optimizations.
"""

from flask import Flask, send_from_directory, jsonify, request as flask_request
from flask_socketio import SocketIO, emit
import os
import socket
import time
import logging
import threading
from datetime import datetime
from typing import Dict, Any, Optional

# Import our custom modules
from config import config
from data_manager import DataManager
from rate_limiter import RateLimiter, ConnectionLimiter

# Configure logging
def setup_logging(config_obj):
    """Setup application logging with proper formatting and handlers"""
    log_level = getattr(logging, config_obj.LOG_LEVEL.upper(), logging.INFO)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Setup root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # File handler (if configured)
    if hasattr(config_obj, 'LOG_FILE') and config_obj.LOG_FILE:
        try:
            file_handler = logging.FileHandler(config_obj.LOG_FILE)
            file_handler.setFormatter(formatter)
            root_logger.addHandler(file_handler)
        except Exception as e:
            logging.error(f"Could not setup file logging: {e}")

# Global variables for the enhanced app
app = None
socketio = None
data_manager = None
rate_limiter = None
connection_limiter = None
button_state = {}
achievements_data = {}
stats_data = {}
logger = None
app_config = None

def initialize_app(config_name: Optional[str] = None):
    """Initialize the Flask application and all components"""
    global app, socketio, data_manager, rate_limiter, connection_limiter
    global button_state, achievements_data, stats_data, logger, app_config
    
    # Determine config
    config_name = config_name or os.environ.get('FLASK_ENV', 'default')
    app_config = config[config_name]
    
    # Setup logging
    setup_logging(app_config)
    logger = logging.getLogger(__name__)
    
    # Create Flask app
    app = Flask(__name__)
    app.config.from_object(app_config)
    
    # Initialize SocketIO with proper configuration
    socketio = SocketIO(
        app, 
        cors_allowed_origins=app_config.CORS_ORIGINS,
        ping_timeout=60,
        ping_interval=25,
        max_http_buffer_size=1024*1024  # 1MB limit
    )
    
    # Initialize components
    data_manager = DataManager(app_config)
    rate_limiter = RateLimiter(app_config.RATE_LIMIT_PER_MINUTE)
    connection_limiter = ConnectionLimiter(app_config.MAX_CONNECTIONS)
    
    # Initialize state from files
    button_state = data_manager.load_button_state()
    achievements_data = data_manager.load_achievements() if app_config.ENABLE_ACHIEVEMENTS else {}
    stats_data = data_manager.load_stats() if app_config.ENABLE_STATS else {}
    
    logger.info(f"Application started with {config_name} configuration")
    logger.info(f"Initial button count: {button_state.get('count', 0)}")
    
    # Background cleanup task
    def cleanup_task():
        """Periodic cleanup task"""
        while True:
            try:
                time.sleep(300)  # Run every 5 minutes
                rate_limiter.cleanup_old_entries()
                
                # Create backup if enabled
                if app_config.ENABLE_BACKUPS:
                    data_manager.create_backup()
                    
            except Exception as e:
                logger.error(f"Error in cleanup task: {e}")
    
    # Start background cleanup thread
    cleanup_thread = threading.Thread(target=cleanup_task, daemon=True)
    cleanup_thread.start()

# Initialize the app
initialize_app()

# Routes
@app.route('/')
def home():
    """Serve the main HTML page"""
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    """Serve static files"""
    return send_from_directory('.', path)

@app.route('/api/stats')
def get_stats():
    """API endpoint for statistics data"""
    if not app_config.ENABLE_STATS:
        return jsonify({"error": "Stats disabled"}), 404
        
    # Update stats before returning
    current_hour = datetime.now().hour
    if "clicks_per_hour" in stats_data and current_hour < len(stats_data["clicks_per_hour"]):
        stats_data["clicks_per_hour"][current_hour] = button_state.get("count", 0)
    return jsonify(stats_data)

@app.route('/api/achievements')
def get_achievements():
    """API endpoint for achievements data"""
    if not app_config.ENABLE_ACHIEVEMENTS:
        return jsonify({"error": "Achievements disabled"}), 404
    return jsonify(achievements_data)

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "version": "2.0",
        "uptime": time.time() - button_state.get("last_updated", time.time()),
        "connections": connection_limiter.get_connection_count(),
        "button_count": button_state.get("count", 0)
    })

# Socket.IO event handlers
@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    from flask import session
    import uuid
    
    # Generate a unique client ID
    if 'client_id' not in session:
        session['client_id'] = str(uuid.uuid4())
    client_id = session['client_id']
    
    # Check connection limit
    if not connection_limiter.can_connect(client_id):
        logger.warning(f"Connection rejected due to limits: {client_id}")
        return False
        
    connection_limiter.add_connection(client_id)
    
    # Send current state to the newly connected client
    emit('update_state', button_state)
    
    # Generate session ID for client tracking
    session_client_id = f"client_{time.time()}_{len(stats_data.get('user_sessions', {}))}"
    emit('set_client_id', {'client_id': session_client_id})
    
    # Update user stats if enabled
    if app_config.ENABLE_STATS:
        stats_data["unique_users"] = stats_data.get("unique_users", 0) + 1
        if "user_sessions" not in stats_data:
            stats_data["user_sessions"] = {}
        stats_data["user_sessions"][session_client_id] = {
            "first_connected": time.time(),
            "clicks": 0,
            "socket_id": client_id
        }
        data_manager.save_stats(stats_data)
    
    logger.info(f"Client connected: {client_id}. Current count: {button_state.get('count', 0)}")

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    from flask import session
    client_id = session.get('client_id', 'unknown')
    connection_limiter.remove_connection(client_id)
    logger.info(f"Client disconnected: {client_id}")

@socketio.on('button_click')
def handle_button_click(data=None):
    """Handle button click events with rate limiting"""
    from flask import session
    import uuid
    
    # Get or create client ID
    if 'client_id' not in session:
        session['client_id'] = str(uuid.uuid4())
    client_id = session['client_id']
    
    # Rate limiting check
    if not rate_limiter.is_allowed(client_id):
        emit('rate_limited', {
            'message': 'Clicking too fast! Please slow down.',
            'remaining': rate_limiter.get_remaining_requests(client_id)
        })
        return
    
    # Update the count
    button_state['count'] = button_state.get('count', 0) + 1
    
    # Get session client_id from data if provided
    session_client_id = None
    if data and isinstance(data, dict):
        session_client_id = data.get('client_id')
    
    # Update user stats if enabled and we have a session client_id
    if app_config.ENABLE_STATS and session_client_id and session_client_id in stats_data.get("user_sessions", {}):
        user_session = stats_data["user_sessions"][session_client_id]
        user_session["clicks"] = user_session.get("clicks", 0) + 1
        user_session["last_click"] = time.time()
        
        # Update daily stats
        stats_data["clicks_today"] = stats_data.get("clicks_today", 0) + 1
        current_hour = datetime.now().hour
        if "clicks_per_hour" not in stats_data:
            stats_data["clicks_per_hour"] = [0] * 24
        if current_hour < len(stats_data["clicks_per_hour"]):
            stats_data["clicks_per_hour"][current_hour] += 1
        
        data_manager.save_stats(stats_data)
    
    # Save button state to file for persistence
    success = data_manager.save_button_state(button_state)
    if not success:
        logger.error("Failed to save button state")
    
    # Broadcast the new state to all connected clients
    emit('update_state', button_state, broadcast=True)
    logger.debug(f"Button clicked by {client_id}. New count: {button_state.get('count', 0)}")

@socketio.on('achievement_unlocked')
def handle_achievement_unlock(data):
    """Handle achievement unlock events"""
    if not app_config.ENABLE_ACHIEVEMENTS:
        return
        
    user_id = data.get('user_id')
    achievement_id = data.get('achievement_id')
    
    if not user_id or not achievement_id:
        logger.warning(f"Invalid achievement unlock data: {data}")
        return
    
    # Add to player's achievements if not already there
    if "player_achievements" not in achievements_data:
        achievements_data["player_achievements"] = {}
        
    if user_id not in achievements_data["player_achievements"]:
        achievements_data["player_achievements"][user_id] = []
    
    if achievement_id not in achievements_data["player_achievements"][user_id]:
        achievements_data["player_achievements"][user_id].append(achievement_id)
    
    # Add to global achievements if not already there
    if "global_unlocked" not in achievements_data:
        achievements_data["global_unlocked"] = []
        
    if achievement_id not in achievements_data["global_unlocked"]:
        achievements_data["global_unlocked"].append(achievement_id)
        # Broadcast new achievement to all clients
        emit('new_global_achievement', {'id': achievement_id}, broadcast=True)
    
    success = data_manager.save_achievements(achievements_data)
    if success:
        logger.info(f"Achievement {achievement_id} unlocked by user {user_id}")
    else:
        logger.error(f"Failed to save achievement unlock: {achievement_id}")

def get_local_ip():
    """Get the local IP address for network access"""
    try:
        # Create a socket connection to an external server
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Doesn't need to be reachable
        s.connect(('8.8.8.8', 1))
        IP = s.getsockname()[0]
        s.close()
        return IP
    except Exception:
        return '127.0.0.1'

def print_startup_info():
    """Print startup information and instructions"""
    # Get the local IP address
    ip_address = get_local_ip()
    port = app_config.PORT
    
    # Print access information
    print(f"\n===== Interactive Button Challenge v2.0 =====")
    print(f"Local access: http://127.0.0.1:{port}")
    print(f"Network access: http://{ip_address}:{port}")
    print(f"Make sure your firewall allows connections to port {port}")
    print(f"Environment: {os.environ.get('FLASK_ENV', 'development')}")
    print(f"Debug mode: {app_config.DEBUG}")
    print(f"=============================================\n")
    
    # Print app state information
    print(f"Current click count: {button_state.get('count', 0)}")
    print(f"Last updated: {datetime.fromtimestamp(button_state.get('last_updated', 0)).strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Unique users recorded: {stats_data.get('unique_users', 0)}")
    print(f"Global achievements unlocked: {len(achievements_data.get('global_unlocked', []))}")
    print(f"Data directory: {app_config.DATA_DIR}")
    print(f"\n===========================================\n")

if __name__ == '__main__':
    # Print startup information
    print_startup_info()
    
    # Run the SocketIO app
    socketio.run(
        app, 
        host=app_config.HOST, 
        port=app_config.PORT, 
        debug=app_config.DEBUG, 
        allow_unsafe_werkzeug=True
    )