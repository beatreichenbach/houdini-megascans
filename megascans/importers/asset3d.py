import logging

import hou
from component_builder import Component, ComponentBuilder

from . import base, common

logger = logging.getLogger(__name__)


class AssetImporter(base.Importer):
    def import_data(self, data: dict, builder: ComponentBuilder) -> None:
        """Import a Megascans 3d Asset into the stage."""

        stage = hou.node('/stage')
        assert isinstance(stage, hou.LopNode)

        asset_id = data['id']
        clean_name = data['name'].replace(' ', '')
        name = f'{clean_name}_{asset_id}'

        # Custom Data
        tags = data['tags']

        localize = data['localize']

        geometry = common.get_geometry(data, localize=localize)
        material = common.get_material(data, localize=localize)
        component = Component(
            name=name,
            geometry=geometry,
            material=material,
            custom_data={'tags': tags},
        )
        builder.create_component(component=component, parent=stage)

        logger.info('Successfully created Asset.')
