import asyncio
from services import notion, nubank
from datetime import datetime
import streamlit as st
from utils import get_monthly_dates, save_file, format_date_to_month_and_year
import os

NOTION_USERNAME = os.getenv("NOTION_USERNAME")


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

  if st.button("Enviar"):
    if file is None:
      st.error("Selecione um extrato bancário (.csv)")

    title = format_date_to_month_and_year(date)
    save_file(file, f"{title}.csv")

    statements, categories, payment_methods = await nubank.get_statements(date)

    financial_database = await notion.find_financial_database(title)
    if financial_database is None:
      financial_database = await notion.create_financial_database(title, categories, payment_methods)

    for statement in statements:
      await notion.add_row_to_financial_database(financial_database["id"], statement.datetime, statement.title, statement.price, statement.category, statement.payment_method)

    st.write(
        f"[Clique para abrir planilha](https://notion.so/{NOTION_USERNAME}/{financial_database['id']})")

    st.success("Planilha no Notion gerada com sucesso!")


if __name__ == '__main__':
  asyncio.run(main())
