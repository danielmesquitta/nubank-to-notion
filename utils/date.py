from datetime import datetime


def is_date_in_current_month(date: str) -> bool:
  """
  Check if the given ISO 8601 date (in 'YYYY-MM-DDTHH:MM:SSZ' format) is in the current month.

  Args:
  iso_date_str (str): The ISO 8601 date string.

  Returns:
  bool: True if the date is in the current month, False otherwise.
  """
  try:
    input_date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ')
    current_date = datetime.now()
    return input_date.year == current_date.year and input_date.month == current_date.month
  except:
    return False
