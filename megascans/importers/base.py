from abc import ABC, abstractmethod

from component_builder import ComponentBuilder

from ..managers.base import Options


class Importer(ABC):
    @abstractmethod
    def import_data(
        self, data: dict, builder: ComponentBuilder, options: Options
    ) -> None:
        """Import the data from the Megascans Bridge export."""
