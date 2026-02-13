import random
from src.core.covenant import SpiritualModule, Scripture, Activity

class LustModule(SpiritualModule):
    @property
    def id(self) -> str:
        return "sin_lust"

    @property
    def title(self) -> str:
        return "Purity"

    @property
    def icon_char(self) -> str:
        return "🔥" # Fire (to be quenched) or Lilies? Let's go with Shield 🛡️ or Water 💧. 
                   # Existing modules: Anger=Dove, Pride=Diamond. 
                   # Let's use 🛡️ for Guarding Heart.
        return "🛡️"

    @property
    def theme_color(self) -> str:
        return "#1565C0" # Blue (Calm/Cool)

    def get_daily_manna(self) -> Scripture:
        from src.core.scripture_service import ScriptureService
        return ScriptureService.get_smart_verse("purity")

    def get_activities(self) -> list[Activity]:
        return [
            Activity(
                id="lust_flight",
                title="Flee & Pray",
                description="Leave the room immediately and say the Jesus Prayer.",
                duration_minutes=5,
                type="Action"
            ),
            Activity(
                id="lust_covenant",
                title="Covenant Eyes",
                description="Review your 'Why'. Remember who you are fighting for.",
                duration_minutes=3,
                type="Reflection"
            ),
             Activity(
                id="lust_shock",
                title="Cold Shock",
                description="Splash cold water on your face or take a cold shower.",
                duration_minutes=2,
                type="Physical"
            )
        ]

    def get_escape_route(self) -> Activity:
        return self.get_activities()[0]
