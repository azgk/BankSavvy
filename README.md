<img alt="Image of a notebook" src="/background.png" title="background image" width="80%"/>
# Personal EOM

## Introduction

Do you and your spouse have too many credit cards to keep track of? Are you tired of tracking expenses across various banks and accounts? Are you wary of sharing your online banking passwords with 3rd party apps? 
Personal EOM (End of Month) can crunch all the numbers for you so you can easily see where your money is coming and going. 

## Features

Personal EOM analyzes transaction data to provide a breakdown of expenses/deposits under different categories (e.g. groceries, restaurants, paychecks). Expenses/Deposits summaries are created for each bank account as well as for all bank accounts. 

## Prepare Transaction Records (.csv)
1. Download transaction records (i.e. account activities) from your online banking portals. Make sure the format is .csv. If not available, download in a format that can be easily converted to .csv (such as .xlsx). 
2. Wells Fargo, Bank of America .csv do not have headers and/or categories, which need to be manually added. For earlier transactions, PNC .csv also may not have categories. For standard names, see main.py and eom.py.

## How to Use Personal EOM
1. Drop your .csv into sub folders of "**csv_files**", organized by bank account. 
2. In main.py, enter YEAR and MONTH. 
3. Run the program.

## Program Output
<img alt="A screenshot of program output (deposits summary) example." src="program output/program_output_summary_dep.png" title="Program Output(deposits summary)" width="50%"/>
<img alt="A screenshot of program output (expenses summary) example." src="program output/program_output_summary_exp.png" title="Program Output(expenses summary)" width="50%"/>
<img alt="A screenshot of program output (acct detail) example." src="program output/program_output_acct_details.png" title="Program Output(acct details)" width="80%"/>

## Caveat
1. Personal EOM has been tested for debit and credit accounts from the four banks mentioned above. It may not work with accounts from other banks or special accounts such as a money market account. 
2. This program does not analyze internal transfers e.g. transfers between two accounts under your name. 
3. This program calculates recurring external transfers like those via Venmo. But it may not capture one-time transfer such as a donation made via PayPal. It also does not capture information on investment (treated as internal transfers).
4. Try not to edit .csv files except for adding column headers or editing category names. Otherwise, there could be bugs.



