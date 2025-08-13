import re
import requests


class CheckerError(Exception):
    pass


def check_url(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        status_code = response.status_code
        html = response.text

        h1_match = re.search(
            r"<h1[^>]*>(.*?)</h1>",
            html,
            re.DOTALL | re.IGNORECASE,
        )
        h1 = h1_match.group(1).strip() if h1_match else ""

        title_match = re.search(
            r"<title[^>]*>(.*?)</title>",
            html,
            re.DOTALL | re.IGNORECASE,
        )
        title = title_match.group(1).strip() if title_match else ""

        desc_match = re.search(
            r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']',
            html,
            re.IGNORECASE,
        )
        description = desc_match.group(1) if desc_match else ""

        return status_code, h1, title, description

    except requests.RequestException as err:
        raise CheckerError from err
