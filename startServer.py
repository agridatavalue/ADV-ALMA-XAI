import os
import argparse
from dotenv import load_dotenv
from os.path import dirname

from logger import get_logger
from server.server import ServiceServer

load_dotenv()


def main():
    parser = argparse.ArgumentParser(description="ADV-XAI Fulfilment")

    parser.add_argument(
        "-LEVEL",
        "-l",
        choices=["INFO", "DEBUG"],
        default="INFO",
        required=False,
    )
    args = parser.parse_args()

    logger = get_logger(level=args.LEVEL.upper())

    logger.info(f"starting with log level {args.LEVEL}")

    app = ServiceServer(__name__, dirname(__file__))
    app.setConfiguration(dict(os.environ))
    
    app.run(
        os.getenv("SERVER_IP") or "0.0.0.0",
        os.getenv("SERVER_PORT") or 8000,
        isDevMode=os.getenv('DEVELOPMENT_MODE'),
    )


if __name__ == "__main__":
    main()
