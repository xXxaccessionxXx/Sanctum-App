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
        return ScriptureService.get_verse("peace")

    def get_escape_route(self) -> Activity:
        return Activity(
            id="anger_cool_down",
            title="The Cooling Chamber",
            description="Type your feelings, but you cannot send them for 60 seconds.",
            duration_minutes=1,
            type="Intervention"
        )