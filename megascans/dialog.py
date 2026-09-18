from __future__ import annotations

import logging

try:
    from PySide6 import QtGui, QtWidgets
except ImportError:
    from PySide2 import QtGui, QtWidgets

from .json_socket import JSONTCPServer
from .managers import ImportManager, Options, Renderer
from .qt_material_icons import MaterialIcon

logger = logging.getLogger(__name__)

dialog = None


class MegascansDialog(QtWidgets.QDialog):
    def __init__(
        self,
        import_manager: ImportManager,
        port: int = 13290,
        parent: QtWidgets.QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self._connected = False
        self._import_manager = import_manager
        self._port = port
        self._server = JSONTCPServer()
        self._server.data_received.connect(self._handle_data)

        self._init_ui()

    def _init_ui(self) -> None:
        self.setWindowTitle('Megascans')
        self.resize(360, 120)

        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        connection_layout = QtWidgets.QHBoxLayout()
        layout.addLayout(connection_layout)
        self.status_icon_label = QtWidgets.QLabel()
        connection_layout.addWidget(self.status_icon_label)
        self.status_text_label = QtWidgets.QLabel()
        connection_layout.addWidget(self.status_text_label)
        connection_layout.addStretch()

        # General
        general_group = QtWidgets.QGroupBox()
        general_group.setTitle('General')
        layout.addWidget(general_group)
        general_layout = QtWidgets.QFormLayout()
        general_group.setLayout(general_layout)

        self.renderer_combo = QtWidgets.QComboBox()
        self.renderer_combo.addItems(list(Renderer))
        general_layout.addRow('Renderer', self.renderer_combo)

        self.localize_check = QtWidgets.QCheckBox()
        self.localize_check.setChecked(True)
        general_layout.addRow('Localize Files', self.localize_check)

        # Surfaces
        surfaces_group = QtWidgets.QGroupBox()
        surfaces_group.setTitle('Surface')
        layout.addWidget(surfaces_group)
        surfaces_layout = QtWidgets.QFormLayout()
        surfaces_group.setLayout(surfaces_layout)

        self.triplanar_check = QtWidgets.QCheckBox()
        surfaces_layout.addRow('Triplanar', self.triplanar_check)

        layout.addStretch()

        button_layout = QtWidgets.QHBoxLayout()
        layout.addLayout(button_layout)
        button_layout.addStretch()
        self.connect_button = QtWidgets.QPushButton()
        self.connect_button.clicked.connect(self._connect_toggled)
        button_layout.addWidget(self.connect_button)

        self._refresh_status()

    def showEvent(self, event: QtGui.QShowEvent) -> None:
        super().showEvent(event)
        self.start()

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        self.stop()
        super().closeEvent(event)

    def start(self) -> None:
        """Start the TCP Server and listen on the port."""

        if not self._server.listen(port=self._port):
            logger.error(
                'Unable to listen on the port. Is another connection already running?'
            )
            return

        self._connected = True
        self._refresh_status()

    def stop(self) -> None:
        """Stop the TCP Server if it is running."""

        if self._server.isListening():
            self._server.close()

        self._connected = False
        self._refresh_status()

    def _connect_toggled(self) -> None:
        if self._connected:
            self.stop()
        else:
            self.start()

    def _refresh_status(self) -> None:
        """Refresh the status label."""

        if self._connected:
            icon = MaterialIcon('check_circle')
            color = QtGui.QColor('#98c379')
            pixmap = icon.pixmap(color=color)
            self.status_text_label.setText('Connected')
            self.status_icon_label.setPixmap(pixmap)
            self.connect_button.setText('Stop Connection')
        else:
            icon = MaterialIcon('circle')
            pixmap = icon.pixmap()
            self.status_text_label.setText('Disconnected')
            self.status_icon_label.setPixmap(pixmap)
            self.connect_button.setText('Start Connection')

    def _handle_data(self, data: list | dict) -> None:
        renderer = Renderer(self.renderer_combo.currentText())
        options = Options(
            renderer=renderer,
            triplanar=self.triplanar_check.isChecked(),
            localize=self.localize_check.isChecked(),
        )
        self._import_manager.handle_data(data, options)
