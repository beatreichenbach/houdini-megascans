import logging

import hou


class HoudiniStatusHandler(logging.Handler):
    """Forward warnings and errors to the Houdini status bar."""

    def emit(self, record: logging.LogRecord) -> None:
        if record.levelno >= logging.ERROR:
            severity = hou.severityType.Error
        else:
            severity = hou.severityType.Warning
        hou.ui.setStatusMessage(record.getMessage(), severity=severity)


def configure_logging() -> None:
    """Install the status handler on the package logger, once."""

    logger = logging.getLogger(__package__)
    if any(isinstance(h, HoudiniStatusHandler) for h in logger.handlers):
        return
    handler = HoudiniStatusHandler()
    handler.setLevel(logging.WARNING)
    logger.addHandler(handler)
