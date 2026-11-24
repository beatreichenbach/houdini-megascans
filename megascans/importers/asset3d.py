import logging

import hou
from component_builder import Component, ComponentBuilder

from ..managers.base import Options
from . import base, common

logger = logging.getLogger(__name__)


class AssetImporter(base.Importer):
    def import_data(
        self, data: dict, builder: ComponentBuilder, options: Options
    ) -> None:
        """Import a Megascans 3d Asset into the stage."""

        stage = hou.node('/stage')
        assert isinstance(stage, hou.LopNetwork)

        asset_id = data['id']
        name = f'{hou.text.variableName(data["name"])}_{asset_id}'

        geometry = common.get_geometry(data, localize=options.localize)
        material = common.get_material(data, localize=options.localize)
        component = Component(
            name=name,
            geometry=geometry,
            material=material,
            custom_data={'tags': data['tags']},
        )
        nodes = builder.create_component(component=component, parent=stage)
        common.layout_nodes(nodes)

        logger.info('Successfully created Asset.')
