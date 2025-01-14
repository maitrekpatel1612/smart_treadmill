# config/settings.py
from typing import Dict, Any
import json
import os

class Settings:
    # Default settings
    _defaults = {
        # Hardware settings
        'SERIAL_PORT': '/dev/ttyUSB0',
        'BAUD_RATE': 9600,
        'HEART_RATE_TIMEOUT': 5,  # seconds
        
        # Analysis settings
        'SAMPLING_RATE': 5,  # seconds
        'MAX_HEART_RATE_DEFAULT': 220,
        'MIN_DATA_POINTS_FOR_THRESHOLD': 10,
        
        # UI settings
        'WINDOW_SIZE': (1024, 768),
        'PLOT_UPDATE_INTERVAL': 1000,  # ms
        'MAX_PLOT_POINTS': 3600,  # 1 hour of data at 1 Hz
        
        # Training zones (percentages of max heart rate)
        'TRAINING_ZONES': {
            'RECOVERY': (0.60, 0.70),
            'AEROBIC': (0.70, 0.80),
            'ANAEROBIC_THRESHOLD': (0.80, 0.90),
            'VO2_MAX': (0.90, 1.00)
        },
        
        # Data storage
        'DATA_DIR': 'data',
        'LOGS_DIR': 'logs',
    }

    @classmethod
    def load(cls, config_file: str = None) -> Dict[str, Any]:
        """Load settings from config file, falling back to defaults"""
        settings = cls._defaults.copy()
        
        if config_file and os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    user_settings = json.load(f)
                settings.update(user_settings)
            except json.JSONDecodeError:
                print(f"Warning: Could not parse config file {config_file}")
            except Exception as e:
                print(f"Warning: Error loading config file: {e}")
        
        # Create necessary directories
        os.makedirs(settings['DATA_DIR'], exist_ok=True)
        os.makedirs(settings['LOGS_DIR'], exist_ok=True)
        
        return settings

    @classmethod
    def save(cls, settings: Dict[str, Any], config_file: str):
        """Save current settings to config file"""
        with open(config_file, 'w') as f:
            json.dump(settings, f, indent=4)