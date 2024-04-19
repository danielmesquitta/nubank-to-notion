from .notion import NotionClient
from .nubank import NubankClient
from .plot import PlotManager

notion = NotionClient()
nubank = NubankClient()
plot = PlotManager(notion.colors)

__all__ = [
    "notion",
    "nubank",
    'plot',
]
