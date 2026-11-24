import hou

try:
    from PySide6 import QtCore
except ImportError:
    from PySide2 import QtCore

from .dialog import DEFAULT_PORT, MegascansDialog
from .logging_utils import configure_logging
from .managers.builder import BuilderImportManager

dialog = None


def show_dialog(port: int = DEFAULT_PORT) -> None:
    global dialog
    configure_logging()
    if dialog is None:
        import_manager = BuilderImportManager()
        dialog = MegascansDialog(import_manager=import_manager, port=port)
        dialog.setParent(hou.qt.mainWindow(), QtCore.Qt.WindowType.Tool)
    dialog.show()
