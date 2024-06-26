import os
import logging
import argparse
from dotenv import load_dotenv
from os.path import dirname

from server.Server import ServiceServer

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

    logging.basicConfig(
        level=getattr(logging, args.LEVEL.upper(), None),
        format="%(levelname)s %(asctime)s - %(message)s",
        encoding="utf-8",
    )
    logging.info(f"starting with environment {args.ENV} and log level {args.LEVEL}")

    app = ServiceServer(__name__, dirname(__file__))
    app.setConfiguration(dict(os.environ))
    app.run(
        os.getenv("SERVER_IP") or "localhost",
        os.getenv("SERVER_PORT") or 8000,
        args.LEVEL == "DEBUG",
    )


if __name__ == "__main__":
    main()
