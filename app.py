from flask import Flask, render_template, send_from_directory, jsonify, request
from flask_socketio import SocketIO, emit
import os
import socket
import json
import time
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = 'interactive-button-secret'
socketio = SocketIO(app, cors_allowed_origins="*")

# Files for data storage
CLICK_DATA_FILE = "button_clicks.json"
ACHIEVEMENTS_FILE = "achievements.json"
STATS_FILE = "stats.json"

# Function to load click count and other state from file
def load_button_state():
    try:
        if os.path.exists(CLICK_DATA_FILE):
            with open(CLICK_DATA_FILE, 'r') as f:
                data = json.load(f)
                return data
    except Exception as e:
        print(f"Error loading button state: {e}")
    
    # Default state if file doesn't exist or there's an error
    return {
        "count": 0,
        "last_updated": time.time()
    }

# Function to save full button state to file
def save_button_state(state):
    try:
        # Always update the timestamp
        state["last_updated"] = time.time()
        
        with open(CLICK_DATA_FILE, 'w') as f:
            json.dump(state, f)
    except Exception as e:
        print(f"Error saving button state: {e}")

# Function to load global achievements
def load_achievements():
    try:
        if os.path.exists(ACHIEVEMENTS_FILE):
            with open(ACHIEVEMENTS_FILE, 'r') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading achievements: {e}")
    
    # Default empty achievements if file doesn't exist
    return {
        "global_unlocked": [],
        "player_achievements": {}
    }

# Function to save global achievements
def save_achievements(achievements_data):
    try:
        with open(ACHIEVEMENTS_FILE, 'w') as f:
            json.dump(achievements_data, f)
    except Exception as e:
        print(f"Error saving achievements: {e}")

# Function to load stats data
def load_stats():
    try:
        if os.path.exists(STATS_FILE):
            with open(STATS_FILE, 'r') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading stats: {e}")
    
    # Default stats data
    return {
        "clicks_today": 0,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "clicks_per_hour": [0] * 24,
        "unique_users": 0,
        "user_sessions": {}
    }

# Function to save stats data
def save_stats(stats_data):
    try:
        # Check if it's a new day and reset daily stats if needed
        today = datetime.now().strftime("%Y-%m-%d")
        if stats_data.get("date") != today:
            stats_data["clicks_today"] = 0
            stats_data["date"] = today
            stats_data["clicks_per_hour"] = [0] * 24
        
        with open(STATS_FILE, 'w') as f:
            json.dump(stats_data, f)
    except Exception as e:
        print(f"Error saving stats: {e}")

# Initialize state from files
button_state = load_button_state()
achievements_data = load_achievements()
stats_data = load_stats()

# Serve the index.html file at the root URL
@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

# Route to serve static files if needed
@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

# API endpoint for stats
@app.route('/api/stats')
def get_stats():
    # Update stats before returning
    current_hour = datetime.now().hour
    stats_data["clicks_per_hour"][current_hour] = button_state["count"]
    return jsonify(stats_data)

# API endpoint for achievements
@app.route('/api/achievements')
def get_achievements():
    return jsonify(achievements_data)

# Socket.IO event for when a client connects
@socketio.on('connect')
def handle_connect():
    # Send current state to the newly connected client
    emit('update_state', button_state)
    
    # Generate session ID for client tracking that doesn't rely on request.sid
    client_id = f"client_{time.time()}_{len(stats_data['user_sessions'])}"
    emit('set_client_id', {'client_id': client_id})
    
    # Update user stats
    stats_data["unique_users"] += 1
    stats_data["user_sessions"][client_id] = {
        "first_connected": time.time(),
        "clicks": 0
    }
    
    save_stats(stats_data)
    print(f"Client connected. Current count: {button_state['count']}")

# Socket.IO event for when a client disconnects
@socketio.on('disconnect')
def handle_disconnect():
    # We no longer use request.sid, but instead track client_id events
    # Clients will report their client_id when they reconnect
    print(f"Client disconnected.")

# Socket.IO event for button clicks
@socketio.on('button_click')
def handle_button_click(data=None):
    # Update the count
    button_state['count'] += 1
    
    # Get client_id from data if provided
    client_id = None
    if data and isinstance(data, dict):
        client_id = data.get('client_id')
    
    # Update user stats if we have a client_id
    if client_id and client_id in stats_data["user_sessions"]:
        stats_data["user_sessions"][client_id]["clicks"] = stats_data["user_sessions"][client_id].get("clicks", 0) + 1
        stats_data["user_sessions"][client_id]["last_click"] = time.time()
    
    # Update daily stats
    stats_data["clicks_today"] += 1
    current_hour = datetime.now().hour
    stats_data["clicks_per_hour"][current_hour] += 1
    
    # Save to files for persistence
    save_button_state(button_state)
    save_stats(stats_data)
    
    # Broadcast the new state to all connected clients
    emit('update_state', button_state, broadcast=True)
    print(f"Button clicked. New count: {button_state['count']} (saved to file)")

# Socket.IO event for achievement updates
@socketio.on('achievement_unlocked')
def handle_achievement_unlock(data):
    # Data should contain user ID and achievement ID
    user_id = data.get('user_id')
    achievement_id = data.get('achievement_id')
    
    if not user_id or not achievement_id:
        return
    
    # Add to player's achievements if not already there
    if user_id not in achievements_data["player_achievements"]:
        achievements_data["player_achievements"][user_id] = []
    
    if achievement_id not in achievements_data["player_achievements"][user_id]:
        achievements_data["player_achievements"][user_id].append(achievement_id)
    
    # Add to global achievements if not already there
    if achievement_id not in achievements_data["global_unlocked"]:
        achievements_data["global_unlocked"].append(achievement_id)
        # Broadcast new achievement to all clients
        emit('new_global_achievement', {'id': achievement_id}, broadcast=True)
    
    save_achievements(achievements_data)
    print(f"Achievement {achievement_id} unlocked by user {user_id}")

# Get the local IP address
def get_local_ip():
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

if __name__ == '__main__':
    # Get the local IP address
    ip_address = get_local_ip()
    port = 5000
    
    # Print access instructions
    print(f"\n===== Access Information =====")
    print(f"Local access: http://127.0.0.1:{port}")
    print(f"Network access: http://{ip_address}:{port}")
    print(f"Make sure your firewall allows connections to port {port}")
    print(f"==============================\n")
    
    # Print app state information
    print(f"Current click count: {button_state['count']}")
    print(f"Last updated: {datetime.fromtimestamp(button_state.get('last_updated', 0)).strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Unique users recorded: {stats_data.get('unique_users', 0)}")
    print(f"Global achievements unlocked: {len(achievements_data.get('global_unlocked', []))}")
    print(f"\n==============================\n")
    
    # Run the Socket.IO app
    socketio.run(app, host='0.0.0.0', port=port, debug=True, allow_unsafe_werkzeug=True)