#!/usr/bin/env python3
"""
Test script for environment variable configuration
Usage:
  export TELEGRAM_BOT_TOKEN="test_token"
  export TELEGRAM_CHAT_ID="test_chat_id"
  python scripts/test_env_config.py
"""

import sys
import os

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from halooglasi_parser.config_loader import config_loader
from halooglasi_parser.config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID


def main():
    print("🧪 Testing Environment Variable Configuration")
    print("=" * 60)
    
    # Show current environment variables
    print("\n🌍 Environment Variables:")
    env_vars = ['TELEGRAM_BOT_TOKEN', 'TELEGRAM_CHAT_ID']
    for var in env_vars:
        value = os.environ.get(var)
        if value:
            # Mask sensitive values for display
            masked_value = value[:8] + "..." if len(value) > 8 else value
            print(f"  {var}: {masked_value}")
        else:
            print(f"  {var}: Not set")
    
    # Show configuration summary
    config_loader.print_config_summary()
    
    # Show actual loaded values
    print("\n📋 Loaded Configuration Values:")
    print(f"  TELEGRAM_BOT_TOKEN: {TELEGRAM_BOT_TOKEN[:8]}..." if len(TELEGRAM_BOT_TOKEN) > 8 else TELEGRAM_BOT_TOKEN)
    print(f"  TELEGRAM_CHAT_ID: {TELEGRAM_CHAT_ID}")
    
    # Validation
    print(f"\n✅ Telegram Config Valid: {config_loader.validate_telegram_config()}")
    
    print("\n" + "=" * 60)
    print("💡 To test environment variables:")
    print("   export TELEGRAM_BOT_TOKEN='your_token'")
    print("   export TELEGRAM_CHAT_ID='your_chat_id'")
    print("   python scripts/test_env_config.py")


if __name__ == "__main__":
    main() 