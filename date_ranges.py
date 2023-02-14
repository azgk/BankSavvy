from datetime import datetime


class DateRange:

  def __init__(self, year: int = None, month: int = None):
    self.year = year
    self.month = month
    self.month_begin = datetime(year=self.year, month=self.month, day=1)
    try:
      self.next_month_begin = datetime(year=self.year, month=self.month + 1, day=1)
    except ValueError:
      # Exception is for Dec.
      self.next_month_begin = datetime(year=self.year + 1, month=1, day=1)
