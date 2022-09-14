class DateRange:

  def __init__(self, year, month):
    self.current_year = year
    self.last_year = str(int(self.current_year) - 1)
    self.next_year = str(int(self.current_year) + 1)
    self.date_ranges = {
      "01": (f"12/31/{self.last_year}", f"02/01/{self.current_year}"),
      "02": (f"01/31/{self.current_year}", f"03/01/{self.current_year}"),
      "03": (f"02/29/{self.current_year}", f"04/01/{self.current_year}"),
      "04": (f"03/31/{self.current_year}", f"05/01/{self.current_year}"),
      "05": (f"04/30/{self.current_year}", f"06/01/{self.current_year}"),
      "06": (f"05/31/{self.current_year}", f"07/01/{self.current_year}"),
      "07": (f"06/30/{self.current_year}", f"08/01/{self.current_year}"),
      "08": (f"07/31/{self.current_year}", f"09/01/{self.current_year}"),
      "09": (f"08/31/{self.current_year}", f"10/01/{self.current_year}"),
      "10": (f"09/30/{self.current_year}", f"11/01/{self.current_year}"),
      "11": (f"10/31/{self.current_year}", f"12/01/{self.current_year}"),
      "12": (f"11/30/{self.current_year}", f"01/01/{self.next_year}")
    }
    self.month = month
    self.month_begin = self.date_ranges[self.month][0]
    self.month_end = self.date_ranges[self.month][1]
