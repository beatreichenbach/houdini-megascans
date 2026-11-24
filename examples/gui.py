import logging
from unittest.mock import Mock

try:
    from PySide6 import QtWidgets
except ImportError:
    from PySide2 import QtWidgets

from megascans.dialog import MegascansDialog


def main() -> None:
    app = QtWidgets.QApplication()

    import_manager = Mock()
    dialog = MegascansDialog(import_manager)
    dialog.show()

    exec_method = getattr(app, 'exec', app.exec_)
    exec_method()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()
