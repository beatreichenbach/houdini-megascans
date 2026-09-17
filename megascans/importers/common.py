import logging

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


def get_material(data: dict) -> Material:
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

        texture = Material.TextureMap(path=path)
        textures[channel] = texture

    # Material
    material = Material(name=name, textures=textures, triplanar=triplanar)

    return material


def get_geometry(data: dict) -> Geometry:
    """Return the Geometry options from a data dictionary."""

    path = data['meshList'][0]
    geometry = Geometry(path=path, scale=0.01)
    return geometry
