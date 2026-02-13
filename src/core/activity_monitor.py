import time
import threading
import win32gui
from datetime import datetime
from src.core.stats_service import StatsService

class ActivityMonitor:
    def __init__(self, interval=10):
        self.interval = interval
        self.stats = StatsService()
        self.stop_event = threading.Event()
        self.monitor_thread = None

    def start(self):
        """Starts monitoring in a background thread if enabled."""
        if not self.stats.is_monitoring_enabled():
            return
            
        if self.monitor_thread and self.monitor_thread.is_alive():
            return

        self.stop_event.clear()
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()

    def stop(self):
        """Stops the monitoring thread."""
        self.stop_event.set()
        if self.monitor_thread:
            self.monitor_thread.join(timeout=2.0)

    def _monitor_loop(self):
        while not self.stop_event.is_set():
            if not self.stats.is_monitoring_enabled():
                break # Stop if permission revoked
                
            try:
                window = win32gui.GetForegroundWindow()
                title = win32gui.GetWindowText(window)
                
                if title:
                    self.stats.log_activity(title, self.interval)
            except Exception as e:
                print(f"Monitor Warning: {e}")
                
            time.sleep(self.interval)
