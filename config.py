"""
Configuration settings for the Interactive Button Application
"""
import os
from datetime import timedelta

class Config:
    """Base configuration class"""
    
    # Flask Settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'interactive-button-secret-key-change-in-production'
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() in ['true', '1', 'yes']
    
    # Server Settings
    HOST = os.environ.get('HOST', '0.0.0.0')
    PORT = int(os.environ.get('PORT', 5000))
    
    # File Storage Settings
    DATA_DIR = os.environ.get('DATA_DIR', 'data')
    CLICK_DATA_FILE = os.path.join(DATA_DIR, "button_clicks.json")
    ACHIEVEMENTS_FILE = os.path.join(DATA_DIR, "achievements.json")
    STATS_FILE = os.path.join(DATA_DIR, "stats.json")
    BACKUP_DIR = os.path.join(DATA_DIR, "backups")
    
    # Performance Settings
    MAX_CONNECTIONS = int(os.environ.get('MAX_CONNECTIONS', 1000))
    RATE_LIMIT_PER_MINUTE = int(os.environ.get('RATE_LIMIT_PER_MINUTE', 600))  # 10 clicks per second max
    SESSION_TIMEOUT = timedelta(hours=int(os.environ.get('SESSION_TIMEOUT_HOURS', 24)))
    
    # Feature Flags
    ENABLE_ACHIEVEMENTS = os.environ.get('ENABLE_ACHIEVEMENTS', 'True').lower() in ['true', '1', 'yes']
    ENABLE_STATS = os.environ.get('ENABLE_STATS', 'True').lower() in ['true', '1', 'yes']
    ENABLE_BACKUPS = os.environ.get('ENABLE_BACKUPS', 'True').lower() in ['true', '1', 'yes']
    
    # Backup Settings
    BACKUP_INTERVAL_HOURS = int(os.environ.get('BACKUP_INTERVAL_HOURS', 24))
    MAX_BACKUPS = int(os.environ.get('MAX_BACKUPS', 7))
    
    # Logging Settings
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = os.path.join(DATA_DIR, 'app.log')
    
    # CORS Settings
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*')
    
    @classmethod
    def ensure_directories(cls):
        """Ensure all required directories exist"""
        directories = [cls.DATA_DIR, cls.BACKUP_DIR]
        for directory in directories:
            os.makedirs(directory, exist_ok=True)

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-must-set-a-secret-key-in-production'
    
    # More restrictive settings for production
    RATE_LIMIT_PER_MINUTE = 300  # 5 clicks per second max
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', 'http://localhost:5000')

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True
    CLICK_DATA_FILE = "test_button_clicks.json"
    ACHIEVEMENTS_FILE = "test_achievements.json"
    STATS_FILE = "test_stats.json"

# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
