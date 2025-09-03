# Interactive Button Speedrun Challenge - Enhanced v2.0

🎮 **[Play the GitHub Pages version instantly!](https://fentbuscoding.github.io/codinh/)** - No setup required!

This project includes two versions:
- **GitHub Pages Edition**: Static version that works in any browser without a server
- **Enhanced Server Edition**: Full-featured Flask-SocketIO version with real-time multiplayer

## 🌐 GitHub Pages Edition (Recommended for Quick Play)

The GitHub Pages version is a complete standalone implementation that includes:
- ✅ All 10 achievements
- ✅ 5 progressive levels with visual/audio effects  
- ✅ Real-time statistics and session tracking
- ✅ Persistent progress (localStorage)
- ✅ Mobile-friendly responsive design
- ✅ Sound effects and confetti animations
- ✅ No installation required

**🚀 [Play Now on GitHub Pages](https://fentbuscoding.github.io/codinh/)**

## 🖥️ Enhanced Server Edition (v2.0)

This is a significantly improved multi-user button clicking game built with Flask and Socket.IO. The enhanced version includes better architecture, error handling, performance optimizations, security features, and comprehensive logging.

## 🚀 What's New in v2.0

### Architecture Improvements
- **Modular Design**: Code split into logical modules (`config.py`, `data_manager.py`, `rate_limiter.py`)
- **Configuration Management**: Environment-based configuration with `.env` file support
- **Application Factory**: Proper Flask application factory pattern
- **Thread Safety**: All file operations are thread-safe with proper locking

### Performance Enhancements
- **Rate Limiting**: Prevents spam clicking with configurable limits (600 clicks/minute default)
- **Connection Limiting**: Limits concurrent connections to prevent server overload
- **Atomic File Operations**: Ensures data integrity during saves
- **Background Cleanup**: Automatic cleanup of old data and rate limiting entries
- **Memory Optimization**: Efficient data structures and cleanup routines

### Security Features
- **Input Validation**: All user inputs are properly validated
- **CORS Configuration**: Configurable CORS settings for security
- **Error Handling**: Comprehensive error handling with proper logging
- **Session Management**: Improved client session tracking

### Data Management
- **Automatic Backups**: Regular backups of all data files
- **Data Recovery**: Automatic recovery from corrupted data files
- **Versioned Data**: Data format versioning for future compatibility
- **Organized Storage**: All data stored in a dedicated `data/` directory

### Monitoring & Logging
- **Structured Logging**: Proper logging with different levels and file output
- **Health Check Endpoint**: `/api/health` for monitoring server status
- **Performance Metrics**: Track connections, response times, and system health
- **Debug Information**: Comprehensive debug output for troubleshooting

## Setup and Installation

### Prerequisites
- Python 3.8+ installed
- Internet connection for downloading dependencies

### Installation Steps

1. **Clone or download the project**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Optional: Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env file to customize settings
   ```

4. **Run the application:**
   ```bash
   python app.py
   ```

5. **Access the application:**
   - Local: `http://localhost:5000`
   - Network: `http://YOUR_IP_ADDRESS:5000` (shown in terminal)

### Configuration Options

Create a `.env` file to customize the application:

```env
# Server Settings
FLASK_ENV=development
PORT=5000
HOST=0.0.0.0

# Performance Settings
MAX_CONNECTIONS=1000
RATE_LIMIT_PER_MINUTE=600

# Feature Flags
ENABLE_ACHIEVEMENTS=True
ENABLE_STATS=True
ENABLE_BACKUPS=True

# Logging
LOG_LEVEL=INFO

# Security
SECRET_KEY=your-secret-key
CORS_ORIGINS=*
```

## Features

### Progressive Button Experience
The button evolves through 5 distinct levels as you click:
- **Level 1 (0-500 clicks)**: Simple button with minimal styling
- **Level 2 (500-1000 clicks)**: Enhanced appearance and animations
- **Level 3 (1000-1500 clicks)**: Exciting effects with background music
- **Level 4 (1500-2000 clicks)**: Advanced visual effects and haptic feedback
- **Level 5 (2000+ clicks)**: Epic button with maximum visual chaos

### Real-time Multiplayer
- **Synchronized Clicks**: All clicks are synchronized across all connected users
- **Live Updates**: See other players' clicks in real-time
- **Session Tracking**: Advanced user session management
- **Connection Status**: Real-time connection status indicators

### Achievement System
- **Progressive Achievements**: Unlock achievements as you reach milestones
- **Global Tracking**: Achievements are tracked globally and per-user
- **Visual Notifications**: Beautiful achievement unlock animations
- **Secret Achievements**: Hidden achievements to discover (hint: try the Konami code!)

### Statistics & Analytics
- **Click Tracking**: Detailed statistics on clicks per hour, day, and user
- **User Analytics**: Track unique users and session data
- **Performance Metrics**: Monitor server performance and response times
- **Data Export**: All statistics available via REST API

### Mobile Optimization
- **Responsive Design**: Works perfectly on all device sizes
- **Touch Support**: Optimized touch controls for mobile devices
- **Haptic Feedback**: Vibration feedback on supported mobile devices
- **Offline Capability**: Limited offline functionality with local storage

### Sound & Visual Effects
- **Dynamic Sound System**: Different sounds for each button level
- **Visual Effects**: Confetti, animations, and particle effects
- **Progressive Enhancement**: Effects become more elaborate as you progress
- **Sound Toggle**: Easy mute/unmute functionality

## API Endpoints

The enhanced version includes a REST API for monitoring and integration:

### Health Check
```
GET /api/health
```
Returns server status, version, uptime, and connection count.

### Statistics
```
GET /api/stats
```
Returns detailed click statistics, user data, and hourly breakdown.

### Achievements
```
GET /api/achievements
```
Returns all unlocked achievements and player progress.

## File Structure

```
├── app.py                 # Main application with enhanced architecture
├── config.py              # Configuration management
├── data_manager.py        # Data persistence and backup handling
├── rate_limiter.py        # Rate limiting and connection management
├── index.html             # Interactive frontend with all features
├── requirements.txt       # Python dependencies
├── .env.example          # Environment configuration template
├── test_enhanced.py       # Comprehensive test suite
├── data/                  # Data storage directory
│   ├── button_clicks.json # Persistent click data
│   ├── achievements.json  # Achievement data
│   ├── stats.json         # Statistics and user data
│   ├── app.log           # Application logs
│   └── backups/          # Automatic backup storage
└── README.md             # This file
```

## Data Persistence & Backup

All data is automatically saved and backed up:

- **Atomic Saves**: Data is saved atomically to prevent corruption
- **Automatic Backups**: Daily backups of all data files
- **Backup Rotation**: Keeps last 7 backups by default
- **Corruption Recovery**: Automatic recovery from corrupted files
- **Cross-Platform**: Works on Windows, Linux, and macOS

## Performance & Scalability

The enhanced version is optimized for performance:

- **Rate Limiting**: Prevents abuse and ensures fair usage
- **Connection Management**: Handles up to 1000 concurrent connections
- **Memory Efficient**: Optimized data structures and cleanup routines
- **Background Processing**: Non-blocking background tasks
- **Caching**: Intelligent caching of frequently accessed data

## Security Features

- **Input Validation**: All user inputs are validated and sanitized
- **Rate Limiting**: Protects against spam and abuse
- **Session Security**: Secure session management
- **CORS Protection**: Configurable CORS settings
- **Error Handling**: Secure error handling without information disclosure

## Testing

Run the comprehensive test suite:

```bash
# Run all tests
python test.py

# Run quick tests (without server dependency)
python test.py --quick
```

## Monitoring & Maintenance

### Logs
Application logs are stored in `data/app.log` with configurable log levels.

### Health Monitoring
Use the `/api/health` endpoint to monitor server status in production.

### Backup Management
Backups are automatically created and rotated. Manual backups can be triggered through the API.

## Troubleshooting

### Common Issues

1. **Port Already in Use**: Change the PORT in `.env` file
2. **Permission Errors**: Ensure write permissions for the `data/` directory
3. **Rate Limited**: Wait or adjust `RATE_LIMIT_PER_MINUTE` in configuration
4. **Connection Issues**: Check firewall settings and network configuration

### Debug Mode

Enable debug mode for development:
```env
FLASK_ENV=development
DEBUG=True
LOG_LEVEL=DEBUG
```

## Contributing

This enhanced version provides a solid foundation for further improvements:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run the test suite
5. Submit a pull request

## License

This project is open source and available under the MIT License.
