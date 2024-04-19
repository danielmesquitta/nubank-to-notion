from notion_client import AsyncClient
import os
from datetime import datetime


class NotionClient:
  NOTION_TOKEN = os.getenv('NOTION_TOKEN')
  colors = ['gray', 'brown', 'orange',
            'yellow', 'green', 'blue', 'purple', 'pink', 'red']

  def __init__(self):
    self.notion = AsyncClient(auth=self.NOTION_TOKEN)

  def __gen_select_options(self, options: list[str]) -> list[dict]:
    options_list = []

    for index, option in enumerate(options):
      index = index % len(self.colors)
      options_list.append(
          {"name": option, "color": self.colors[index]})

    return options_list

  async def create_page(self, page_id: str, title: str) -> dict:
    new_page = await self.notion.pages.create(
        parent={"page_id": page_id},
        properties={
            "title": {
                "title": [
                    {
                        "text": {
                            "content": title
                        }
                    }
                ]
            }
        },
        icon={
            "type": "emoji",
            "emoji": "💵"
        },
    )

    return new_page

  async def create_financial_database(self, page_id: str, title: str, categories: list[str], payment_methods: list[str]) -> dict:
    category_options = self.__gen_select_options(categories)
    payment_method_options = self.__gen_select_options(payment_methods)

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
        },
        "Método de pagamento": {
            "select": {
                "options": payment_method_options
            }
        },
    }

    response = await self.notion.databases.create(
        parent={"page_id": page_id},
        icon={"type": "emoji", "emoji": "💵"},
        title=[{
            "type": "text",
            "text": {
                "content": title
            }
        }],
        properties=database_schema,
        is_inline=True
    )

    return response

  async def add_row_to_financial_database(
          self,
          database_id: str,
          date: datetime,
          name: str,
          price: float,
          category: str | None = None,
          payment_method: str | None = None
  ) -> dict:
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
            },
            "Método de pagamento": {
                "select": {
                    "name": payment_method
                }
            }
        }
    }

    if category is None:
      del new_page_data["properties"]["Categoria"]

    if payment_method is None:
      del new_page_data["properties"]["Método de pagamento"]

    response = await self.notion.pages.create(**new_page_data)

    return response
