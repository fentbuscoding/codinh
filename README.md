# Epic Button Speedrun Challenge

This is an interactive multi-user button clicking game built with Flask and Socket.IO where users can compete to click a button as fast as possible. All clicks are synchronized in real-time across all connected users and persist even when the server restarts!

## Setup and Running

1. Make sure you have Python installed on your computer.
2. Install required packages by running: `pip install -r requirements.txt`
3. Run the application: `python app.py`
4. Open your browser and go to: `http://localhost:5000`
5. Share with friends using your local network IP (displayed when starting the app)

## Features

### Progressive Button Experience
The button evolves as you click it, going through 5 distinct levels:
- **Level 1 (0-500 clicks)**: Simple button with minimal styling
- **Level 2 (500-1000 clicks)**: Enhanced button with better appearance
- **Level 3 (1000-1500 clicks)**: Exciting button with animations
- **Level 4 (1500-2000 clicks)**: Advanced button with special effects
- **Level 5 (2000+ clicks)**: Epic button with maximum visual effects

### Sound Effects System
- Different sounds for each button level
- Special milestone sounds when reaching click milestones
- Sound toggle button to mute/unmute all audio
- Background music at higher levels

### Achievements System
- Unlock achievements as you click and reach milestones
- Achievement notifications when you earn a new achievement
- View all available and locked achievements in the achievements panel
- Special secret achievement to discover

### Mobile Optimization
- Responsive design that works on all device sizes
- Touch-friendly buttons and controls
- Haptic feedback on mobile devices (vibration)
- Landscape and portrait orientation support

## Persistence

All data persists between server restarts:
- Button click count is saved to a file (`button_clicks.json`)
- Achievements are saved locally and on the server
- User statistics are tracked across sessions

## Network Access

To allow others on your network to access the application:
- Run the included `open_firewall.bat` as administrator (Windows only)
- Share your local IP address (shown in the terminal when starting the app)
- Have others connect to `http://YOUR_IP_ADDRESS:5000`

## How it Works

- The Flask app with Socket.IO serves the interactive button webpage
- Button clicks are synchronized in real-time across all connected users
- The server maintains the global counter state and saves it to a file
- Click count persists between server restarts
- Fun animations and confetti effects trigger when clicking the button
- Special milestone effects happen every 10 clicks
- Sound effects and music enhance the experience
- Achievements system rewards continued engagement
- Mobile-friendly design ensures it works on all devices

## Files

- `index.html`: The interactive button webpage with animations and Socket.IO client
- `app.py`: The Flask and Socket.IO server that manages real-time communication
- `requirements.txt`: List of Python packages needed for the application
- `open_firewall.bat`: Script to open the required firewall port on Windows
- `button_clicks.json`: Automatically created file that stores the persistent click count
- `achievements.json`: Stores global achievement data
- `stats.json`: Stores user statistics and session data
- `test_features.py`: Test script to verify functionality

## Testing

Run the test script to verify all features are working correctly:
```
python test_features.py --all
```

Or test specific features:
```
python test_features.py --socket --api
python test_features.py --clicks 50
```