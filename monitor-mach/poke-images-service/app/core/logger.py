import logging
import os
from datetime import datetime

from app.core.config import settings


class LabFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        timestamp = datetime.fromtimestamp(record.created).isoformat(timespec="milliseconds")

        module = getattr(record, "lab_module", settings.SERVICE_NAME)
        api = getattr(record, "lab_api", "-")
        function = getattr(record, "lab_function", record.funcName)

        message = record.getMessage()

        return f"{timestamp} {module} {api} {function} {message}"


def get_logger() -> logging.Logger:
    logger = logging.getLogger(settings.SERVICE_NAME)

    if logger.handlers:
        return logger

    logger.setLevel(settings.LOG_LEVEL.upper())

    os.makedirs(os.path.dirname(settings.LOG_FILE), exist_ok=True)

    formatter = LabFormatter()

    file_handler = logging.FileHandler(settings.LOG_FILE, encoding="utf-8")
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


logger = get_logger()


def log_event(api: str, function: str, message: str, level: int = logging.INFO) -> None:
    logger.log(
        level,
        message,
        extra={
            "lab_module": settings.SERVICE_NAME,
            "lab_api": api,
            "lab_function": function,
        },
    )
