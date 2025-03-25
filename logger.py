import logging
import colorlog

def get_logger(level:str='') -> logging.Logger:
    """Returns a configured logger instance for the entire project."""
    log_format = "%(log_color)s%(levelname)s %(asctime)s - %(message)s"
    log_colors = {
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "bold_red",
    }

    formatter = colorlog.ColoredFormatter(log_format, log_colors=log_colors)

    # Create a logger
    logger = logging.getLogger("adv_logger")
    if not logger.hasHandlers():
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        if level:
            logger.setLevel(getattr(logging, level, None))
        logger.debug("Logger initialized")

    return logger 