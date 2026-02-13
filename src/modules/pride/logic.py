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
        return ScriptureService.get_smart_verse("humility")

    def get_activities(self) -> list[Activity]:
        return [
            Activity(
                id="pride_litany",
                title="The Litany of Humility",
                description="Read the prayer of surrender.",
                duration_minutes=2,
                type="Prayer"
            ),
             Activity(
                id="pride_service",
                title="Service of Humility",
                description="Do a hidden chore or act of service. Tell no one.",
                duration_minutes=10,
                type="Service"
            ),
             Activity(
                id="pride_silence",
                title="The Validation Fast",
                description="Commit to staying silent when you want credit.",
                duration_minutes=1,
                type="Intention"
            )
        ]

    def get_escape_route(self) -> Activity:
        return self.get_activities()[0]