import re
import requests


class CheckerError(Exception):
    """Ошибка проверки страницы (сетевые/HTTP проблемы)."""


_FLAGS = re.IGNORECASE | re.DOTALL

_H1_RE = r"<h1[^>]*>(.*?)</h1>"
_TITLE_RE = r"<title[^>]*>(.*?)</title>"
_DESC_RE = r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']'


def _first_match(pattern: str, text: str) -> str:
    matches = re.findall(pattern, text, flags=_FLAGS)
    return matches[0].strip() if matches else ""


def check_url(url: str):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as err:
        raise CheckerError from err

    html = response.text
    status_code = response.status_code

    h1 = _first_match(_H1_RE, html)
    title = _first_match(_TITLE_RE, html)
    description = _first_match(_DESC_RE, html)

    return status_code, h1, title, description
