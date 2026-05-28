import logging
import sys
from datetime import datetime


class StandardFormatter(logging.Formatter):
    """
    Log format required by Lab 10:
    {Fecha} {Modulo} {API} {Funcion} Message
    Example:
    2026-05-27 10:32:15 [SearchAPI] [POST /poke/search] [search_pokemon] Pokemon 'charizard' found
    """

    def format(self, record: logging.LogRecord) -> str:
        fecha = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        modulo = getattr(record, "modulo", record.name)
        api = getattr(record, "api", "SearchAPI")
        funcion = getattr(record, "funcName", "-")
        level = record.levelname
        message = record.getMessage()
        return f"{fecha} [{modulo}] [{api}] [{funcion}] [{level}] {message}"


def get_logger(module_name: str, api_name: str = "SearchAPI") -> logging.Logger:
    logger = logging.getLogger(module_name)

    if not logger.handlers:
        logger.setLevel(logging.DEBUG)

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(StandardFormatter())
        logger.addHandler(console_handler)

        # File handler — one log file per module
        file_handler = logging.FileHandler(f"logs/{module_name}.log", mode="a", encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(StandardFormatter())
        logger.addHandler(file_handler)

    return logger