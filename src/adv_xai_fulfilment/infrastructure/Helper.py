from os.path import exists
from urllib.parse import urlparse


class Helper:
    @staticmethod
    def is_local_path(url: str) -> bool:
        url_parsed = urlparse(url)
        if url_parsed.scheme in ("file", ""):  # Possibly a local file
            return exists(url_parsed.path)
        return False
