#!/usr/bin/env python3
"""
HaloOglasi Apartment Parser - Automated Scheduler
Runs apartment search every 30 minutes from 8:00 AM to 8:00 PM
"""

import schedule
import time
import logging
import sys
import os
from datetime import datetime, time as dt_time

# Add the src directory to the path so we can import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

# Import the main function from the run_search script
sys.path.append(os.path.dirname(__file__))
from run_search import main as run_apartment_search

# Configure logging
log_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'apartment_scheduler.log')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

def is_within_active_hours():
    """Check if current time is within active hours (8:00 AM - 8:00 PM)"""
    now = datetime.now().time()
    start_time = dt_time(8, 0)   # 8:00 AM
    end_time = dt_time(20, 0)    # 8:00 PM
    
    return start_time <= now <= end_time

def scheduled_apartment_search():
    """Wrapper function for scheduled apartment search"""
    if not is_within_active_hours():
        logger.info("Outside active hours (8:00 AM - 8:00 PM), skipping search")
        return
    
    logger.info("=" * 80)
    logger.info("🚀 Starting scheduled apartment search")
    logger.info("=" * 80)
    
    try:
        # Redirect print output to logger
        import sys
        from io import StringIO
        
        # Capture stdout
        old_stdout = sys.stdout
        sys.stdout = captured_output = StringIO()
        
        # Run the apartment search
        run_apartment_search()
        
        # Restore stdout
        sys.stdout = old_stdout
        
        # Log the captured output
        output = captured_output.getvalue()
        if output:
            for line in output.strip().split('\n'):
                if line.strip():
                    logger.info(line)
        
        logger.info("✅ Scheduled apartment search completed successfully")
        
    except Exception as e:
        logger.error(f"❌ Error during scheduled apartment search: {e}")
        # Restore stdout in case of error
        sys.stdout = old_stdout
    
    logger.info("=" * 80)

def main():
    """Main scheduler function"""
    logger.info("🕐 HaloOglasi Apartment Scheduler starting...")
    logger.info("📅 Schedule: Every 30 minutes from 8:00 AM to 8:00 PM")
    logger.info("🔄 Press Ctrl+C to stop the scheduler")
    logger.info("")
    
    # Schedule the job every 30 minutes
    schedule.every(30).minutes.do(scheduled_apartment_search)
    
    # Run immediately if within active hours
    if is_within_active_hours():
        logger.info("🚀 Running initial search...")
        scheduled_apartment_search()
    else:
        logger.info("⏰ Outside active hours, waiting for next scheduled time...")
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    except KeyboardInterrupt:
        logger.info("\n🛑 Scheduler stopped by user")
        logger.info("👋 Goodbye!")

if __name__ == "__main__":
    main() 