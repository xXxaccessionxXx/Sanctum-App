from src.core.covenant import SpiritualModule, Scripture, Activity

class GreedModule(SpiritualModule):
    @property
    def id(self) -> str:
        return "sin_greed"

    @property
    def title(self) -> str:
        return "Contentment"

    @property
    def icon_char(self) -> str:
        return "🎁" 

    @property
    def theme_color(self) -> str:
        return "#2E7D32" # Green (Growth, distinct from Money Green)

    def get_daily_manna(self) -> Scripture:
        from src.core.scripture_service import ScriptureService
        return ScriptureService.get_verse("contentment")

    def get_escape_route(self) -> Activity:
        return Activity(
            id="greed_gratitude",
            title="The Ledger of Grace",
            description="Log 3 blessings that money cannot buy.",
            duration_minutes=3,
            type="Journaling"
        )
