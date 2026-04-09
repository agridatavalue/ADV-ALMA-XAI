import os
import logging
import colorlog
from logging.handlers import RotatingFileHandler

def get_logger(level: str = 'INFO') -> logging.Logger:
    """Configura un logger con colori in console e rotazione file."""
    
    logger = logging.getLogger("adv_logger")
    logger.propagate = False
    
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    logger.setLevel(numeric_level)

    if not logger.handlers:
        console_format = "%(log_color)s%(levelname)-8s %(asctime)s [%(funcName)s] - %(message)s"
        log_colors = {
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "bold_red",
        }
        console_formatter = colorlog.ColoredFormatter(console_format, log_colors=log_colors)

        file_format = "%(levelname)-8s %(asctime)s [%(funcName)s] - %(message)s"
        file_formatter = logging.Formatter(file_format)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

        if not os.path.exists("logs"):
            os.makedirs("logs")
            
        # maxBytes=5*1024*1024 (5MB), backupCount=5 (tiene gli ultimi 5 file)
        file_handler = RotatingFileHandler(
            "logs/app.log", 
            maxBytes=5_000_000, 
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

        logger.debug("Logger inizializzato correttamente")

    return logger