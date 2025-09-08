from .scraper import Scraping
from .indexer import Indexing

scraper = Scraping()
indexer = Indexing()

__all__ = ["scraper", "indexer"]