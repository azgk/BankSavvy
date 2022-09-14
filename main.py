from date_ranges import DateRange
from eom import EOM

# ________________Enter your bank information below____________________________
YEAR = 2022   # Year format: 4-digit year.
MONTH = "07"  # Month format: 2-digit month.
CSV_DIR = "csv_files"

# Enter account name and csv file column names of each expense account. Format:
# {bank_acct_1_name: {"acct_col": (column name for date, column name for category, column name for dollar amount,
#                                column name for description)},
#  bank_acct_2_name: {"acct_col": (.......)},
# }
# The column names should be given in the same order as shown above.
EXP_ACCT_INFO = {
  "Gringott Wizarding Bank": {"acct_col": ("Date", "Category", "Withdrawals", "Description")},
  "Citibank": {"acct_col": ("Transaction Date", "Category", "Amount", "Description")},
  "Duchess Credit Union": {"acct_col": ("Posted Date", "Category", "Amount", "Payee")},
  "Durmstrang Associated": {"acct_col": ("Date", "Category", "Amount", "Description")},
}

# Enter information of each deposit account. Format is the same as that for expense accounts.
# If an account has both expenses and deposits, the respective information should be entered into
# both EXP_ACCT_INFO and DEPO_ACCT_INFO.
DEPO_ACCT_INFO = {
  "Gringott Wizarding Bank": {"acct_col": ("Date", "Category", "Deposits", "Description")},
}

#__________________No need to edit the code below____________________________________________________________

eom = EOM(YEAR, MONTH, CSV_DIR, EXP_ACCT_INFO, DEPO_ACCT_INFO)