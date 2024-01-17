from notion_client import AsyncClient
import os
from datetime import datetime


class NotionClient:
  NOTION_TOKEN = os.getenv('NOTION_TOKEN')
  notion_colors = ['gray', 'brown', 'orange',
                   'yellow', 'green', 'blue', 'purple', 'pink', 'red']

  def __init__(self):
    self.notion = AsyncClient(auth=NotionClient.NOTION_TOKEN)

  @staticmethod
  def generate_financial_database_title():
    current_date = datetime.now()
    return current_date.strftime("%b/%Y")

  async def create_financial_database(self, categories: list[str]) -> dict:
    page_id = "2c19ae4a-c6ca-400d-b59a-37f1f1fe6ba9"
    category_options = []

    for index, category in enumerate(categories):
      index = index % len(NotionClient.notion_colors)
      category_options.append(
          {"name": category, "color": NotionClient.notion_colors[index]})

    database_schema = {
        "Data": {
            "date": {}
        },
        "Nome": {
            "title": {}
        },
        "Preço": {
            "number": {}
        },
        "Categoria": {
            "select": {
                "options": category_options
            }
        }
    }

    title = self.generate_financial_database_title()

    response = await self.notion.databases.create(
        parent={"page_id": page_id},
        icon={"type": "emoji", "emoji": "💵"},
        title=[{
            "type": "text",
            "text": {
                "content": title
            }
        }],
        properties=database_schema
    )

    return response

  async def add_row_to_financial_database(self, database_id: str, date: datetime, name: str, price: float, category: str) -> dict:
    new_page_data = {
        "parent": {"database_id": database_id},
        "properties": {
            "Data": {
                "date": {
                    "start": date
                }
            },
            "Nome": {
                "title": [
                    {
                        "type": "text",
                        "text": {"content": name}
                    }
                ]
            },
            "Preço": {
                "number": price
            },
            "Categoria": {
                "select": {
                    "name": category
                }
            }
        }
    }

    response = await self.notion.pages.create(**new_page_data)

    return response

  async def find_financial_database(self) -> dict | None:
    title = self.generate_financial_database_title()
    response = await self.notion.search(query=title)
    results: list = response["results"]

    if results and len(results) > 0:
      for result in results:
        if result["object"] == "database" and result["archived"] == False:
          return result

    return None
