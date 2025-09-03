# Button Clicker - GitHub Pages Edition

🚀 **Live Demo**: [Play Now on GitHub Pages](https://fentbuscoding.github.io/codinh/)

A fun, interactive button clicking game that works entirely in your browser! This is the GitHub Pages compatible version of the original Flask-SocketIO application.

## 🎮 Features

- **Single Player Mode**: All functionality runs client-side using localStorage
- **5 Progressive Levels**: Visual and audio effects that get more exciting as you click
- **Achievement System**: 10 different achievements to unlock
- **Real-time Statistics**: Session tracking, clicks per minute, streaks
- **Sound Effects**: Different audio feedback for each level
- **Responsive Design**: Works on desktop and mobile devices
- **Visual Effects**: Confetti celebrations and level-up animations
- **Persistent Progress**: Your progress is saved locally in your browser

## 🎯 Achievements

- 👆 **First Click**: Click the button for the first time
- 🔥 **Getting Started**: Click 10 times
- 🚀 **Halfway There**: Click 50 times
- 🌟 **Century**: Click 100 times
- ⬆️ **Level Up**: Reach Level 2 (500 clicks)
- 💥 **Button Master**: Reach Level 3 (1000 clicks)
- 🥇 **Button Pro**: Reach Level 4 (1500 clicks)
- 👑 **Button God**: Reach Level 5 (2000 clicks)
- ⚡ **Speed Clicker**: Click 5 times in 3 seconds
- 🏠 **Persistent**: Keep clicking even on GitHub Pages! (25 clicks)

## 🚀 GitHub Pages Deployment

This version is specifically designed to work with GitHub Pages static hosting:

### Quick Setup

1. **Fork this repository**
2. **Enable GitHub Pages**: Go to Settings → Pages → Source: Deploy from a branch → Branch: main → Folder: /github-pages
3. **Access your site**: `https://yourusername.github.io/codinh/`

### Manual Deployment Steps

1. **Create a new GitHub repository**
2. **Upload the `github-pages/index.html` file to your repository**
3. **Enable GitHub Pages** in repository settings
4. **Your game is now live!**

## 📁 Files

- `github-pages/index.html` - Complete standalone game (no server required)
- `app.py` - Original Flask-SocketIO server version
- `requirements.txt` - Python dependencies for server version

## 🔧 Technical Details

### GitHub Pages Version
- **Technology**: Pure HTML, CSS, JavaScript
- **Storage**: Browser localStorage
- **Audio**: Howler.js + online sound effects
- **Effects**: Canvas Confetti
- **No server required**: Fully client-side

### Original Server Version
- **Technology**: Python Flask + SocketIO
- **Features**: Real-time multiplayer, server-side data persistence
- **Database**: JSON files with atomic operations
- **Advanced**: Rate limiting, connection management, backups

## 🎨 Level Progression

1. **Level 1** (0-499 clicks): Basic button
2. **Level 2** (500-999 clicks): Styled with gradients
3. **Level 3** (1000-1499 clicks): Colorful with shadows
4. **Level 4** (1500-1999 clicks): Fancy animations
5. **Level 5** (2000+ clicks): Epic rainbow madness!

## 📱 Mobile Support

The GitHub Pages version is fully responsive and includes:
- Touch-friendly button sizing (minimum 44px)
- Optimized layout for small screens
- Mobile-friendly achievement notifications
- Responsive statistics panel

## 🔊 Audio Features

- Different sound effects for each level
- Achievement unlock sounds
- Level-up fanfares
- Toggle sound on/off

## 💾 Data Persistence

Your progress is automatically saved to browser localStorage:
- Button click count
- Unlocked achievements
- Session statistics
- Sound preferences

## 🎯 Keyboard Controls

- **Spacebar**: Click the button
- Works alongside mouse/touch input

## 🐛 Browser Compatibility

- ✅ Chrome/Chromium
- ✅ Firefox
- ✅ Safari
- ✅ Edge
- ✅ Mobile browsers

## 🔄 Differences from Server Version

| Feature | Server Version | GitHub Pages Version |
|---------|---------------|---------------------|
| Multiplayer | ✅ Real-time | ❌ Single player only |
| Data Storage | Server files | Browser localStorage |
| Deployment | Requires Python server | Static files only |
| Setup Complexity | Medium | Very Easy |
| Offline Support | ❌ | ✅ After first load |

## 🎮 How to Play

1. Click the button to increase your count
2. Unlock achievements as you progress
3. Watch the game transform through 5 different levels
4. Try to become a Button God (2000+ clicks)!
5. Use spacebar for rapid clicking

## 🌟 Tips for High Scores

- Use the spacebar for faster clicking
- Try to maintain clicking streaks
- Aim for the "Speed Clicker" achievement early
- The visual effects get more exciting at higher levels!

## 📊 Statistics Tracking

- **Session Time**: How long you've been playing
- **Clicks/Min**: Your current clicking rate
- **Best Streak**: Longest consecutive clicking streak
- **Total Achievements**: Progress tracking
- **Current Level**: Visual progression indicator

---

**Made with ❤️ for GitHub Pages**

Enjoy the game! 🎮
