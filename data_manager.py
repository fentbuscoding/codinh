"""
Data management utilities for the Interactive Button Application
"""
import json
import os
import time
import logging
import shutil
from datetime import datetime
from typing import Dict, Any, Optional
from threading import Lock

logger = logging.getLogger(__name__)

class DataManager:
    """Handles all data persistence operations with thread safety and error handling"""
    
    def __init__(self, config):
        self.config = config
        self._file_locks = {
            'clicks': Lock(),
            'achievements': Lock(),
            'stats': Lock()
        }
        
        # Ensure data directories exist
        config.ensure_directories()
    
    def _safe_file_operation(self, operation_name: str, file_path: str, operation_func, default_data: Any = None):
        """
        Safely perform file operations with proper error handling and logging
        """
        try:
            return operation_func()
        except FileNotFoundError:
            logger.info(f"{operation_name}: File {file_path} not found, using default data")
            return default_data
        except json.JSONDecodeError as e:
            logger.error(f"{operation_name}: JSON decode error in {file_path}: {e}")
            # Create backup of corrupted file
            self._backup_corrupted_file(file_path)
            return default_data
        except PermissionError as e:
            logger.error(f"{operation_name}: Permission error accessing {file_path}: {e}")
            raise
        except Exception as e:
            logger.error(f"{operation_name}: Unexpected error with {file_path}: {e}")
            return default_data
    
    def _backup_corrupted_file(self, file_path: str):
        """Create a backup of corrupted file for debugging"""
        if os.path.exists(file_path):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = f"{file_path}.corrupted.{timestamp}"
            try:
                shutil.copy2(file_path, backup_path)
                logger.info(f"Corrupted file backed up to: {backup_path}")
            except Exception as e:
                logger.error(f"Failed to backup corrupted file: {e}")
    
    def load_button_state(self) -> Dict[str, Any]:
        """Load button state from file with thread safety"""
        with self._file_locks['clicks']:
            def load_operation():
                with open(self.config.CLICK_DATA_FILE, 'r') as f:
                    data = json.load(f)
                    # Validate data structure
                    if not isinstance(data, dict) or 'count' not in data:
                        raise ValueError("Invalid button state structure")
                    return data
            
            default_state = {
                "count": 0,
                "last_updated": time.time(),
                "version": "2.0"
            }
            
            return self._safe_file_operation(
                "Load button state",
                self.config.CLICK_DATA_FILE,
                load_operation,
                default_state
            )
    
    def save_button_state(self, state: Dict[str, Any]) -> bool:
        """Save button state to file with thread safety and atomic writes"""
        with self._file_locks['clicks']:
            try:
                # Update timestamp and version
                state["last_updated"] = time.time()
                state["version"] = "2.0"
                
                # Atomic write: write to temp file first, then rename
                temp_file = self.config.CLICK_DATA_FILE + '.tmp'
                with open(temp_file, 'w') as f:
                    json.dump(state, f, indent=2)
                
                # Atomic rename
                if os.name == 'nt':  # Windows
                    if os.path.exists(self.config.CLICK_DATA_FILE):
                        os.remove(self.config.CLICK_DATA_FILE)
                    os.rename(temp_file, self.config.CLICK_DATA_FILE)
                else:  # Unix-like systems
                    os.rename(temp_file, self.config.CLICK_DATA_FILE)
                
                logger.debug(f"Button state saved: count={state.get('count', 0)}")
                return True
                
            except Exception as e:
                logger.error(f"Error saving button state: {e}")
                # Clean up temp file if it exists
                if os.path.exists(temp_file):
                    try:
                        os.remove(temp_file)
                    except:
                        pass
                return False
    
    def load_achievements(self) -> Dict[str, Any]:
        """Load achievements data from file"""
        with self._file_locks['achievements']:
            def load_operation():
                with open(self.config.ACHIEVEMENTS_FILE, 'r') as f:
                    data = json.load(f)
                    # Validate structure
                    if not isinstance(data, dict):
                        raise ValueError("Invalid achievements structure")
                    return data
            
            default_achievements = {
                "global_unlocked": [],
                "player_achievements": {},
                "version": "2.0"
            }
            
            return self._safe_file_operation(
                "Load achievements",
                self.config.ACHIEVEMENTS_FILE,
                load_operation,
                default_achievements
            )
    
    def save_achievements(self, achievements_data: Dict[str, Any]) -> bool:
        """Save achievements data to file"""
        with self._file_locks['achievements']:
            try:
                achievements_data["version"] = "2.0"
                achievements_data["last_updated"] = time.time()
                
                temp_file = self.config.ACHIEVEMENTS_FILE + '.tmp'
                with open(temp_file, 'w') as f:
                    json.dump(achievements_data, f, indent=2)
                
                if os.name == 'nt':
                    if os.path.exists(self.config.ACHIEVEMENTS_FILE):
                        os.remove(self.config.ACHIEVEMENTS_FILE)
                    os.rename(temp_file, self.config.ACHIEVEMENTS_FILE)
                else:
                    os.rename(temp_file, self.config.ACHIEVEMENTS_FILE)
                
                logger.debug("Achievements data saved")
                return True
                
            except Exception as e:
                logger.error(f"Error saving achievements: {e}")
                if os.path.exists(temp_file):
                    try:
                        os.remove(temp_file)
                    except:
                        pass
                return False
    
    def load_stats(self) -> Dict[str, Any]:
        """Load stats data from file"""
        with self._file_locks['stats']:
            def load_operation():
                with open(self.config.STATS_FILE, 'r') as f:
                    data = json.load(f)
                    # Validate structure
                    if not isinstance(data, dict):
                        raise ValueError("Invalid stats structure")
                    return data
            
            default_stats = {
                "clicks_today": 0,
                "date": datetime.now().strftime("%Y-%m-%d"),
                "clicks_per_hour": [0] * 24,
                "unique_users": 0,
                "user_sessions": {},
                "version": "2.0"
            }
            
            return self._safe_file_operation(
                "Load stats",
                self.config.STATS_FILE,
                load_operation,
                default_stats
            )
    
    def save_stats(self, stats_data: Dict[str, Any]) -> bool:
        """Save stats data to file"""
        with self._file_locks['stats']:
            try:
                # Check if it's a new day and reset daily stats if needed
                today = datetime.now().strftime("%Y-%m-%d")
                if stats_data.get("date") != today:
                    stats_data["clicks_today"] = 0
                    stats_data["date"] = today
                    stats_data["clicks_per_hour"] = [0] * 24
                    logger.info("Daily stats reset for new day")
                
                stats_data["version"] = "2.0"
                stats_data["last_updated"] = time.time()
                
                temp_file = self.config.STATS_FILE + '.tmp'
                with open(temp_file, 'w') as f:
                    json.dump(stats_data, f, indent=2)
                
                if os.name == 'nt':
                    if os.path.exists(self.config.STATS_FILE):
                        os.remove(self.config.STATS_FILE)
                    os.rename(temp_file, self.config.STATS_FILE)
                else:
                    os.rename(temp_file, self.config.STATS_FILE)
                
                logger.debug("Stats data saved")
                return True
                
            except Exception as e:
                logger.error(f"Error saving stats: {e}")
                if os.path.exists(temp_file):
                    try:
                        os.remove(temp_file)
                    except:
                        pass
                return False
    
    def create_backup(self) -> Optional[str]:
        """Create a backup of all data files"""
        if not self.config.ENABLE_BACKUPS:
            return None
            
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"backup_{timestamp}.json"
            backup_path = os.path.join(self.config.BACKUP_DIR, backup_filename)
            
            # Collect all data
            backup_data = {
                "timestamp": timestamp,
                "button_state": self.load_button_state(),
                "achievements": self.load_achievements(),
                "stats": self.load_stats(),
                "version": "2.0"
            }
            
            with open(backup_path, 'w') as f:
                json.dump(backup_data, f, indent=2)
            
            logger.info(f"Backup created: {backup_path}")
            
            # Clean up old backups
            self._cleanup_old_backups()
            
            return backup_path
            
        except Exception as e:
            logger.error(f"Error creating backup: {e}")
            return None
    
    def _cleanup_old_backups(self):
        """Remove old backup files to maintain max backup count"""
        try:
            backup_files = []
            for filename in os.listdir(self.config.BACKUP_DIR):
                if filename.startswith("backup_") and filename.endswith(".json"):
                    filepath = os.path.join(self.config.BACKUP_DIR, filename)
                    backup_files.append((filepath, os.path.getmtime(filepath)))
            
            # Sort by modification time (newest first)
            backup_files.sort(key=lambda x: x[1], reverse=True)
            
            # Remove excess backups
            if len(backup_files) > self.config.MAX_BACKUPS:
                for filepath, _ in backup_files[self.config.MAX_BACKUPS:]:
                    os.remove(filepath)
                    logger.info(f"Old backup removed: {filepath}")
                    
        except Exception as e:
            logger.error(f"Error cleaning up old backups: {e}")
    
    def restore_from_backup(self, backup_path: str) -> bool:
        """Restore data from a backup file"""
        try:
            with open(backup_path, 'r') as f:
                backup_data = json.load(f)
            
            # Validate backup structure
            required_keys = ["button_state", "achievements", "stats"]
            if not all(key in backup_data for key in required_keys):
                raise ValueError("Invalid backup file structure")
            
            # Restore each data file
            success = True
            success &= self.save_button_state(backup_data["button_state"])
            success &= self.save_achievements(backup_data["achievements"])
            success &= self.save_stats(backup_data["stats"])
            
            if success:
                logger.info(f"Successfully restored from backup: {backup_path}")
            else:
                logger.error(f"Partial failure restoring from backup: {backup_path}")
            
            return success
            
        except Exception as e:
            logger.error(f"Error restoring from backup {backup_path}: {e}")
            return False
