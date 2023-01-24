from date_ranges import DateRange

# Give test input here:
YEAR = 2023
MONTH = 1

date_range = DateRange(year=YEAR, month=MONTH)
print("date_range.month_begin: ", date_range.month_begin)
print("date_range.next_month_begin: ", date_range.next_month_begin)

