import pandas
from date_ranges import DateRange
import locale
import glob
import pprint
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

TRANSACTION_TYPES = ("Deposits", "Expenses")


def convert_dollarStr(month_df=None, amount_col=None, uncommon_col="Deposits"):
  """
  Convert dollar amount from string to float if needed.
  :param month_df: A Pandas DataFrame (df) filtered for data from a particular month.
  :param amount_col: The header of dollar amount column in df.
  :param uncommon_col: A second column (if any) for dollar amount.
  :return: month_df: A modified month_df.
  """
  # Check if type of dollar amount is string.
  amount_is_str = False
  for index, row in month_df.iterrows():
    if pandas.isna(row[amount_col]):
      pass
    else:
      amount_is_str = isinstance(row[amount_col], str)
      break

  # Convert string to float.
  if amount_is_str:
    if uncommon_col is None:
      for index, row in month_df.iterrows():
        try:
          month_df.at[index, amount_col] = 0 - locale.atof(row[amount_col][1:])
        # Whenever "$" is used, Expense is often shown as positive in bank data. Thus making it negative so that it
        # matches the format/pattern of other bank data.
        except TypeError:  # When the cell is blank (NaN).
          pass
    else:
      for index, row in month_df.iterrows():
        if pandas.isna(row[amount_col]):
          month_df.at[index, uncommon_col] = locale.atof(row[uncommon_col][1:])
        else:
          month_df.at[index, amount_col] = -1 * locale.atof(row[amount_col][1:])

  return month_df


