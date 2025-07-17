#!/usr/bin/env python3
"""
HaloOglasi Apartment Parser - Automated Scheduler
Runs apartment search at 7:00 AM, 1:00 PM, and 7:00 PM daily
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
    """Check if current time is one of the scheduled times (7:00 AM, 1:00 PM, 7:00 PM)"""
    now = datetime.now().time()
    scheduled_times = [
        dt_time(7, 0),   # 7:00 AM
        dt_time(13, 0),  # 1:00 PM  
        dt_time(19, 0),  # 7:00 PM
    ]
    
    # Allow a 5-minute window around each scheduled time
    for scheduled_time in scheduled_times:
        # Convert to minutes for easier comparison
        now_minutes = now.hour * 60 + now.minute
        scheduled_minutes = scheduled_time.hour * 60 + scheduled_time.minute
        
        # Check if within 5 minutes of scheduled time
        if abs(now_minutes - scheduled_minutes) <= 5:
            return True
    
    return False

def scheduled_apartment_search():
    """Wrapper function for scheduled apartment search"""
    if not is_within_active_hours():
        logger.info("Outside scheduled hours (7:00 AM, 1:00 PM, 7:00 PM), skipping search")
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
    logger.info("📅 Schedule: Daily at 7:00 AM, 1:00 PM, and 7:00 PM")
    logger.info("🔄 Press Ctrl+C to stop the scheduler")
    logger.info("")
    
    # Schedule the job at specific times: 7am, 1pm, 7pm
    schedule.every().day.at("07:00").do(scheduled_apartment_search)
    schedule.every().day.at("13:00").do(scheduled_apartment_search)
    schedule.every().day.at("19:00").do(scheduled_apartment_search)
    
    # Show next scheduled run time
    next_run = schedule.next_run()
    if next_run:
        logger.info(f"⏰ Next scheduled run: {next_run.strftime('%Y-%m-%d %H:%M:%S')}")
    else:
        logger.info("⏰ Waiting for next scheduled time...")
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    except KeyboardInterrupt:
        logger.info("\n🛑 Scheduler stopped by user")
        logger.info("👋 Goodbye!")

if __name__ == "__main__":
    main() 