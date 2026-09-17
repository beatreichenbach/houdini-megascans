import logging

import hou
from component_builder import ComponentBuilder

from . import base, common

logger = logging.getLogger(__name__)


class SurfaceImporter(base.Importer):
    default_library_name = 'megascans'

    def import_data(self, data: dict, builder: ComponentBuilder) -> None:
        """
        Import a Megascans Surface (Material) into the currently selected
        material library or the default one.
        """

        stage = hou.node('/stage')
        assert isinstance(stage, hou.LopNode)

        current_node = common.get_current_node()
        if current_node and current_node.type().name() == 'materiallibrary':
            parent = current_node
        elif lib := stage.node(self.default_library_name):
            parent = lib
        else:
            lib = stage.createNode('materiallibrary', self.default_library_name)
            lib.moveToGoodPosition()
            parent = lib
        assert isinstance(parent, hou.LopNode)

        localize = data['localize']
        material = common.get_material(data, localize=localize)
        material_node = builder.create_material(material=material, parent=parent)

        # Layout
        common.layout_nodes([material_node])

        logger.info('Successfully created Surface.')
