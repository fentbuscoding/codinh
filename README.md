# Epic Button Speedrun Challenge

This is an interactive multi-user button clicking game built with Flask and Socket.IO where users can compete to click a button as fast as possible. All clicks are synchronized in real-time across all connected users!

## Setup and Running

1. Make sure you have Python installed on your computer.
2. Install required packages by running: `pip install -r requirements.txt`
3. Run the application: `python app.py`
4. Open your browser and go to: `http://localhost:5000`
5. Share with friends using your local network IP (displayed when starting the app)

## Network Access

To allow others on your network to access the application:
- Run the included `open_firewall.bat` as administrator (Windows only)
- Share your local IP address (shown in the terminal when starting the app)
- Have others connect to `http://YOUR_IP_ADDRESS:5000`

## How it Works

- The Flask app with Socket.IO serves the interactive button webpage
- Button clicks are synchronized in real-time across all connected users
- The server maintains the global counter state
- Fun animations and confetti effects trigger when clicking the button
- Special milestone effects happen every 10 clicks

## Files

- `index.html`: The interactive button webpage with animations and Socket.IO client
- `app.py`: The Flask and Socket.IO server that manages real-time communication
- `requirements.txt`: List of Python packages needed for the application
- `open_firewall.bat`: Script to open the required firewall port on Windows