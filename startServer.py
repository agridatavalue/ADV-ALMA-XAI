import os
import logging
import colorlog
import argparse
from dotenv import load_dotenv
from os.path import dirname

from server.server import ServiceServer

load_dotenv()


def main():
    parser = argparse.ArgumentParser(description="ADV-XAI Fulfilment")

    parser.add_argument(
        "-LEVEL",
        "-l",
        choices=["INFO", "DEBUG", "INFO"],
        default="INFO",
        required=False,
    )
    parser.add_argument(
        "-ENV", "-e", choices=["DEV", "PROD"], default="DEV", required=False
    )
    args = parser.parse_args()

    log_format = "%(log_color)s%(levelname)s %(asctime)s - %(message)s"
    log_colors = {
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "bold_red",
    }

    # Set up the formatter with colors
    formatter = colorlog.ColoredFormatter(log_format, log_colors=log_colors)

    # Create a stream handler
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    # Configure the root logger
    logging.basicConfig(
        level=getattr(logging, args.LEVEL.upper(), None),
        handlers=[handler],
    )
    logging.info(f"starting with environment {args.ENV} and log level {args.LEVEL}")

    app = ServiceServer(__name__, dirname(__file__))
    app.setConfiguration(dict(os.environ))
    app.run(
        os.getenv("SERVER_IP") or "0.0.0.0",
        os.getenv("SERVER_PORT") or 8000,
        args.LEVEL == "DEBUG",
    )


if __name__ == "__main__":
    main()
