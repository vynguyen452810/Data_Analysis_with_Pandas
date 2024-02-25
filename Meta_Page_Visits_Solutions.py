"""
Title: Meta Page Visits

Instruction: Given the tables provided below, solve the problem sets involving Pandas DataFrames. 

Hint: Time yourself. Aim to solve each question spending no more than 7 to 8 minutes per each question. In addition, practice explaining your solution out loud.


+---------+------------+-------+------------+----------+
| user_id |    date    | pages | time_spent | platform |
+---------+------------+-------+------------+----------+
|  1001   | 2023-01-05 |   3   |     15     |  Mobile  |
|  1002   | 2023-01-06 |   5   |     20     |  Web     |
|  1003   | 2023-01-07 |   4   |     18     |  VR      |
|  1004   | 2023-01-08 |   6   |     25     |  Web     |
+---------+------------+-------+------------+----------+


### DataFrames ### 

# df_user_interactions

+---------+------------+---------------+--------------------+----------+
| user_id |     date   | pages_visited | time_spent_minutes | platform |
+---------+------------+---------------+--------------------+----------+
| 1001    | 2023-01-05 |      3        |        15          |  Mobile  |
| 1002    | 2023-01-06 |      5        |        20          |  Web     |
| 1003    | 2023-01-07 |      4        |        18          |  VR      |
| 1004    | 2023-01-08 |      6        |        25          |  Web     |
+---------+------------+---------------+--------------------+----------+

# df_user_profiles
+---------+-----+--------+---------+------------------+
| user_id | age | gender | country | registered_since |
+---------+-----+--------+---------+------------------+
|  1001   | 28  |   M    |    US   |    2020-06-01    |
|  1002   | 34  |   F    |    UK   |    2018-11-15    |
|  1003   | 24  |   M    |    IN   |    2021-05-20    |
|  1005   | 30  |   F    |    CA   |    2019-08-07    |
+---------+-----+--------+---------+------------------+

# df_page_metadata

+---------+--------------+-------------+
| page_id | page_name    | category    |
+---------+--------------+-------------+
|    1    |  Home        | Landing     |
|    2    |  Photos      | Multimedia  |
|    3    |  Marketplace | E-commerce  |
|    4    |  VR World    | Interactive |
+---------+--------------+-------------+

### Questions ###

1. Using the `df_user_interactions` and `df_user_profiles` DataFrames, determine the country of each user and their average time spent on interactions. Note that each user in the `df_user_profiles` DataFrame can have multiple entries in the `df_user_interactions` DataFrame. Only include users in both DataFrames.

2. Given the User Profiles (`df_user_profiles`) DataFrame, find out how many users have registered in each year. Display the counts in descending order.

3. Given the two DataFrames, `df_user_interactions` (which contains user interactions) and `df_page_metadata` (which provides metadata about each page), determine the total time each user has spent on different page categories. After calculating, for each user, order the page categories by the time they've spent in descending order. Your resulting table should display the columns: `user_id`, `category`, `time_spent_minutes`, `country`, and `age`. Exclude any users who are not present in the `df_user_interactions` DataFrame.
"""

### Solution ###

import pandas as pd

# Setup

df_user_interactions = pd.read_csv('./Data/Meta/user_interactions.csv')
df_user_profiles = pd.read_csv('./Data/Meta/user_profiles.csv')
df_page_metadata = pd.read_csv('./Data/Meta/page_metadata.csv')

## 1.

df_user = (
	# Start with the interactions data
    df_user_interactions 
    # Merge with user profiles based on user_id
    .merge(df_user_profiles, how='inner', on='user_id')  
    # Group by user_id and country
    .groupby(['user_id', 'country'])['time_spent_minutes']  
    # Calculate the average time spent
    .mean()  
     # Reset the index for a clean DataFrame format
    .reset_index() 
)

print(df_user)

## 2.

# Convert the 'registered_since' column to datetime format
df_user_profiles['registered_since'] = pd.to_datetime(df_user_profiles['registered_since'])

# Extract the year from the 'registered_since' column and count the occurrences
yearly_counts = df_user_profiles['registered_since'].dt.year.value_counts()

# Sort the counts in descending order
sorted_counts = yearly_counts.sort_values(ascending=False)

print(sorted_counts)

## 3. 

# Calculate the total time spent by users on each page category
df_user_time_spent = (
    df_user_interactions.merge(df_page_metadata, how='inner', left_on='pages_visited', right_on='page_id')
    .groupby(['user_id', 'category'])['time_spent_minutes']
    .sum()
    .reset_index()
    .sort_values(['user_id', 'time_spent_minutes'], ascending=[True, False])  # Sort by user_id, and then by time spent in descending order
)

# Merge with the user profiles to get additional details like country and age
df_user = (
    df_user_time_spent
    .merge(df_user_profiles, how='inner', on='user_id')
)

# Select the desired columns for the final result
result = df_user[['user_id', 'category', 'time_spent_minutes', 'country', 'age']]

print(result)