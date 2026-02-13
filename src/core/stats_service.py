import json
import os
from datetime import datetime, timedelta

STATS_FILE = "data/stats.json"

class StatsService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(StatsService, cls).__new__(cls)
            cls._instance._load_stats()
        return cls._instance

    def _load_stats(self):
        self.stats = {}
        if os.path.exists(STATS_FILE):
            try:
                with open(STATS_FILE, "r") as f:
                    self.stats = json.load(f)
            except:
                self.stats = {}
        
        # Ensure structure: {"module_name": ["YYYY-MM-DD HH:MM", ...]}
        # Also track challenge history: {"challenges": [{"id": ..., "date": ..., "status": ...}]}
        if "challenges" not in self.stats:
            self.stats["challenges"] = []
            
        if "monitoring_enabled" not in self.stats:
            self.stats["monitoring_enabled"] = False

    def set_monitoring(self, enabled: bool):
        self.stats["monitoring_enabled"] = enabled
        self._save_stats()

    def is_monitoring_enabled(self) -> bool:
        return self.stats.get("monitoring_enabled", False)

    def log_module_entry(self, module_name):
        """Logs that a user entered a specific module."""
        if module_name not in self.stats:
            self.stats[module_name] = []
        
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.stats[module_name].append(now)
        self._save_stats()

    def get_entries_last_24h(self, module_name):
        """Returns count of entries in the last 24 hours."""
        if module_name not in self.stats:
            return 0
        
        count = 0
        now = datetime.now()
        one_day_ago = now - timedelta(days=1)
        
        # Filter and clean up old entries (optional optimization)
        valid_entries = []
        for timestamp in self.stats[module_name]:
            try:
                dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
                if dt > one_day_ago:
                    count += 1
                valid_entries.append(timestamp) # Keep history for now
            except:
                pass
        
        # Optionally prune here if list gets too long
        return count

    def get_days_since_last_use(self, module_name):
        """Returns days since last use. Returns -1 if never used."""
        if module_name not in self.stats or not self.stats[module_name]:
            return -1
        
        last_entry = self.stats[module_name][-1]
        try:
            dt = datetime.strptime(last_entry, "%Y-%m-%d %H:%M:%S")
            delta = datetime.now() - dt
            return delta.days
        except:
            return -1

    def log_activity(self, app_title, duration_seconds):
        """Logs user activity (app title and duration)."""
        if "activity_log" not in self.stats:
            self.stats["activity_log"] = {} # {date_hour: {app_name: total_seconds}}
            
        # Key by Date+Hour to allow pruning/analysis
        key = datetime.now().strftime("%Y-%m-%d %H")
        
        if key not in self.stats["activity_log"]:
            self.stats["activity_log"][key] = {}
            
        current = self.stats["activity_log"][key].get(app_title, 0)
        self.stats["activity_log"][key][app_title] = current + duration_seconds
        
        # Optimize save: only save every X updates or implicitly? 
        # For now, save every time (might be IO heavy, but safe)
        self._save_stats()

    def get_recent_activity(self, hours=1):
        """Returns aggregated activity for the last X hours."""
        # Simple implementation for now
        pass

    def _save_stats(self):
        os.makedirs(os.path.dirname(STATS_FILE), exist_ok=True)
        with open(STATS_FILE, "w") as f:
            json.dump(self.stats, f, indent=4)
