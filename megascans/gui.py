import logging

import hou

try:
    from PySide6 import QtCore
except ImportError:
    from PySide2 import QtCore

from .dialog import MegascansDialog, logger
from .managers.builder import BuilderImportManager

dialog = None


def show_dialog() -> None:
    global dialog
    if dialog is None:
        logger.setLevel(logging.INFO)
        import_manager = BuilderImportManager()
        dialog = MegascansDialog(import_manager=import_manager)
        dialog.setParent(hou.qt.mainWindow(), QtCore.Qt.WindowType.Tool)
    dialog.show()
