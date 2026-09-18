import hou

try:
    from PySide6 import QtCore
except ImportError:
    from PySide2 import QtCore

from .dialog import MegascansDialog
from .managers.builder import BuilderImportManager

dialog = None


def show_dialog(port: int = 13290) -> None:
    global dialog
    if dialog is None:
        import_manager = BuilderImportManager()
        dialog = MegascansDialog(import_manager=import_manager, port=port)
        dialog.setParent(hou.qt.mainWindow(), QtCore.Qt.WindowType.Tool)
    dialog.show()
