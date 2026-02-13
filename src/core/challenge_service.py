from datetime import datetime
from src.core.stats_service import StatsService

class ChallengeService:
    def __init__(self):
        self.stats_service = StatsService()
        self.challenges_db = [
            {
                "id": "purity_fast",
                "title": "The Purity Fast",
                "desc": "Do not open the browser for 1 hour. Read Scripture instead.",
                "module_trigger": "lust",
                "trigger_threshold_24h": 3, # If lust module visited > 3 times
                "type": "abstinence"
            },
            {
                "id": "cooling_sprint",
                "title": "The Cooling Sprint",
                "desc": "Use the Cooling Chamber 3 times today.",
                "module_trigger": "anger",
                "trigger_threshold_24h": 2,
                "type": "action"
            },
            {
                "id": "confession_call",
                "title": "Call to Confession",
                "desc": "You haven't journaled in 3 days. Write one entry now.",
                "module_trigger": "journal",
                "trigger_days_unused": 3,
                "type": "action"
            },
            {
                "id": "gratitude_check",
                "title": "Ledger Audit",
                "desc": "Log 5 blessings in the Ledger of Grace.",
                "module_trigger": "greed",
                "trigger_days_unused": 5,
                "type": "action"
            }
        ]

    def get_active_challenges(self):
        """
        Returns a list of active challenges. Generates new ones if needed (up to 5).
        """
        today_str = datetime.now().strftime("%Y-%m-%d")
        history = self.stats_service.stats.get("challenges", [])
        
        active_list = []
        c_today_completed = 0
        c_today_generated = 0
        
        # 1. Collect currently active
        for entry in history:
            if entry.get("status") == "active":
                active_list.append(entry)
            elif entry.get("date") == today_str and entry.get("status") == "completed":
                c_today_completed += 1
                
        # Count challenges generated today (to avoid infinite spam if user completes them fast)
        # Actually, let's just cap TOTAL active at 5.
        
        # 2. Add 'Permission' Challenge if not monitoring and not already present
        if not self.stats_service.is_monitoring_enabled():
             # Check if permission prompt is already active
             if not any(c["id"] == "permission_grant" for c in active_list):
                 perm_challenge = {
                     "id": "permission_grant",
                     "title": "Deepen the Mirror",
                     "desc": "Allow Grace of God to see your activity for better guidance?",
                     "date": today_str,
                     "status": "active",
                     "type": "system"
                 }
                 active_list.append(perm_challenge)
                 # We don't save system prompts to JSON history usually, but let's do it for consistency
                 # Or just return it dynamically? Let's save it so 'complete' works same way.
                 self.stats_service.stats["challenges"].append(perm_challenge)
                 self.stats_service._save_stats()
        
        # 3. Generate new challenges if < 5 active logic
        # Rule: Max 5 active at once.
        while len(active_list) < 5:
            new_c = self._generate_challenge(active_list)
            if not new_c:
                break # No more triggers matched
            
            # Save
            record = {
                "id": new_c["id"],
                "title": new_c["title"],
                "desc": new_c["desc"],
                "date": today_str,
                "status": "active",
                "progress": 0,
                "target": 1
            }
            self.stats_service.stats["challenges"].append(record)
            self.stats_service._save_stats()
            active_list.append(record)
            
        return active_list

    def _generate_challenge(self, current_active):
        """Analyzes stats to pick a challenge. Returns dict or None."""
        active_ids = [c["id"] for c in current_active]
        
        # Helper to check if already active
        def is_active(cid): return cid in active_ids

        # --- Context Triggers ---
        import random
        hour = datetime.now().hour
        
        # Morning Trigger (5-10 AM)
        if 5 <= hour < 10 and not is_active("morning_prayer"):
             return {
                 "id": "morning_prayer",
                 "title": "Morning Zeal",
                 "desc": "Start the day with the 'Diligence' module.",
                 "type": "action"
             }

        # Evening Trigger (8-11 PM)
        if 20 <= hour < 23 and not is_active("evening_examen"):
             return {
                 "id": "evening_examen",
                 "title": "Evening Examen",
                 "desc": "Review your day in the 'Gluttony' or 'Greed' module.",
                 "type": "action"
             }

        # --- Stat Triggers ---
        
        # Check Lust (High Usage)
        lust_usage = self.stats_service.get_entries_last_24h("lust")
        if lust_usage >= 3 and not is_active("purity_fast"):
            return self._find_challenge_by_id("purity_fast")

        # Check Anger (High Usage)
        anger_usage = self.stats_service.get_entries_last_24h("anger")
        if anger_usage >= 2 and not is_active("cooling_sprint"):
            return self._find_challenge_by_id("cooling_sprint")

        # Check Journal (Low Usage)
        journal_unused = self.stats_service.get_days_since_last_use("journal")
        if journal_unused >= 3 and not is_active("confession_call"):
            return self._find_challenge_by_id("confession_call")

        # --- Activity Triggers (New) ---
        # 1. Gaming Trigger (e.g. "League of Legends", "Steam", "Minecraft")
        # We need to scan activity log for today
        if self.stats_service.is_monitoring_enabled():
             today_key = datetime.now().strftime("%Y-%m-%d")
             # Sum up gaming time across hours for today
             total_game_seconds = 0
             total_browser_seconds = 0
             
             # Keywords
             game_keywords = ["league of legends", "steam", "minecraft", "valorant", "overwatch", "fortnite"]
             browser_keywords = ["chrome", "firefox", "edge", "opera", "brave"]
             
             # Scan all keys starting with today's date
             if "activity_log" in self.stats_service.stats:
                  for key, apps in self.stats_service.stats["activity_log"].items():
                      if key.startswith(today_key):
                           for app_title, duration in apps.items():
                               title_lower = app_title.lower()
                               if any(k in title_lower for k in game_keywords):
                                   total_game_seconds += duration
                               if any(k in title_lower for k in browser_keywords):
                                   total_browser_seconds += duration
            
             # Trigger Sloth/Diligence if Gaming > 2 hours (7200s)
             if total_game_seconds > 7200 and not is_active("gaming_detox"):
                  return {
                      "id": "gaming_detox",
                      "title": "Digital Fast",
                      "desc": f"You've spent {int(total_game_seconds/60)}m gaming today. Step away.",
                      "type": "abstinence"
                  }
             
             # Trigger Temperance if Browser > 4 hours
             if total_browser_seconds > 14400 and not is_active("browser_limit"):
                  return {
                      "id": "browser_limit",
                      "title": "Mindless Scroll",
                      "desc": "High browser usage detected. Close tabs and pray.",
                      "type": "abstinence"
                  }

        # Random Fillers (if we have space giving variance)
        fillers = [
            {"id": "daily_offering", "title": "Daily Offering", "desc": "Pray 'The Hidden Intercessor' for someone you dislike."},
            {"id": "silence_hour", "title": "Hour of Silence", "desc": "No music or media for 1 hour."},
            {"id": "nature_walk", "title": "Creation Walk", "desc": "Walk outside 5 mins without phone."}
        ]
        
        available_fillers = [f for f in fillers if not is_active(f["id"])]
        if available_fillers:
            # 30% chance to add a random filler if we pass specific triggers
            if random.random() < 0.3:
                return random.choice(available_fillers)

        return None

    def complete_challenge(self, challenge_id):
        """Marks a specific challenge as complete."""
        history = self.stats_service.stats.get("challenges", [])
        for entry in history:
            if entry.get("id") == challenge_id and entry.get("status") == "active":
                entry["status"] = "completed"
                entry["completed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Special Logic for Permission Grant
                if challenge_id == "permission_grant":
                    self.stats_service.set_monitoring(True)
                
                self.stats_service._save_stats()
                return True
        return False

    def _find_challenge_by_id(self, c_id):
        for c in self.challenges_db:
            if c["id"] == c_id:
                return c
        return None


