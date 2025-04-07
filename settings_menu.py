import os
import time
import threading
import colorama
from colorama import Fore, Style

# Initialize colorama
colorama.init()

class Settings:
    def __init__(self, threshold=5.0, interval=1, ai_enabled=False):
        self.threshold = threshold
        self.interval = interval
        self.ai_enabled = ai_enabled
        self.settings_changed = threading.Event()
        self.exit_requested = threading.Event()
        self.menu_active = False
        self.lock = threading.Lock()

    def display_current_settings(self):
        """Display the current settings"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"\n{Style.BRIGHT}{Fore.CYAN}=== STOCK TRACKER SETTINGS ==={Style.RESET_ALL}")
        print(f"1. Alert Threshold: {Fore.YELLOW}{self.threshold}%{Style.RESET_ALL}")
        print(f"2. Refresh Interval: {Fore.YELLOW}{self.interval} minute(s){Style.RESET_ALL}")
        print(f"3. AI Insights: {Fore.GREEN if self.ai_enabled else Fore.RED}{self.ai_enabled}{Style.RESET_ALL}")
        print(f"4. {Fore.GREEN}Apply Changes & Return to Market View{Style.RESET_ALL}")
        print(f"5. {Fore.RED}Exit Application{Style.RESET_ALL}")
        print(f"\n{Style.DIM}Press the number of the setting you want to change...{Style.RESET_ALL}")

    def update_threshold(self):
        """Update the alert threshold"""
        try:
            print(f"\nCurrent alert threshold: {self.threshold}%")
            new_threshold = float(input("Enter new threshold (e.g., 2.5): "))
            if new_threshold < 0:
                print(f"{Fore.RED}Threshold must be a positive number.{Style.RESET_ALL}")
                time.sleep(1.5)
                return
            
            with self.lock:
                self.threshold = new_threshold
            print(f"{Fore.GREEN}Threshold updated to {new_threshold}%{Style.RESET_ALL}")
            time.sleep(1)
        except ValueError:
            print(f"{Fore.RED}Invalid input. Please enter a number.{Style.RESET_ALL}")
            time.sleep(1.5)

    def update_interval(self):
        """Update the refresh interval"""
        try:
            print(f"\nCurrent refresh interval: {self.interval} minute(s)")
            new_interval = int(input("Enter new interval in minutes (e.g., 5): "))
            if new_interval < 1:
                print(f"{Fore.RED}Interval must be at least 1 minute.{Style.RESET_ALL}")
                time.sleep(1.5)
                return
            
            with self.lock:
                self.interval = new_interval
            print(f"{Fore.GREEN}Interval updated to {new_interval} minute(s){Style.RESET_ALL}")
            time.sleep(1)
        except ValueError:
            print(f"{Fore.RED}Invalid input. Please enter a whole number.{Style.RESET_ALL}")
            time.sleep(1.5)

    def toggle_ai(self):
        """Toggle AI insights on/off"""
        with self.lock:
            self.ai_enabled = not self.ai_enabled
        status = "enabled" if self.ai_enabled else "disabled"
        print(f"{Fore.GREEN}AI insights {status}{Style.RESET_ALL}")
        time.sleep(1)

    def show_menu(self):
        """Show the settings menu and handle user input"""
        self.menu_active = True
        while self.menu_active:
            self.display_current_settings()
            choice = input("\nEnter your choice (1-5): ")
            
            if choice == '1':
                self.update_threshold()
            elif choice == '2':
                self.update_interval()
            elif choice == '3':
                self.toggle_ai()
            elif choice == '4':
                self.menu_active = False
                self.settings_changed.set()
                print(f"{Fore.GREEN}Applying changes and returning to market view...{Style.RESET_ALL}")
                time.sleep(1)
            elif choice == '5':
                self.menu_active = False
                self.exit_requested.set()
                print(f"{Fore.RED}Exiting application...{Style.RESET_ALL}")
                time.sleep(1)
            else:
                print(f"{Fore.RED}Invalid choice. Please enter a number between 1 and 5.{Style.RESET_ALL}")
                time.sleep(1)

    def start_menu_thread(self):
        """Start the menu in a separate thread"""
        menu_thread = threading.Thread(target=self.show_menu)
        menu_thread.daemon = True
        menu_thread.start()
        return menu_thread

def get_settings_instance(initial_threshold=5.0, initial_interval=1, initial_ai=False):
    """Get a singleton instance of Settings"""
    if not hasattr(get_settings_instance, "instance"):
        get_settings_instance.instance = Settings(
            threshold=initial_threshold,
            interval=initial_interval,
            ai_enabled=initial_ai
        )
    return get_settings_instance.instance
