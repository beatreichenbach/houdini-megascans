import dataclasses
import json
import logging

import hou
from component_builder import (
    ArnoldComponentBuilder,
    ComponentBuilder,
    KarmaComponentBuilder,
)

from ..importers import Importer
from ..importers.asset3d import AssetImporter
from ..importers.surface import SurfaceImporter
from .base import AssetType, ImportManager, Options, Renderer

logger = logging.getLogger(__name__)


class BuilderImportManager(ImportManager):
    """An implementation of the ImportManager that uses ComponentBuilders on import."""

    def __init__(self) -> None:
        self.builders: dict[Renderer, ComponentBuilder] = {
            Renderer.ARNOLD: ArnoldComponentBuilder(),
            Renderer.KARMA: KarmaComponentBuilder(),
        }

        self.importers: dict[AssetType, Importer] = {
            AssetType.ASSET_3D: AssetImporter(),
            AssetType.SURFACE: SurfaceImporter(),
        }

    def handle_data(self, data: list | dict, options: Options) -> None:
        """Handle the data with the options."""

        data_list = data if isinstance(data, list) else [data]
        for d in data_list:
            try:
                with hou.undos.group('Import Asset'):
                    self.import_data(d, options)
            except Exception as e:
                hou.undos.performUndo()
                logger.error('Failed to import data.', exc_info=e)

    def import_data(self, data: dict, options: Options) -> None:
        """Import the data using one of the available Importers."""

        logger.debug(options)
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(json.dumps(data, indent=2))

        data_type = str(data.get('type', ''))
        try:
            importer = self.importers[AssetType(data_type)]
        except (KeyError, ValueError):
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

        importer.import_data(
            data, builder, dataclasses.replace(options, localize=localize)
        )
