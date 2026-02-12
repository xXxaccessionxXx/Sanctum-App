from abc import ABC, abstractmethod
from dataclasses import dataclass

# --- 1. Data Models ---

@dataclass
class Scripture:
    text: str
    reference: str
    translation: str = "ESV"

@dataclass
class Activity:
    id: str
    title: str
    description: str
    duration_minutes: int
    type: str 

@dataclass
class Confession:
    id: str
    text: str
    timestamp: str 

# --- 2. The Interface ---

class SpiritualModule(ABC):
    @property
    @abstractmethod
    def id(self) -> str:
        pass

    @property
    @abstractmethod
    def title(self) -> str:
        pass

    @property
    @abstractmethod
    def icon_char(self) -> str:
        """
        We will use Unicode characters (e.g., '🛡️') for stability 
        instead of relying on library-specific icon sets.
        """
        pass

    @property
    @abstractmethod
    def theme_color(self) -> str:
        """Hex code"""
        pass

    @abstractmethod
    def get_daily_manna(self) -> Scripture:
        pass

    @abstractmethod
    def get_escape_route(self) -> Activity:
        pass