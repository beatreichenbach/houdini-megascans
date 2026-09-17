from __future__ import annotations

import dataclasses
from typing import Any


@dataclasses.dataclass
class ExportData:
    @dataclasses.dataclass
    class Meta:
        key: str
        name: str
        value: Any

    @dataclasses.dataclass
    class Component:
        path: str
        type: str
        resolution: str
        format: str
        name: str
        nameOverride: str
        colorSpace: str
        physicalSize: str

    @dataclasses.dataclass
    class Mesh:
        path: str
        type: str
        resolution: str
        format: str
        name: str
        nameOverride: str

    @dataclasses.dataclass
    class Lod:
        lod: str
        path: str
        name: str
        nameOverride: str
        lodObjectName: str
        format: str
        type: str

    message: str
    id: str
    name: str
    path: str
    guid: str
    type: str
    category: str
    exportAs: str

    resolution: str
    resolutionValue: int
    textureFormat: str
    meshFormat: str
    previewImage: str
    averageColor: str
    minLOD: str
    activeLOD: str
    workflow: str
    origin: str
    namingConvention: dict[str, str]
    folderNamingConvention: str
    mapNameOverride: dict[str, str]
    scriptFilePath: str | None = None
    version: int = 1
    meshVersion: int = 1
    tags: tuple[str, ...] = ()
    categories: tuple[str, ...] = ()
    isExternal: bool = False
    exportPath: str = ""
    meta: tuple[Meta, ...] = ()
    materials: tuple = ()
    textureSets: tuple = ()
    isModularAsset: bool = False
    components: tuple[Component, ...] = ()
    meshList: tuple[Mesh, ...] = ()
    packedTextures: tuple = ()
    lodList: tuple[Lod, ...] = ()
    components_billboard: tuple = ()
    isCustom: bool = False

