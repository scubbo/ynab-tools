import requests

from logging import getLogger
from pathlib import Path
from typing import Optional

BASE_URL = "https://api.ynab.com/v1"
LOGGER = getLogger(__name__)


class BaseClient:
    """
    Very basic client that just handles authentication and jsonifying response - no prebuilt methods for specific paths.
    """
    def __init__(self, session: Optional[requests.Session]=None):
        self.session = session if session else get_session()

    def get(self, path: str):
        LOGGER.debug(f'calling {path}')
        response = self.session.get(f'{BASE_URL}{path}').json()
        LOGGER.debug(response)
        return response


def get_session(token: Optional[str]=None) -> requests.Session:
    if not token:
        token_path = Path('.token')
        if not token_path.exists():
            raise Exception('Found no token file at path `.token`')
        token = token_path.read_text().strip()

    session = requests.session()
    session.headers.update({'Authorization': f'Bearer {token}'})
    return session
