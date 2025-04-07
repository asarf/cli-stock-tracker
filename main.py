import argparse
import os
import sys
import time
import threading
from apscheduler.schedulers.background import BackgroundScheduler
from stock_fetcher import fetch_indices_data
from notifier import check_notifications
from utils import display_indices_table
from ai_analytics import get_ai_insights, display_ai_insights, generate_market_summary
from settings_menu import get_settings_instance
import colorama
from colorama import Fore, Style

# Initialize colorama for colored terminal output
colorama.init()

def job():
    # Get current settings
    settings = get_settings_instance()
    
    # Clear the screen
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Show header with current settings
    print(f"{Style.BRIGHT}{Fore.GREEN}STOCK MARKET TRACKER{Style.RESET_ALL}")
    print(f"Alert Threshold: {settings.threshold}% | Refresh: {settings.interval} min | AI: {'ON' if settings.ai_enabled else 'OFF'}")
    print(f"Press 'm' to open settings menu\n")
    
    # Fetch and display data
    data = fetch_indices_data()
    display_indices_table(data)
    check_notifications(data, settings.threshold)
    
    # If AI mode is enabled, show AI-powered insights
    if settings.ai_enabled:
        print(f"\n{Fore.CYAN}Generating AI insights (this may take a moment)...{Style.RESET_ALL}")
        insights = get_ai_insights(data)
        display_ai_insights(insights)
        summary = generate_market_summary(insights)
        print(summary)

def check_for_key_press():
    """Check for 'm' key press to open the settings menu"""
    import msvcrt
    settings = get_settings_instance()
    
    while True:
        if msvcrt.kbhit():
            key = msvcrt.getch().decode('utf-8').lower()
            if key == 'm':
                # Open settings menu
                settings.show_menu()
                
                # If exit was requested, stop the application
                if settings.exit_requested.is_set():
                    print("Exiting application...")
                    os._exit(0)
                    
                # If settings were changed, update the scheduler
                if settings.settings_changed.is_set():
                    update_scheduler()
                    settings.settings_changed.clear()
                    
                # Run the job immediately with new settings
                job()
        time.sleep(0.1)

def update_scheduler():
    """Update the scheduler with new settings"""
    global scheduler
    settings = get_settings_instance()
    
    # Remove existing jobs
    for job_obj in scheduler.get_jobs():
        scheduler.remove_job(job_obj.id)
    
    # Add new job with updated interval
    scheduler.add_job(fetch_and_display, 'interval', minutes=settings.interval, id='market_update')

def fetch_and_display():
    """Wrapper function for the job to avoid name conflicts"""
    job()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Live Global Stock Market CLI Tracker")
    parser.add_argument("--threshold", type=float, default=5.0,
                        help="Percentage threshold for notifications (default: 5%)")
    parser.add_argument("--ai", action="store_true",
                        help="Enable AI-powered market insights and predictions")
    parser.add_argument("--interval", type=int, default=1,
                        help="Refresh interval in minutes (default: 1)")
    args = parser.parse_args()

    # Initialize settings with command line arguments
    settings = get_settings_instance(
        initial_threshold=args.threshold,
        initial_interval=args.interval,
        initial_ai=args.ai
    )

    # Use background scheduler instead of blocking
    scheduler = BackgroundScheduler()
    scheduler.add_job(fetch_and_display, 'interval', minutes=settings.interval, id='market_update')

    # Use colorama for colored output
    print(f"{Fore.GREEN}[LAUNCH] Starting Stock Market Tracker{Style.RESET_ALL}")
    print(f"  - Refresh interval: {settings.interval} minute(s)")
    print(f"  - Alert threshold: {settings.threshold}%")
    print(f"  - AI-powered insights: {'ENABLED' if settings.ai_enabled else 'DISABLED'}")
    print(f"  - Press 'm' at any time to open the settings menu")
    print("")
    
    # Start the scheduler
    scheduler.start()
    
    # Run the job immediately
    job()
    
    # Start the key press listener in the main thread
    try:
        check_for_key_press()
    except KeyboardInterrupt:
        print("\nExiting application...")
        scheduler.shutdown()
        sys.exit(0)