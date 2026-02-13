import random
from src.core.covenant import SpiritualModule, Scripture, Activity

class AngerModule(SpiritualModule):
    @property
    def id(self) -> str:
        return "sin_anger"

    @property
    def title(self) -> str:
        return "Peace" # Virtue focus

    @property
    def icon_char(self) -> str:
        return "🕊️" # Dove

    @property
    def theme_color(self) -> str:
        return "#B71C1C" # Deep Red (Subdued)

    def get_daily_manna(self) -> Scripture:
        from src.core.scripture_service import ScriptureService
        return ScriptureService.get_smart_verse("peace")

    def get_activities(self) -> list[Activity]:
        return [
            Activity(
                id="anger_cool_down",
                title="The Cooling Chamber",
                description="Type your feelings, but you cannot send them for 60 seconds.",
                duration_minutes=1,
                type="Intervention"
            ),
            Activity(
                id="anger_prayer",
                title="Prayer for Enemies",
                description="Pray for the person you are angry with. Wish them good.",
                duration_minutes=3,
                type="Prayer"
            ),
            Activity(
                id="anger_journal",
                title="Journal the Rage",
                description="Write down your anger to release it from your mind.",
                duration_minutes=5,
                type="Journaling"
            ),
            Activity(
                id="anger_physical",
                title="Physical Release",
                description="Do pushups or run to burn off the adrenaline.",
                duration_minutes=2,
                type="Physical"
            )
        ]

    def get_escape_route(self) -> Activity:
        return self.get_activities()[0]