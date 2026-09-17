import json
import logging

import hou
from component_builder import ArnoldComponentBuilder, ComponentBuilder

from ..importers import Importer
from ..importers.asset3d import AssetImporter
from ..importers.surface import SurfaceImporter
from .base import ImportManager, Options, Renderer

logger = logging.getLogger(__name__)


class BuilderImportManager(ImportManager):
    """An implementation of the ImportManager that uses ComponentBuilders on import."""

    def __init__(self) -> None:
        self.builders: dict[str, ComponentBuilder] = {
            Renderer.ARNOLD: ArnoldComponentBuilder()
        }

        self.importers: dict[str, Importer] = {
            '3d': AssetImporter(),
            'surface': SurfaceImporter(),
        }

    def handle_data(self, data: list | dict, options: Options) -> None:
        """Handle the data with the options."""

        data_list = data if isinstance(data, list) else [data]
        for d in data_list:
            self.import_data(d, options)

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

        localize = options.localize
        if localize and hou.hipFile.isNewFile():
            logger.warning('File is not saved. Skipping localizing files.')
            localize = False

        data['triplanar'] = options.triplanar
        data['localize'] = localize

        importer.import_data(data, builder)
