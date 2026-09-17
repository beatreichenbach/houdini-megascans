import dataclasses
import logging
from abc import ABC, abstractmethod
from enum import StrEnum

logger = logging.getLogger(__name__)


class Renderer(StrEnum):
    ARNOLD = 'Arnold'


@dataclasses.dataclass
class Options:
    renderer: Renderer = Renderer.ARNOLD
    triplanar: bool = False
    localize: bool = True


class ImportManager(ABC):
    @abstractmethod
    def handle_data(self, data: list | dict, options: Options) -> None:
        """Handle the data with the options."""
