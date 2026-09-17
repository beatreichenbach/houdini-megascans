import logging
from unittest.mock import Mock

from PySide2 import QtWidgets

from megascans.dialog import MegascansDialog


def test_gui() -> None:
    app = QtWidgets.QApplication()

    import_manager = Mock()
    import_manager.handle_data.return_value = None
    import_manager.import_data.return_value = None
    dialog = MegascansDialog(import_manager)
    dialog.show()
    app.exec_()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    test_gui()
