from pynubank import Nubank
import os
import asyncio
from datetime import datetime
import uuid
from typing import List
import pandas as pd
from utils import is_same_month, format_date_to_month_and_year


class Statement:
  id: uuid.UUID
  title: str
  category: str
  payment_method: str
  price: float
  datetime: str

  def __init__(self, id: uuid.UUID, title: str, category: str, payment_method: str, price: float, datetime: str):
    self.id = id
    self.title = title
    self.category = category
    self.payment_method = payment_method
    self.price = price
    self.datetime = datetime


class NubankClient:
  NUBANK_REFRESH_TOKEN = os.getenv('NUBANK_REFRESH_TOKEN')
  NUBANK_CPF = os.getenv('NUBANK_CPF')
  NUBANK_PASSWORD = os.getenv('NUBANK_PASSWORD')

  def __init__(self):
    self.nu = Nubank()
    self.authenticate()

  def _get_category_from_account_statement(self, csv_account_statement: pd.Series) -> str | None:
    description: str = csv_account_statement["Descrição"]

    if "TAPAJOS EMPREENDIMENTOS IMOBILIARIOS LTDA" in description:
      return "Casa"
    if "RECEITA FEDERAL" in description:
      return "Imposto"

    return None

  def _get_payment_method_from_account_statement(self, csv_account_statement: pd.Series) -> str | None:
    description: str = csv_account_statement["Descrição"]

    if "Pix" in description:
      return "Pix"
    if "boleto" in description:
      return "Boleto"

    return None

  def _get_title_from_account_statement(self, csv_account_statement: pd.Series) -> str:
    description: str = csv_account_statement["Descrição"]
    return description.replace("Transferência enviada pelo Pix - ", "").replace("Pagamento de boleto efetuado - ", "")

  def _get_filtered_account_statements(self, account_statements: list[Statement]):
    not_allowed_titles = ["Aplicação RDB",
                          "Resgate RDB", "Pagamento de fatura"]

    filtered_account_statements: list[Statement] = []

    for account_statement in account_statements:
      if not (account_statement.title in not_allowed_titles):
        filtered_account_statements.append(account_statement)

    return filtered_account_statements

  def authenticate(self):
    if self.NUBANK_REFRESH_TOKEN:
      self.nu.authenticate_with_refresh_token(
          self.NUBANK_REFRESH_TOKEN, 'cert.p12')
    else:
      refresh_token = self.nu.authenticate_with_cert(
          self.NUBANK_CPF, self.NUBANK_PASSWORD, './cert.p12')
      self.NUBANK_REFRESH_TOKEN = refresh_token
      print('NUBANK_REFRESH_TOKEN: ', refresh_token)

  def get_card_statements(self, date: datetime) -> List[Statement]:
    card_statements = self.nu.get_card_statements()

    filtered_card_statements: List[Statement] = []

    for card_statement in card_statements:
      if (is_same_month(date, card_statement["time"])):
        filtered_card_statements.append(Statement(
            id=uuid.uuid4(),
            title=card_statement["description"],
            category=card_statement["title"].capitalize(),
            payment_method="Cartão de crédito",
            price=card_statement["amount"] / 100,
            datetime=card_statement["time"])
        )

    return filtered_card_statements

  def get_account_statements(self, date: datetime) -> List[Statement]:
    title = format_date_to_month_and_year(date)
    account_statements: List[Statement] = []

    cwd = os.getcwd()
    file_path = os.path.join(cwd, 'tmp', f"{title}.csv")
    csv_account_statements = pd.read_csv(file_path)

    for _, account_statement in csv_account_statements.iterrows():
      price = account_statement["Valor"] * -1
      if price > 0:
        title = self._get_title_from_account_statement(
            account_statement)
        category = self._get_category_from_account_statement(
            account_statement)
        payment_method = self._get_payment_method_from_account_statement(
            account_statement)
        id = uuid.uuid4()
        date = datetime.strptime(
            account_statement["Data"], "%d/%m/%Y").isoformat()

        account_statements.append(
            Statement(id, title, category, payment_method, price, date))

    account_statements = self._get_filtered_account_statements(
        account_statements)

    return account_statements

  async def get_statements(self, date: datetime):
    event_loop = asyncio.get_event_loop()

    card_statements_task = event_loop.run_in_executor(
        None, self.get_card_statements, date)
    account_statements_task = event_loop.run_in_executor(
        None, self.get_account_statements, date)

    card_statements, account_statements = await asyncio.gather(card_statements_task, account_statements_task)

    statements = [*card_statements, *account_statements]

    categories: list[str] = []
    payment_methods: list[str] = []

    for statement in statements:
      if statement.category is not None and statement.category not in categories:
        categories.append(statement.category)
      if statement.payment_method is not None and statement.payment_method not in payment_methods:
        payment_methods.append(statement.payment_method)

    categories.sort()
    payment_methods.sort()

    return statements, categories, payment_methods
