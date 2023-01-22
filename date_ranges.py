from datetime import datetime


class DateRange:

  def __init__(self, year, month):
    self.year = year
    self.month = month
    self.month_begin = datetime(year=self.year, month=self.month, day=1).strftime("%m/%d/%Y")
    try:
      self.next_month_begin = datetime(year=self.year, month=self.month + 1, day=1).strftime("%m/%d/%Y")
    except ValueError:
      # Exception is for Dec.
      self.next_month_begin = datetime(year=self.year + 1, month=1, day=1).strftime("%m/%d/%Y")
