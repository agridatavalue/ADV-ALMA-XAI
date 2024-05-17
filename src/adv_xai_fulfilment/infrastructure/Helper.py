from os.path import exists, abspath
from urllib.parse import urlparse


class Helper:
    @staticmethod
    def is_local_path(destination: str) -> bool:
        if exists(destination) or exists(abspath(destination)):
            return True

        # check if the param is an url
        url_parsed = urlparse(destination)
        if url_parsed.scheme in ("file", ""):  # Possibly a local file
            return exists(url_parsed.path)
        return False
