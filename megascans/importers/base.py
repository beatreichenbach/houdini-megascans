from abc import ABC, abstractmethod

from component_builder import ComponentBuilder


class Importer(ABC):
    @abstractmethod
    def import_data(self, data: dict, builder: ComponentBuilder) -> None:
        """Import the data from the Megascans Bridge export."""
