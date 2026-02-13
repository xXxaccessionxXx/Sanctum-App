from plyer import notification
import threading
import time
import random
from src.core.stats_service import StatsService
from src.core.scripture_service import ScriptureService

class NotificationService:
    def __init__(self, interval_minutes=60):
        self.interval = interval_minutes * 60
        self.stats = StatsService()
        self.stop_event = threading.Event()
        self.thread = None

    def start(self):
        """Starts the notification scheduler."""
        if self.thread and self.thread.is_alive():
            return
            
        self.stop_event.clear()
        self.thread = threading.Thread(target=self._loop, daemon=True)
        self.thread.start()

    def stop(self):
        self.stop_event.set()
        if self.thread:
            self.thread.join(timeout=1.0)

    def _loop(self):
        # Initial delay so it doesn't pop immediately on startup
        time.sleep(10)
        
        while not self.stop_event.is_set():
            # Check monitoring enabled? Or separate setting?
            # For now, let's assume if monitoring is on, notifications are on, 
            # OR we can add a separate toggle later. using monitoring for now.
            if self.stats.is_monitoring_enabled():
                self._send_random_verse()
            
            # Sleep for interval (with checks)
            for _ in range(int(self.interval / 5)):
                if self.stop_event.is_set(): break
                time.sleep(5)

    def _send_random_verse(self):
        try:
            # Send a time-aware verse
            verse = ScriptureService.get_smart_verse()
            
            notification.notify(
                title="Grace of God",
                message=f"{verse.text}\n- {verse.reference}",
                app_name="Grace of God",
                timeout=10
            )
        except Exception as e:
            print(f"Notification Error: {e}")

    def send_manual(self, title, message):
        """Allows other services to trigger notifications."""
        try:
            notification.notify(
                title=title,
                message=message,
                app_name="Grace of God",
                timeout=10
            )
        except:
            pass
