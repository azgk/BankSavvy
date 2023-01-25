from eom import EndOfMonthFinance
ACCT_INFO = {
  "PNC": {"acct_cols": ("Date", "Category", "Withdrawals", "Description"), "uncommon_col": "Deposits"},
  "Chase": {"acct_cols": ("Transaction Date", "Category", "Amount", "Description")},
  "Bank of America": {"acct_cols": ("Posted Date", "Category", "Amount", "Payee")},
  "Wells Fargo": {"acct_cols": ("Date", "Category", "Amount", "Description")},
}

eom = EndOfMonthFinance(year=2022, month=12, eom_month_dir="test_csv_files", acct_info=ACCT_INFO)

modified_df_BOA = eom.modify_df(f_path="/Users/mrs.giri/PycharmProjects/Personal_EOM/tests/test_csv_files/Bank of Ameri"
                                       "ca/December2022_6826.csv", acct="Bank of America")
print("modified_df_BOA:\n", modified_df_BOA)
# modified_df_PNC = eom.modify_df(f_path="/Users/mrs.giri/PycharmProjects/Personal_EOM/tests/test_csv_files/PNC/account"
                                       #"ActivityExport. SG.csv", acct="PNC")
# print(modified_df_PNC)
#TODO: continue from here. test out tally one file, tally one account, tally all account. add comments/heading to this.
#TODO: organize/modify test files.
#TODO: update all methods to use kwargs.
#TODO: make a PR for review.
