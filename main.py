from date_ranges import DateRange
from eom import EOM

# ________________Enter your bank information below____________________________
YEAR = 2022   # Year format: 4-digit year, integer.
MONTH = 7  # Month format: integer.
CSV_DIR = "csv_files"

# Enter account name and csv file column names of each expense account. Format:
# {bank_acct_1_name: {"acct_col": (column name for date, column name for category, column name for dollar amount,
#                                column name for description)},
#  bank_acct_2_name: {"acct_col": (.......)},
# }
# The column names should be given in the same order as shown above.
ACCT_INFO = {
  "Gringott Wizarding Bank": {"acct_cols": ("Date", "Category", "Withdrawals", "Description"), "uncommon_col": "Deposits"},
  "Citibank": {"acct_cols": ("Transaction Date", "Category", "Amount", "Description")},
  "Duchess Credit Union": {"acct_cols": ("Posted Date", "Category", "Amount", "Payee")},
  "Durmstrang Associated": {"acct_cols": ("Date", "Category", "Amount", "Description")},
}

#__________________No need to edit the code below____________________________________________________________

eom = EOM(YEAR, MONTH, CSV_DIR, ACCT_INFO)
eom.tally_all_accts()
eom.print_acct_details()
