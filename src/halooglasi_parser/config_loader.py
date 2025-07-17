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
        1. Environment variable (highest priority)
        2. Properties file
        3. Default value (lowest priority)
        """
        # Try environment variable first (highest priority)
        env_value = os.environ.get(key)
        if env_value:
            print(f"🔧 Using environment variable for {key}")
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
    
    def is_exclusive_chat_mode(self) -> bool:
        """Check if TELEGRAM_CHAT_ID is configured for exclusive mode (disables auto-discovery)."""
        chat_id = self.get('TELEGRAM_CHAT_ID')
        return chat_id and chat_id not in ["YOUR_CHAT_ID_HERE", "", None]
    
    def validate_telegram_config(self) -> bool:
        """Validate that Telegram configuration is properly set."""
        return (self.is_configured('TELEGRAM_BOT_TOKEN') and 
                self.is_configured('TELEGRAM_CHAT_ID'))
    
    def get_config_source(self, key: str) -> str:
        """Get the source of a configuration value (env, file, or default)."""
        # Check environment variable
        if os.environ.get(key):
            return "environment"
        
        # Check properties file
        try:
            self.config.get('DEFAULT', key)
            return "properties_file"
        except (configparser.NoOptionError, configparser.NoSectionError):
            pass
        
        return "default"
    
    def print_config_summary(self):
        """Print a summary of where configuration values are loaded from."""
        important_keys = ['TELEGRAM_BOT_TOKEN', 'TELEGRAM_CHAT_ID']
        
        print("\n🔧 Configuration Sources:")
        print("=" * 50)
        
        for key in important_keys:
            source = self.get_config_source(key)
            is_configured = self.is_configured(key)
            
            if source == "environment":
                status = "✅ Environment Variable"
            elif source == "properties_file":
                status = "📄 Properties File"
            else:
                status = "⚠️  Default/Placeholder"
            
            config_status = "✅ Configured" if is_configured else "❌ Not Set"
            print(f"  {key:20} | {status:20} | {config_status}")
        
        print("=" * 50)


# Global config loader instance
config_loader = ConfigLoader() 