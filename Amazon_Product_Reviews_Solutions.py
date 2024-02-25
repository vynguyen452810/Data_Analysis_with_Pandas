"""
Title: Amazon Product Reviews

# df_product_sales
+------------+------------+------------+------------+--------+
| product_id | sale_date  | units_sold | sale_price | region |
+------------+------------+------------+------------+--------+
|    P101    | 2023-05-01 |     10     |    49.99   | North  |
|    P102    | 2023-05-02 |     8      |    24.99   | West   |
|    P103    | 2023-05-03 |     15     |    14.99   | South  |
|    P104    | 2023-05-04 |     5      |   199.99   | East   |
+------------+------------+------------+------------+--------+

# df_product_reviews
+------------+-------------+--------+-------------+
| product_id | review_date | rating | reviewer_id |
+------------+-------------+--------+-------------+
|    P101    |  2023-05-03 |   5    |    R501     |
|    P102    |  2023-05-04 |   3    |    R502     |
|    P103    |  2023-05-05 |   4    |    R503     |
|    P105    |  2023-05-06 |   2    |    R504     |
+------------+-------------+--------+-------------+

### Questions

1. For each product in the df_product_sales DataFrame, what is the total sales (units_sold multiplied by sale_price)
and average rating? Output a DataFrame showing product_id, total_revenue, and average_rating of each product. Assume
that some products in the df_product_sales may not have any reviews. For such products, impute the average_rating 
with-99.

2. For the product_sales table, compute the day-on-day growth in total_revenue. Display the results in a new column
named DoD_growth. Remove the first day in the output DataFrame, and sort the rows based on the ascending order of date.

3. For the product_sales table, group by the region column and determine the product with the highest sales
(in terms of revenue) for each region. Assume that more than one product could have the same revenue values
for each region. Output the region, product_id, total_revenue.

"""

### Solution ###

import pandas as pd

# Get data
df_product_sales = pd.read_csv('./Data/Amazon/product_sales.csv')
df_product_reviews = pd.read_csv('./Data/Amazon/product_reviews.csv')


# 1. For each product in the df_product_sales DataFrame, what is the total sales (units_sold multiplied by sale_price)
# and average rating? Output a DataFrame showing product_id, total_revenue, and average_rating of each product. Assume
# that some products in the df_product_sales may not have any reviews. For such products, impute the average_rating 
# with-99.

# Calculate total revenue for each product sale entry by multiplying units_sold and sale_price
df_product_sales['total_revenue'] = (
	df_product_sales['units_sold'] * df_product_sales['sale_price']
)

# Group by product_id to get the total revenue for each product
df_total_revenues = (
	df_product_sales
		.groupby('product_id')['total_revenue']
		.sum()  # Sum the total_revenue for each product
		.reset_index()  # Reset index to move product_id from index to column
)

# Group by product_id to get the average rating for each product
df_avg_ratings = (
	df_product_reviews
		.groupby('product_id')['rating']
		.mean()  # Calculate the mean of ratings for each product
		.reset_index()  # Reset index to move product_id from index to column
		.rename(columns={'rating': 'average_rating'})  # Rename the rating column to average_rating for clarity
)

# Merge the total revenues dataframe with average 
# ratings dataframe based on product_id
df_output = df_total_revenues.merge(df_avg_ratings, how='left', on='product_id')

# Handle missing ratings by filling NaN values 
# with a placeholder value of -99
df_output['average_rating'] = df_output['average_rating'].fillna(-99)

# Display the merged output
print(df_output)


# 2. For the product_sales table, compute the day-on-day growth in total_revenue. Display the results in a new column
# named DoD_growth. Remove the first day in the output DataFrame, and sort the rows based on the ascending order of date.

# Calculate the total revenue for each row by multiplying units_sold and sale_price
df_product_sales['total_revenue'] = (
    df_product_sales['units_sold'] * df_product_sales['sale_price']
)

# Aggregate total revenue for each sale date
df_total_revenues = (
    df_product_sales
        .groupby('sale_date')['total_revenue']  # Group by sale_date
        .sum()  # Sum the total_revenue for each sale date
        .reset_index()  # Convert sale_date from an index to a column
        .sort_values('sale_date', ascending=True)  # Sort by sale_date in ascending order
)

# Compute previous day's total revenue using shift() for day-on-day growth rate calculation
df_total_revenues['prev_total_revenue'] = df_total_revenues['total_revenue'].shift()

# Calculate the day-on-day growth rate
df_total_revenues['DoD'] = (
    df_total_revenues['total_revenue'] / df_total_revenues['prev_total_revenue'] - 1
)

# Exclude the first row as it doesn't have a previous day to compare to
# And retain only the 'sale_date' and 'DoD' columns for final output
df_output = df_total_revenues.loc[1:, ['sale_date', 'DoD']]

# Display the result
print(df_output)


# 3. For the product_sales table, group by the region column and determine the product with the highest sales
# (in terms of revenue) for each region. Assume that more than one product could have the same revenue values
# for each region. Output the region, product_id, total_revenue.

# Calculate the total revenue for each row by multiplying units_sold and sale_price
df_product_sales['total_revenue'] = (
    df_product_sales['units_sold'] * df_product_sales['sale_price']
)

# Rank products within each region based on total revenue
df_product_sales['product_rank'] = (
    df_product_sales.groupby('region')['total_revenue']
    .rank(method='dense', ascending=False)
)

# Filter rows where product_rank is 1, implying top product(s) in terms of revenue
df_output = df_product_sales[df_product_sales.product_rank == 1]

# Optionally, filter only relevant columns for clarity
df_output = df_output[['region', 'product_id', 'total_revenue']]

# Display the result
print(df_output)



