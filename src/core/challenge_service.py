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

    def get_active_challenge(self):
        """
        Determines the current challenge based on user stats.
        Returns a dict or None.
        """
        # 1. Check if there's already an active, uncompleted challenge for today
        today_str = datetime.now().strftime("%Y-%m-%d")
        history = self.stats_service.stats.get("challenges", [])
        
        # Check active or completed today
        for entry in history:
            # If active, return it
            if entry.get("status") == "active":
                return entry
            
            # If completed TODAY, return it (so we don't generate a new one immediately)
            if entry.get("date") == today_str and entry.get("status") == "completed":
                return entry

        # 2. If no active challenge, generate a new one
        new_challenge = self._generate_challenge()
        if new_challenge:
            # Save it as active
            record = {
                "id": new_challenge["id"],
                "title": new_challenge["title"],
                "desc": new_challenge["desc"],
                "date": today_str,
                "status": "active",
                "progress": 0,
                "target": 1 # Simplified for now
            }
            self.stats_service.stats["challenges"].append(record)
            self.stats_service._save_stats()
            return record
        
        return None

    def _generate_challenge(self):
        """Analyzes stats to pick a challenge."""
        
        # Check Lust (High Usage Trigger)
        lust_usage = self.stats_service.get_entries_last_24h("lust")
        if lust_usage >= 3:
            return self._find_challenge_by_id("purity_fast")

        # Check Anger (High Usage Trigger)
        anger_usage = self.stats_service.get_entries_last_24h("anger")
        if anger_usage >= 2:
            return self._find_challenge_by_id("cooling_sprint")

        # Check Journal (Low Usage Trigger)
        journal_unused = self.stats_service.get_days_since_last_use("journal")
        if journal_unused >= 3:
            return self._find_challenge_by_id("confession_call")

        # Default fallback (if nothing triggers, maybe random or None)
        # For now, return a generic "Daily Prayer" challenge if nothing else
        return {
            "id": "daily_prayer",
            "title": "Daily Offering",
            "desc": "Pray 'The Hidden Intercessor' for someone you dislike.",
            "type": "action"
        }

    def _find_challenge_by_id(self, c_id):
        for c in self.challenges_db:
            if c["id"] == c_id:
                return c
        return None

    def complete_challenge(self):
        """Marks the current active challenge as complete."""
        history = self.stats_service.stats.get("challenges", [])
        for entry in history:
            if entry.get("status") == "active":
                entry["status"] = "completed"
                entry["completed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.stats_service._save_stats()
                return True
        return False
