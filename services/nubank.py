from pynubank import Nubank
import os
import asyncio
from datetime import datetime
import uuid
from typing import List


class Statement:
  id: uuid.UUID
  description: str
  title: str
  amount: int
  time: datetime


class NubankClient:
  def __init__(self):
    self.nu = Nubank()
    self.authenticate()

  def authenticate(self):
    refresh_token = os.getenv('NUBANK_REFRESH_TOKEN')
    if refresh_token:
      self.nu.authenticate_with_refresh_token(refresh_token, 'cert.p12')
    else:
      NUBANK_CPF = os.getenv('NUBANK_CPF')
      NUBANK_PASSWORD = os.getenv('NUBANK_PASSWORD')
      refresh_token = self.nu.authenticate_with_cert(
          NUBANK_CPF, NUBANK_PASSWORD, './cert.p12')
      print('NUBANK_REFRESH_TOKEN: ', refresh_token)

  def get_card_statements(self) -> List[Statement]:
    return self.nu.get_card_statements()

  def get_account_statements(self):
    response = self.nu.get_account_statements()
    return response

  async def get_statements(self):
    event_loop = asyncio.get_event_loop()

    card_statements_task = event_loop.run_in_executor(
        None, self.get_card_statements)
    account_statements_task = event_loop.run_in_executor(
        None, self.get_account_statements)

    card_statements, account_statements = await asyncio.gather(card_statements_task, account_statements_task)

    return card_statements, account_statements
