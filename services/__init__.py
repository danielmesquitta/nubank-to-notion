from .notion import NotionClient
from .nubank import NubankClient

notion = NotionClient()
nubank = NubankClient()

__all__ = [
    "notion",
    "nubank",
]
