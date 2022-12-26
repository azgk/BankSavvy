from eom import EOM

# Enter year and month here.
YEAR = 2022   # Year format: 4-digit year, integer.
MONTH = 7  # Month format: integer.
CSV_DIR = "csv_files"  # Drop your csv files in this directory.

# ACCT_INFO has unique .csv column headers used by each bank.
# uncommon_col: PNC has two columns for expenses/deposits instead of just one in other .csv files.
ACCT_INFO = {
  "PNC": {"acct_cols": ("Date", "Category", "Withdrawals", "Description"), "uncommon_col": "Deposits"},
  "Chase": {"acct_cols": ("Transaction Date", "Category", "Amount", "Description")},
  "Bank of America": {"acct_cols": ("Posted Date", "Category", "Amount", "Payee")},
  "Wells Fargo": {"acct_cols": ("Date", "Category", "Amount", "Description")},
}

eom = EOM(YEAR, MONTH, CSV_DIR, ACCT_INFO)
eom.tally_all_accts()
eom.print_acct_details()
