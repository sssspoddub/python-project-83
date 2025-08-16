from bs4 import BeautifulSoup
import requests


class CheckerError(Exception):
    """Ошибка проверки страницы (сетевые/HTTP проблемы)."""
    pass

TIMEOUT = 10

def text_or_empty(node):
    return node.get_text(strip=True) if node else ''


def meta_content(soup, name):
    tag = soup.find('meta', attrs={'name': name})
    return tag.get('content', '').strip() if tag and tag.has_attr('content') else ''

def check_url(url):
    try:
        response = requests.get(url, timeout=TIMEOUT)
        response.raise_for_status()
    except requests.RequestException as err:
        raise CheckerError from err
    
    soup = BeautifulSoup(response.text, 'html.parser')
    h1 = text_or_empty(soup.find('h1'))
    title = text_or_empty(soup.title)
    description = meta_content(soup, 'description')
    return response.status_code, h1, title, description