class EndOfMonthFinance:
  def __init__(self, year=None, month=None, eom_month_dir="csv_files", acct_info=None):
    self.year = year
    self.month = month
    self.month_dir = eom_month_dir
    self.acct_info = acct_info

    # Mapping category names in .csv to "standard" names (chosen for this project).
    self.category_ref = {
      "Healthcare": "Discretionary",
      "Health & Wellness": "Discretionary",
      "Auto + Gas": "Transportation",
      "Other Expenses": "Discretionary",
      "Travel": "Discretionary",
      "Bills & Utilities": "Utilities",
      "Food & Drink": "Restaurants",
      "Automotive": "Transportation",
      "Gas": "Transportation",
      "Misc": "Discretionary",
      "Cable + Phone": "Utilities",
      "Services + Supplies": "Utilities",
      "Personal + Family": "Rent",
    }

    self.summary = {
      "Deposits": {
        "Paychecks": 0,
        "Interest": 0,
        "Return": 0,
        "Miscellaneous": 0,
      },
      "Expenses": {
        "Groceries": 0,
        "Restaurants": 0,
        "Amazon": 0,
        "Target": 0,
        "Transportation": 0,
        "Utilities": 0,
        "Entertainment": 0,
        "Pets": 0,
        "Discretionary": 0,
        "Rent": 0
      }
    }

  def modify_df(self, f_path=None, acct=None):
    """
    Filter df by date then convert dollar amount from str to float.
    :param f_path: CSV file absolute path.
    :param acct: A bank account name.
    :return: modified_df (modified Pandas dataframe).
    """
    df = pandas.read_csv(f_path)
    date_col, category_col, amount_col, description_col = self.acct_info[acct]["acct_cols"]

    date_range = DateRange(self.year, self.month)
    month_begin, next_month_begin = date_range.month_begin, date_range.next_month_begin
    if self.month == 12:
      month_df = df[(df[date_col] >= month_begin)]  # Strings are compared so "12" would be the biggest number and not
      # smaller than "01" (Jan) of next year.
    else:
      month_df = df[(df[date_col] >= month_begin) & (df[date_col] < next_month_begin)]
    # The dataframe is filtered by date--rows with dates bigger than or equal to 1st date of the month AND dates
    # smaller than 1st date of the next month are extracted. (A bank CSV often contains data from multiple months,
    # since billing cycles often span across months. Thus the need for filtering.)
    self.acct_info[acct].setdefault("uncommon_col", None)  # Exception: when there is a second column for dollar
    # amount in .csv the second column also needs to have dollar strings converted to integers.
    modified_df = convert_dollarStr(month_df=month_df, amount_col=amount_col, uncommon_col=self.acct_info[acct]
                                    ["uncommon_col"])
    return modified_df

  def add_to_summary(self, acct=None):
    """
    Tally up data from all accounts to self.summary.
    :return: None.
    """
    for transaction_type in TRANSACTION_TYPES:
      transaction_dict = self.acct_info[acct][transaction_type][0]
      for key, value in transaction_dict.items():
        if key in self.summary[transaction_type]:
          self.summary[transaction_type][key] += value
        elif key in self.category_ref:  # Modify category names (change them to standardized ones).
          new_key = self.category_ref[key]
          self.summary[transaction_type].setdefault(new_key, 0)
          self.summary[transaction_type][new_key] += value
        elif transaction_type == "Expenses":
          self.summary[transaction_type]["Discretionary"] += value
        elif transaction_type == "Deposits":
            self.summary[transaction_type]["Miscellaneous"] += value

      self.acct_info[acct][transaction_type].append({"Total": self.get_total(transaction_dict)})

  def get_total(self, transaction_dict=None):
    """
    Calculate the total amount of expenses or deposits from one bank account.
    :param transaction_dict: dict (mapping categories to amounts) of expenses or deposits from one bank account.
    :return: total amount (float)
    """
    total = sum(transaction_dict.values())
    return total

  def read_keywords(self, row=None, description_col=None, category_col=None):
    """
    Rename categories based on keywords in transaction description.
    :param row: A row in Pandas dataframe.
    :param description_col: CSV file column header for description column.
    :param category_col: CSV file column header for description column.
    :return: renamed_category (string)
    """
    keywords_to_category = {
      "VENMO": "Discretionary",
      "AMZN": "Amazon",
      "TARGET": "Target",
      "DOG STOP": "Pets",
      "CHEWY": "Pets",
      "CREDIT CARD PMT": None,
      "AUTOMATIC PAYMENT": None,
      "TRANSFER": None,
    }
    for keyword, standard_category in keywords_to_category.items():
      if keyword in row[description_col]:
        renamed_category = standard_category
        break
    else:
      renamed_category = row[category_col]
      if renamed_category == "Transfers" or renamed_category == "Credit Card Payments":
        renamed_category = None
    return renamed_category

  def tally_one_file(self, modified_df=None, acct=None):
    """
    Tally expenses and deposits in a CSV file.
    :param modified_df: A Pandas dataframe filtered by date; any dollar amount in str converted to float.
    :return: A dict containing file_expenses (dict) and file_deposits (dict). Each file dict has categories mapped to
    dollar amounts (data from one file).
    """
    date_col, category_col, amount_col, description_col = self.acct_info[acct]["acct_cols"]  # Extract CSV column headers.
    file_expenses = {}
    file_deposits = {}
    # Determine category then tally numbers for each category.
    for (index, row) in modified_df.iterrows():
      this_category = self.read_keywords(row, description_col, category_col)
      if this_category is not None:  # The tally does not include rows for internal transfers (e.g. credit card
        # payments).
        if row[amount_col] < 0:  # For expenses (negative float).
          file_expenses[this_category] = file_expenses.setdefault(this_category, 0) + row[amount_col]
        elif row[amount_col] > 0:  # For credit card refund etc (positive float).
          file_deposits[this_category] = file_deposits.setdefault(this_category, 0) + row[amount_col]
        elif pandas.isna(row[amount_col]):  # Exception: PNC csv has one column for withdrawals and another for
          # deposits. For each row, one of these two columns is empty.
          uncommon_amount_col = self.acct_info[acct]["uncommon_col"]
          file_deposits[this_category] = file_deposits.setdefault(this_category, 0) + row[uncommon_amount_col]
    file_dicts = {"Expenses": file_expenses, "Deposits": file_deposits}
    return file_dicts

  def add_fileDict_to_attrDict(self, acct=None, file_dicts=None):
    """
    Add file dicts to class attribute, self.acct_info.
    :file_dicts: A dict containing file_expenses (dict) and file_deposits (dict).
    :return: None
    """
    for transaction_type, file_dict in file_dicts.items():
      for category, amount in file_dict.items():
        self.acct_info[acct][transaction_type][0][category] = self.acct_info[acct][transaction_type][0].setdefault\
                                                                (category, 0) + amount

  def tally_one_acct(self, acct=None):
    """
    Load CSV , modify data and then tally expenses/deposits from one bank account.
    :param acct: Account name.
    :param acct_cols: Headers of columns in .csv files.
    :return: acct_expenses(dict) and acct_deposits (dict)
    """
    self.acct_info[acct]["Expenses"] = [{}]
    self.acct_info[acct]["Deposits"] = [{}]

    for f_path in glob.glob(f"{self.month_dir}/{acct}/*"):
      # Modify csv data (filter by date, convert dollar amount from string to float)
      modified_df = self.modify_df(f_path, acct)
      file_dicts = self.tally_one_file(modified_df=modified_df, acct=acct)
      self.add_fileDict_to_attrDict(acct=acct, file_dicts=file_dicts)

  def tally_all_accts(self):
    """
    Tally expenses and deposits from all bank accounts.
    :return: None.
    """
    for acct, info in self.acct_info.items():
      self.tally_one_acct(acct)
      self.add_to_summary(acct=acct)

  def summary_df(self):
    """
    Creates a Pandas dataframe to display summary of all accounts.
    :return: A Pandas dataframe of summary.
    """
    for transaction_type in TRANSACTION_TYPES:
      print(f"\nSummary_{transaction_type}: ")
      self.summary[transaction_type].append({"Total": self.get_total(self.summary[transaction_type][0])})
      col_headers = ["Category", "Amount"]
      transaction_data = [[key, value] for key, value in self.summary[transaction_type][0].items()]
      transaction_data.append(["Total", self.summary[transaction_type][1]["Total"]])
      row_headers = list(self.summary[transaction_type][0].keys())
      row_headers.append("Total")
      index = [i for i in range(1, len(row_headers) + 1)]
      print(pandas.DataFrame(transaction_data, index=index, columns=col_headers))

  def print_summary(self):
    self.summary = {k: [v] for k, v in self.summary.items()}
    self.summary_df()

  def print_acct_details(self):
    pp = pprint.PrettyPrinter(indent=2)
    print("\nAccount Details\n")
    for acct, info in self.acct_info.items():
      for transaction_type in TRANSACTION_TYPES:
        print(f"{acct} {transaction_type}:")
        pp.pprint(info[f"{transaction_type}"])
      print("\n")
