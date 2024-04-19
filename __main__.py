import asyncio
from services import notion, nubank, plot
from services.plot import PieChartDataItem
from datetime import datetime
import streamlit as st
from utils import get_monthly_dates, save_file, format_date_to_month_and_year
import os

NOTION_USERNAME = os.getenv("NOTION_USERNAME")
NOTION_PAGE_ID = os.getenv('NOTION_PAGE_ID')


async def main():
  today = datetime.today()
  min_date = datetime(2023, 1, 1)
  monthly_dates = get_monthly_dates(today, min_date)
  monthly_dates.reverse()

  date = st.selectbox(
      "Selecione um mês",
      monthly_dates,
      format_func=format_date_to_month_and_year
  )

  file = st.file_uploader("Selecione o extrato bancário (.csv)", type="csv")

  if not st.button("Enviar"):
    return

  if file is None:
    return st.error("Selecione um extrato bancário (.csv)")

  title = format_date_to_month_and_year(date)
  save_file(file, f"{title}.csv")

  statements, categories, payment_methods = await nubank.get_statements(date)

  page = await notion.create_page(NOTION_PAGE_ID, title)

  financial_database = await notion.create_financial_database(page["id"], title, categories, payment_methods)

  price_sum_by_category = {}
  price_sum_by_payment_method = {}

  for statement in statements:
    await notion.add_row_to_financial_database(financial_database["id"], statement.datetime, statement.title, statement.price, statement.category, statement.payment_method)

    price_sum_by_category[statement.category] = price_sum_by_category.get(
        statement.category, 0) + statement.price

    price_sum_by_payment_method[statement.payment_method] = price_sum_by_payment_method.get(
        statement.payment_method, 0) + statement.price

  plot.pie(f"{title}-Category", [
      PieChartDataItem(category, price)
      for category, price in price_sum_by_category.items()
  ])

  plot.pie(f"{title}-Payment-method", [
      PieChartDataItem(payment_method, price)
      for payment_method, price in price_sum_by_payment_method.items()
  ])

  page_id = page["id"].replace("-", "")

  st.write(
      f"[Clique para abrir planilha](https://notion.so/{NOTION_USERNAME}/{page_id})")

  st.success("Planilha no Notion gerada com sucesso!")


if __name__ == '__main__':
  asyncio.run(main())
