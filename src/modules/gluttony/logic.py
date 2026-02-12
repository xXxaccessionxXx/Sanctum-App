from src.core.covenant import SpiritualModule, Scripture, Activity

class GluttonyModule(SpiritualModule):
    @property
    def id(self) -> str:
        return "sin_gluttony"

    @property
    def title(self) -> str:
        return "Temperance"

    @property
    def icon_char(self) -> str:
        return "🍞" 

    @property
    def theme_color(self) -> str:
        return "#795548" # Brown (Bread/Earth) or #8D6E63

    def get_daily_manna(self) -> Scripture:
        from src.core.scripture_service import ScriptureService
        return ScriptureService.get_verse("temperance")

    def get_escape_route(self) -> Activity:
        return Activity(
            id="gluttony_manna",
            title="The Manna Portion",
            description="Feast on the Word for 60 seconds before you eat.",
            duration_minutes=1,
            type="Mindfulness"
        )
