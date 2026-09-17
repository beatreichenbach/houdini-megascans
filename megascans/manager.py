import dataclasses
import json
import logging
from collections.abc import Sequence
from enum import StrEnum
from typing import Any

logger = logging.getLogger(__name__)


class Renderer(StrEnum):
    ARNOLD = 'Arnold'


@dataclasses.dataclass
class Options:
    renderer: Renderer = Renderer.ARNOLD
    triplanar: bool = False


class ImportManager:
    def __init__(self) -> None:
        # Delayed import to keep GUI decoupled
        from component_builder import ArnoldComponentBuilder, ComponentBuilder

        from .base import Importer
        from .importers import AssetImporter, SurfaceImporter

        self.builders: dict[str, ComponentBuilder] = {
            Renderer.ARNOLD: ArnoldComponentBuilder()
        }

        self.importers: dict[str, Importer] = {
            '3d': AssetImporter(),
            'surface': SurfaceImporter(),
        }

    def handle_data(self, data: Any) -> None:
        if not isinstance(data, Sequence):
            data = (data,)

        for d in data:
            self.import_data(d)

    def import_data(self, data: dict, options: Options) -> None:
        """Import the data using one of the available Importers."""

        logger.debug(options)
        logger.debug(json.dumps(data, indent=2))

        data_type = str(data.get('type', ''))
        importer = self.importers.get(data_type)
        if importer is None:
            logger.error(f'The asset type {data_type!r} is not supported.')
            return

        builder = self.builders.get(options.renderer)
        if builder is None:
            logger.error(f'The renderer {options.renderer.value} is not supported.')
            return

        data['triplanar'] = options.triplanar

        importer.import_data(data, builder)
