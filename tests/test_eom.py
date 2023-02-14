from eom import EndOfMonthFinance
ACCT_INFO = {
  "PNC": {"acct_cols": ("Date", "Category", "Withdrawals", "Description"), "uncommon_col": "Deposits"},
  "Chase": {"acct_cols": ("Transaction Date", "Category", "Amount", "Description")},
  "Bank of America": {"acct_cols": ("Posted Date", "Category", "Amount", "Payee")},
  "Wells Fargo": {"acct_cols": ("Date", "Category", "Amount", "Description")},
}
acct_and_fPath = {
  "Bank of America": "/Users/mrs.giri/PycharmProjects/Personal_EOM/tests/test_csv_files/Bank of America/August2022_6826.csv",
  "PNC": "/Users/mrs.giri/PycharmProjects/Personal_EOM/tests/test_csv_files/PNC/creditCardAccountActivityExport.csv",
}

eom = EndOfMonthFinance(year=2022, month=7, eom_month_dir="test_csv_files", acct_info=ACCT_INFO)


# Tests on eom.modify_df (read CSV into dataframe and process data)
def test_modify_df(**acct_and_fPath):
  modified_dfs = {}
  for acct, fPath in acct_and_fPath.items():
    modified_df = eom.modify_df(acct=acct, f_path=fPath)
    modified_dfs[acct] = modified_df
    print(f"{acct}_modified_df:\n", modified_df)
  return modified_dfs


modified_dfs = test_modify_df(**acct_and_fPath)

# Tests on eom.tally_one_file
def test_tally_one_file(**modified_dfs):
  accts_dicts = {}
  for acct, modified_df in modified_dfs.items():
    file_expenses, file_deposits = eom.tally_one_file(acct=acct, modified_df=modified_df)
    accts_dicts[acct] = {"file_expenses": file_expenses, "file_deposits": file_deposits}
    print(f"\n{acct}_file_dicts:\n", accts_dicts[acct])
  return accts_dicts


accts_dicts = test_tally_one_file(**modified_dfs)

# Tests on eom.tally_one_acct
def test_tally_one_acct(**acct_dicts):
  for acct in acct_dicts.keys():
    eom.tally_one_acct(acct)
    print(f"\n{acct}_attr_dict:\n", eom.acct_info[acct])


test_tally_one_acct(**accts_dicts)

# Tests on eom.tally_all_accts
eom.tally_all_accts()
print(f"\nSummary:\n", eom.summary)





