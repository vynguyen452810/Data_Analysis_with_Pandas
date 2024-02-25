"""
Title: DoorDash Deliveries Insights

# df_deliveries
| order_id | delivery_date | delivery_time | customer_id | total_price |
|----------|---------------|---------------|-------------|-------------|
| D101     | 2023-05-01    | 12:15 PM      | C001        | 24.99       |
| D102     | 2023-05-01    | 1:05 PM       | C002        | 39.99       |
| D103     | 2023-05-02    | 7:45 PM       | C003        | 15.49       |
| D104     | 2023-05-02    | 8:10 PM       | C001        | 29.99       |
| D105     | 2023-05-03    | 2:00 PM       | C004        | 19.99       |
| D106     | 2023-05-03    | 2:45 PM       | C005        | 49.99       |
| D107     | 2023-05-04    | 6:30 PM       | C006        | 34.99       |
| D108     | 2023-05-05    | 7:00 PM       | C001        | 44.99       |
| D109     | 2023-05-05    | 8:15 PM       | C007        | 54.99       |

# df_customers
| customer_id | name | age | country | joined_since |
|-------------|------|-----|---------|--------------|
| C001        | Ana  | 28  | US      | 2019-01-15   |
| C002        | Ben  | 34  | CA      | 2020-03-20   |
| C003        | Cam  | 29  | UK      | 2021-04-10   |
| C004        | Dan  | 31  | AU      | 2018-06-05   |
| C005        | Elle | 25  | NZ      | 2019-09-17   |
| C006        | Fay  | 30  | US      | 2017-11-07   |
| C007        | Greg | 35  | IN      | 2022-01-01   |

### Questions

1. Calculate the total revenue earned by DoorDash for each day. Then, sort the output based on 
the descending order of revenue.

2. For each customer, determine the average total_price of their orders. Include customers with no order,
and set their average total_price as 0. Then sort it based on the acending order of average price. Output
their name, age, country, and average price, but not the customer_id.

3. Which customers have made at least 2 orders within 72 hours of each other?

4. In each country, list the customer who had the highest order amount ($). 
Return the country, name, age, and total order amount.
"""

### Solution ###

import pandas as pd

# Get data
df_customers = pd.read_csv('./Data/DoorDash/customers.csv')
df_deliveries = pd.read_csv('./Data/DoorDash/deliveries.csv')

# 1. Calculate the total revenue earned by DoorDash for each day.

# Convert delivery_date to datetime 
df_output = (
	df_deliveries
		.groupby('delivery_date') # Group by on delivery date
		['total_price'].sum()     # Aggregate-sum on price
		.sort_values(ascending=False) # Sort on the descending order of price
)

print(df_output)

# 2. For each customer, determine the average total_price of their orders. Include customers with no order,
# and set their average total_price as 0. Then sort it based on the acending order of average price. Output
# their name, age, country, and average price, but not the customer_id.

df_output = (
	df_deliveries
		# Apply outer merge to retain customers who have not ordered
		.merge(df_customers, how='outer', on='customer_id')
		# Groupby on id, name, age, and country to retain the fields
		.groupby(['customer_id','name','age','country'])['total_price'].mean()
		# Sort on average total price
		.sort_values()
		# Reset index to restore id, name, age, and country as columns
		.reset_index()
		# Drop customer_id as it's not needed.
		.drop('customer_id', axis=1)
)

print(df_output)

# 3. Which customers have made at least 2 orders within 72 hours of each other?

# Merge the dataframes
merged_df = df_deliveries.merge(df_customers, on='customer_id')

# Convert delivery_date and delivery_time to datetime
merged_df['datetime'] = pd.to_datetime(merged_df['delivery_date'] + ' ' + merged_df['delivery_time'])

# Sort by customer_id and datetime
merged_df.sort_values(by=['customer_id', 'datetime'], inplace=True)

# Calculate the difference in time for each row
merged_df['time_diff'] = merged_df.groupby('customer_id')['datetime'].diff()

print(merged_df[['customer_id','time_diff']])

# Filter customers who made at least 2 orders within 72 hours
df_output = merged_df[merged_df['time_diff'].dt.total_seconds() <= 72*60*60]['customer_id'].unique()


# 4. In each country, list the customer who had the highest order amount ($). 
# Return the country, name, age, and total order amount.

merged_df = (
	df_deliveries
		# Apply outer merge to retain customers who have not ordered
		.merge(df_customers, how='outer', on='customer_id')
		# Get the total price
		.groupby(['customer_id','name','age','country'])['total_price'].sum()	
		# Reset index to restore attributes as columns
		.reset_index()
		# Drop customer id
		.drop('customer_id', axis=1)
)

# In each country, rank customers based on total price
merged_df['rank'] = merged_df.groupby('country')['total_price'].rank(method='first', ascending=False)
# Filter on rank=1 then drop the field as it's not needed in the output
df_output = merged_df.query('rank == 1').drop('rank', axis=1)

print(df_output)