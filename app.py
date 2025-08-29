from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO, emit
import os
import socket

app = Flask(__name__)
app.config['SECRET_KEY'] = 'interactive-button-secret'
socketio = SocketIO(app, cors_allowed_origins="*")

# Current button state - stored on server
button_state = {"count": 0}

# Serve the index.html file at the root URL
@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

# Route to serve static files if needed
@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

# Socket.IO event for when a client connects
@socketio.on('connect')
def handle_connect():
    # Send current state to the newly connected client
    emit('update_state', button_state)
    print(f"Client connected. Current count: {button_state['count']}")

# Socket.IO event for button clicks
@socketio.on('button_click')
def handle_button_click():
    # Update the count
    button_state['count'] += 1
    # Broadcast the new state to all connected clients
    emit('update_state', button_state, broadcast=True)
    print(f"Button clicked. New count: {button_state['count']}")

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
    
    # Run the Socket.IO app
    socketio.run(app, host='0.0.0.0', port=port, debug=True, allow_unsafe_werkzeug=True)