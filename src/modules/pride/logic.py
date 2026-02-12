import random
from src.core.covenant import SpiritualModule, Scripture, Activity

class PrideModule(SpiritualModule):
    @property
    def id(self) -> str:
        return "sin_pride"

    @property
    def title(self) -> str:
        return "Humility"

    @property
    def icon_char(self) -> str:
        return "💎"  # Diamond for value/purity

    @property
    def theme_color(self) -> str:
        return "#4A148C"  # Deep Purple

    def get_daily_manna(self) -> Scripture:
        from src.core.scripture_service import ScriptureService
        return ScriptureService.get_verse("humility")

    def get_escape_route(self) -> Activity:
        return Activity(
            id="pride_reset",
            title="The Litany of Humility",
            description="Read the prayer of surrender.",
            duration_minutes=2,
            type="Prayer"
        )