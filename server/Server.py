import os
from flask import Flask
from os.path import join
from flask_cors import CORS
from dotenv import load_dotenv
from swagger_ui import flask_api_doc

DEFAULT_LOG_LEVEL: str = "INFO"

load_dotenv()

from .endpoints import routes


class ServiceServer:
    _app: Flask
    _name: str
    _conf: dict = {}
    _level: str = DEFAULT_LOG_LEVEL
    _prefix: str = ""

    def __init__(self, name: str, FOLDER_PATH: str) -> None:
        self._name = name

        self.app = Flask(self._name)
        CORS(self.app)

        self._prefix: str = (
            f"/{os.getenv('SERVER_URI')}" if os.getenv("SERVER_URI") else ""
        )

        for route in routes:
            self.app.register_blueprint(route, url_prefix=self._prefix)

        flask_api_doc(
            self.app,
            config_spec=self._prepareSwaggerContent(FOLDER_PATH),
            url_prefix="/api/doc",
            title="API doc",
        )

        self._conf = {"FOLDER_PATH": FOLDER_PATH}

    def setConfiguration(self, conf: dict):
        assert isinstance(conf, dict), "Bad argument to setConfiguration method"
        self._conf = {**conf, **(self._conf or {})}

    def run(self, host: str, port: int, isDebugMode: bool = False):
        self.app.run(
            host=host,
            port=port,
            debug=isDebugMode,
        )

    def _prepareSwaggerContent(self, folderPath: str) -> str:
        swaggerContent = ""
        with open(join(folderPath, join("sources", "api.yaml")), "r") as swaggerFile:
            swaggerContent = swaggerFile.read()

        if not self._prefix:
            return swaggerContent

        for route in routes:
            swaggerContent = swaggerContent.replace(
                f"/{route.name}:", f"{self._prefix}/{route.name}:"
            )

        return swaggerContent
