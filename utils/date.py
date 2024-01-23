from datetime import datetime


def convert_str_to_datetime(date: str):
  """
  Convert ISO 8601 date string (in 'YYYY-MM-DDTHH:MM:SSZ' format) in datetime.

  Args:
  date (str): The ISO 8601 date string.

  Returns:
  datetime: The datetime instance.
  """
  return datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ')


def is_same_month(date: datetime | str, compare_date: datetime | str) -> bool:
  """
  Check if the given ISO 8601 date (in 'YYYY-MM-DDTHH:MM:SSZ' format) is in the current month.

  Args:
  date (datetime | str): The ISO 8601 date string or a datetime instance.
  compare_date (datetime | str): The ISO 8601 date string or a datetime instance.

  Returns:
  bool: True if the date is in the current month, False otherwise.
  """
  try:
    if isinstance(date, str):
      date = convert_str_to_datetime(date)

    if isinstance(compare_date, str):
      compare_date = convert_str_to_datetime(compare_date)

    return compare_date.year == date.year and compare_date.month == date.month
  except:
    return False


def format_date_to_month_and_year(date: datetime) -> str:
  return date.strftime("%b-%Y")


def get_monthly_dates(start_date: datetime, end_date: datetime):
  end_date = datetime.today()
  start_date = datetime(end_date.year - 1, end_date.month, 1)

  dates: list[datetime] = []

  current_year, current_month = start_date.year, start_date.month

  while (current_year < end_date.year) or (current_month <= end_date.month):
    dates.append(datetime(current_year, current_month, 1))
    current_month += 1
    if current_month > 12:
      current_month = 1
      current_year += 1

  return dates
