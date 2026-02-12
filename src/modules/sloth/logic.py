from src.core.covenant import SpiritualModule, Scripture, Activity

class SlothModule(SpiritualModule):
    @property
    def id(self) -> str:
        return "sin_sloth"

    @property
    def title(self) -> str:
        return "Diligence"

    @property
    def icon_char(self) -> str:
        return "🐜" # Ant (Proverbs 6:6) or Hammer/Trowel. Let's use 🧱 for Building. 
        return "🧱"

    @property
    def theme_color(self) -> str:
        return "#FB8C00" # Orange (Energy/Work)

    def get_daily_manna(self) -> Scripture:
        from src.core.scripture_service import ScriptureService
        return ScriptureService.get_verse("diligence")

    def get_escape_route(self) -> Activity:
        return Activity(
            id="sloth_work",
            title="The First Brick",
            description="Do just one minute of the task you are avoiding.",
            duration_minutes=25,
            type="Work"
        )
