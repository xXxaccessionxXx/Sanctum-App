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
        return ScriptureService.get_smart_verse("temperance")

    def get_activities(self) -> list[Activity]:
        return [
            Activity(
                id="gluttony_manna",
                title="The Manna Portion",
                description="Feast on the Word for 60 seconds before you eat.",
                duration_minutes=1,
                type="Mindfulness"
            ),
             Activity(
                id="gluttony_water",
                title="The Water Fast",
                description="Drink a warm glass of water slowly. Appreciate its purity.",
                duration_minutes=2,
                type="Physical"
            ),
             Activity(
                id="gluttony_walk",
                title="The Prayer Walk",
                description="Walk for 5 minutes. Pray for those who have no food.",
                duration_minutes=5,
                type="Physical"
            )
        ]

    def get_escape_route(self) -> Activity:
        # Default/Primary activity
        return self.get_activities()[0]
