import pandas as pd
from workalendar.europe import France  # Adjust the region/calendar as needed
from datetime import date, timedelta, datetime

# Read the existing CSV file
df = pd.read_csv("C:/Users/Florent/WebEnvironment/RedenSolar/DataStorage/joursOuvrees.csv")

# Get the last date in the existing data
last_date = df['Date'].iloc[-1]

# Convert the last date to a datetime object
date_format = "%Y-%m-%d"
last_date_object = datetime.strptime(last_date, date_format).date()  # Convert to date object

# Define the end date (adjust as needed)
end_date = date(2024, 10, 30)

# Generate a list of dates from the last date to the end date
date_list = [last_date_object + timedelta(days=x) for x in range((end_date - last_date_object).days + 1)]

# Initialize the calendar
cal = France()

# Create a DataFrame with date and is_day_off columns
newData = pd.DataFrame({'Date': date_list})
newData['IsDayOff'] = newData['Date'].apply(lambda x: not cal.is_working_day(x))

# Concatenate the existing data and the new data
result = pd.concat([df, newData], ignore_index=True)

# Save the result to a new CSV file
result.to_csv('C:/Users/Florent/WebEnvironment/RedenSolar/DataStorage/joursOuvrees.csv', index=False)
