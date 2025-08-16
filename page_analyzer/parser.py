# page_analyzer/parser.py

import requests
from bs4 import BeautifulSoup


class CheckerError(Exception):
    """Ошибка проверки страницы (сетевые/HTTP проблемы)."""

    pass


TIMEOUT = 10


def text_or_empty(node):
    if not node:
        return ""
    if hasattr(node, "get_text"):
        return node.get_text(strip=True)
    return str(node).strip()


def meta_content(soup, name):
    tag = soup.find("meta", attrs={"name": name})
    if tag and tag.has_attr("content"):
        content = tag.get("content", "")
        return content.strip()
    return ""


def check_url(url):
    try:
        response = requests.get(url, timeout=TIMEOUT)
        response.raise_for_status()
    except requests.RequestException as err:
        raise CheckerError from err

    soup = BeautifulSoup(response.text, "html.parser")

    h1 = text_or_empty(soup.find("h1"))
    title = text_or_empty(soup.title)
    description = meta_content(soup, "description")

    return response.status_code, h1, title, description
