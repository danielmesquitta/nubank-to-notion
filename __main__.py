import asyncio
from services import notion, nubank
import utils


async def main():
  cards = nubank.get_card_statements()

  financial_database = await notion.find_financial_database()
  if financial_database is None:
    titles: list[str] = []

    for card in cards:
      card["title"] = str(card["title"]).capitalize()
      titles.append(card["title"])

    unique_titles = list(set(titles))
    unique_titles.sort()

    financial_database = await notion.create_financial_database(unique_titles)

  for card in cards:
    if utils.is_date_in_current_month(card["time"]):
      await notion.add_row_to_financial_database(financial_database["id"], card["time"], card["description"], card["amount"] / 100, card["title"])


if __name__ == '__main__':
  asyncio.run(main())
