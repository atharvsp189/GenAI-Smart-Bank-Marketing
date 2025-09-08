import requests
from bs4 import BeautifulSoup
from typing import List
from langchain_community.document_loaders import WebBaseLoader

import nest_asyncio

nest_asyncio.apply()

class Scraping:
    def __init__(self):
        pass

    def get_all_links(self, url: str) -> List[str]:
        """Get all the embedded links on a webpage"""
        # Fetch the page
        response = requests.get(url)
        response.raise_for_status()  # raise error if request failed
        # Parse HTML
        soup = BeautifulSoup(response.text, "html.parser")
        # Extract all <a> tags with href
        links = [a["href"] for a in soup.find_all("a", href=True)]
        return links

    def is_reachable_url(self, url: str) -> bool:
        try:
            response = requests.head(url, allow_redirects=True, timeout=5)
            return response.status_code < 400  # 2xx or 3xx considered valid
        except requests.RequestException:
            return False

    def load_webpage(self, urls: List[str]):
        """Loads the webpage into langchain document object"""
        loader = WebBaseLoader(urls)
        loader.requests_per_second = 1
        docs = loader.aload()

        return docs