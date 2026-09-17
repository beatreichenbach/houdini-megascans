from __future__ import annotations

import json
import logging
from functools import partial

try:
    from PySide6 import QtCore, QtNetwork
except ImportError:
    from PySide2 import QtCore, QtNetwork


logger = logging.getLogger(__name__)


class JSONTCPServer(QtNetwork.QTcpServer):
    data_received = QtCore.Signal(object)

    def __init__(self, parent: QtCore.QObject | None = None) -> None:
        super().__init__(parent)

        self.newConnection.connect(self._handle_new_connection)

    def _handle_new_connection(self) -> None:
        """Handle new connections."""

        while self.hasPendingConnections():
            sock = self.nextPendingConnection()
            sock.readyRead.connect(partial(self._read_data, sock))
            sock.disconnected.connect(sock.deleteLater)

    def _read_data(self, sock: QtNetwork.QTcpSocket) -> None:
        """Read the data sent to the socket."""

        data = sock.readAll().data()
        # data = .decode('utf-8')
        try:
            obj = json.loads(data)
            self.data_received.emit(obj)
        except json.JSONDecodeError as e:
            logger.error('Failed to decode the data.', exc_info=e)

        try:
            sock.disconnectFromHost()
        except RuntimeError:
            # Already garbage collected
            pass
