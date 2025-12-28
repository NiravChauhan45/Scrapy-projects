from datetime import datetime

# Input date string in "Oct 27" format and year separately
date_str = "Oct 27"
year = "2024"

# Combine date string with the year
full_date_str = f"{date_str} {year}"

# Parse the string into a datetime object
date_obj = datetime.strptime(full_date_str, "%b %d %Y")

# Convert the date into "27-10-2024" format
formatted_date = date_obj.strftime("%Y-%m-%d %X")

print(formatted_date)
