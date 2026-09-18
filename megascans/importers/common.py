from __future__ import annotations

import logging
import os
import shutil
from collections.abc import Sequence

import hou
from component_builder import Geometry, Material

logger = logging.getLogger(__name__)

ComponentType = Material.ComponentType

CHANNELS = {
    'albedo': ComponentType.BASE_COLOR,
    'metalness': ComponentType.METALNESS,
    'roughness': ComponentType.SPECULAR_ROUGHNESS,
    'transmission': ComponentType.TRANSMISSION_COLOR,
    'translucency': ComponentType.SUBSURFACE_COLOR,
    'emission': ComponentType.EMISSION_COLOR,
    'opacity': ComponentType.OPACITY,
    'normal': ComponentType.NORMAL,
    'displacement': ComponentType.DISPLACEMENT,
}


def get_material(data: dict, localize: bool = False) -> Material:
    """Return the Material options from a data dictionary."""

    name = data['id']
    triplanar = data['triplanar']

    # Textures
    textures: dict[ComponentType, Material.TextureMap] = {}
    for component in data['components']:
        path = component['path']
        component_type = component['type']

        channel = CHANNELS.get(component_type)
        if channel is None:
            logger.warning(f'Could not map {component_type!r} to a channel.')
            continue

        if localize:
            path = localize_file(path)

        texture = Material.TextureMap(path=path)
        textures[channel] = texture

    # Material
    material = Material(name=name, textures=textures, triplanar=triplanar)

    return material


def get_geometry(data: dict, localize: bool = False) -> Geometry:
    """Return the Geometry options from a data dictionary."""

    mesh_list = data['meshList']
    if mesh_list:
        mesh = mesh_list[0]
        path = mesh['path']
        if localize:
            path = localize_file(path)
    else:
        path = ''
    geometry = Geometry(path=path, scale=0.01)
    return geometry


def get_current_node() -> hou.Node | None:
    """Return the Node of the active NetworkEditor."""

    current_pane = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
    if isinstance(current_pane, hou.NetworkEditor):
        return current_pane.pwd()
    return None


def get_bounding_box(nodes: Sequence[hou.NetworkMovableItem]) -> hou.BoundingRect:
    """Return the BoundingRect for Nodes."""

    bbox = hou.BoundingRect()
    for node in nodes:
        bbox.enlargeToContain(node.position())
        bbox.enlargeToContain(node.position() + node.size())
    return bbox


def layout_nodes(nodes: Sequence[hou.Node], margin: hou.Vector2 | None = None) -> None:
    """Lay out the nodes in an empty area of the NetworkEditor."""

    if not nodes:
        return

    if margin is None:
        margin = hou.Vector2(1, 0)

    parent = nodes[0].parent()
    if parent is None:
        return

    all_items = parent.allItems()
    existing_items = [item for item in all_items if item not in nodes]
    existing_bbox = get_bounding_box(existing_items)

    loaded_bbox = get_bounding_box(nodes)

    if existing_bbox.isValid():
        target_position = existing_bbox.max() + margin
        source_position = hou.Vector2(loaded_bbox.min().x(), loaded_bbox.max().y())
        offset = target_position - source_position
        for node in nodes:
            node.move(offset)


def localize_file(file: str, destination: str = '$HIP/source') -> str:
    """
    Localize the file to a destination.
    By default, localize into the directory containing the current scene file.
    """

    if not destination:
        raise ValueError(f'invalid destination: {destination!r}')

    normpath = os.path.normpath(os.path.expandvars(destination))
    source_dir_name = os.path.basename(os.path.dirname(file))
    target_dir = os.path.join(normpath, source_dir_name)

    # Copy
    logger.debug(f'Localizing file {file!r} to {target_dir!r} ...')
    os.makedirs(target_dir, exist_ok=True)
    destination_file = shutil.copy(file, target_dir)

    # Make relative
    project_dir = os.path.dirname(os.path.normpath(hou.hipFile.path()))
    path = destination_file.replace(project_dir, '$HIP')

    return path
