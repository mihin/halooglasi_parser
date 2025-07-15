"""
Configuration loader for reading credentials from properties file.
Handles loading sensitive configuration from config.properties file.
"""

import os
import configparser
from typing import Dict, Optional


class ConfigLoader:
    """Loads configuration from properties file with fallback to environment variables."""
    
    def __init__(self, config_file: str = "config.properties"):
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        self._load_config()
    
    def _load_config(self):
        """Load configuration from properties file."""
        # Get the project root directory (three levels up from this file)
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        config_path = os.path.join(project_root, self.config_file)
        
        if os.path.exists(config_path):
            # Read properties file with configparser
            # Add a default section since properties files don't have sections
            with open(config_path, 'r', encoding='utf-8') as f:
                config_string = '[DEFAULT]\n' + f.read()
            
            self.config.read_string(config_string)
        else:
            print(f"⚠️  Warning: {config_path} not found. Using environment variables or defaults.")
    
    def get(self, key: str, default: Optional[str] = None) -> str:
        """
        Get configuration value by key.
        
        Priority order:
        1. Environment variable
        2. Properties file
        3. Default value
        """
        # Try environment variable first
        env_value = os.environ.get(key)
        if env_value:
            return env_value
        
        # Try properties file
        try:
            return self.config.get('DEFAULT', key)
        except (configparser.NoOptionError, configparser.NoSectionError):
            pass
        
        # Return default or original placeholder
        if default is not None:
            return default
        
        # Return placeholder for required values
        if key in ['TELEGRAM_BOT_TOKEN', 'TELEGRAM_CHAT_ID']:
            return f"YOUR_{key}_HERE"
        
        return ""
    
    def get_all_credentials(self) -> Dict[str, str]:
        """Get all credential values as a dictionary."""
        credentials = {}
        
        # Define all credential keys
        credential_keys = [
            'TELEGRAM_BOT_TOKEN',
            'TELEGRAM_CHAT_ID',
            'API_KEY',
            'API_SECRET',
            'DB_PASSWORD',
            'DB_HOST',
            'DB_USER',
            'EMAIL_PASSWORD',
            'SMTP_HOST',
            'SMTP_PORT',
            'WEBHOOK_SECRET'
        ]
        
        for key in credential_keys:
            credentials[key] = self.get(key)
        
        return credentials
    
    def is_configured(self, key: str) -> bool:
        """Check if a credential is properly configured (not using placeholder)."""
        value = self.get(key)
        return value and not value.startswith("YOUR_") and not value.endswith("_HERE")
    
    def validate_telegram_config(self) -> bool:
        """Validate that Telegram configuration is properly set."""
        return (self.is_configured('TELEGRAM_BOT_TOKEN') and 
                self.is_configured('TELEGRAM_CHAT_ID'))


# Global config loader instance
config_loader = ConfigLoader() 