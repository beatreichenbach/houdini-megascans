import logging

from PySide2 import QtWidgets

from megascans.gui import MegascansDialog


def test_gui() -> None:
    app = QtWidgets.QApplication()
    dialog = MegascansDialog()
    dialog.show()
    app.exec_()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    test_gui()
