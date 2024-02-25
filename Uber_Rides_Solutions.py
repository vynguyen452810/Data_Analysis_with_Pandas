"""
**Title: Uber Rides Analysis**

### DataFrames

# df_riders
|---------|------------|-----------|------------|-----------------|
| rider_id| rider_name | dob       | city       | registered_date |
|---------|------------|-----------|------------|-----------------|
| R101    | John       | 1991-05-01| New York   | 2020-04-01      |
| R102    | Sara       | 1989-09-15| San Francisco | 2019-08-10   |
| R103    | Alex       | 1994-11-20| Seattle    | 2021-01-15      |
| R104    | Mia        | 1992-02-28| Chicago    | 2019-09-05      |
| R105    | Eric       | 1988-06-30| Los Angeles| 2020-03-20      |
| R106    | Anna       | 1990-07-14| Houston    | 2022-05-07      |
| R107    | Lucas      | 1987-03-03| Miami      | 2021-04-29      |
| R108    | Emma       | 1995-01-25| Dallas     | 2021-12-01      |
| R109    | James      | 1993-12-12| Denver     | 2022-02-14      |

# df_rides
|--------|----------|-----------|----------|------------|-----------|
| ride_id| rider_id | date      | distance | fare       | driver_id |
|--------|----------|-----------|----------|------------|-----------|
| R201   | R101     | 2022-05-01| 7.5      | $15.50     | D401      |
| R202   | R102     | 2022-05-03| 12.3     | $24.60     | D402      |
| R203   | R103     | 2022-05-03| 9.7      | $19.40     | D401      |
| R204   | R104     | 2022-05-04| 5.2      | $10.40     | D403      |
| R205   | R105     | 2022-05-05| 15.8     | $31.60     | D404      |
| R206   | R106     | 2022-05-05| 4.3      | $8.60      | D402      |
| R207   | R107     | 2022-05-06| 8.9      | $17.80     | D405      |
| R208   | R108     | 2022-05-07| 6.1      | $12.20     | D406      |
| R209   | R101     | 2022-05-08| 5.5      | $11.00     | D407      |
| R210   | R102     | 2022-05-09| 13.2     | $26.40     | D408      |
| R211   | R104     | 2022-05-10| 6.8      | $13.60     | D409      |
| R212   | R105     | 2022-05-11| 7.2      | $14.40     | D410      |
| R213   | R107     | 2022-05-12| 9.4      | $18.80     | D411      |
| R214   | R108     | 2022-05-13| 12.5     | $25.00     | D412      |
| R215   | R106     | 2022-05-14| 11.3     | $22.60     | D413      |
| R216   | R103     | 2022-05-15| 10.1     | $20.20     | D414      |
| R217   | R101     | 2022-05-02|  7.5     | $13.50     | D413      |
| R218   | R101     | 2022-05-02|  7.5     | $11.40     | D415      |

### Questions

1. Which rider has spent the most on rides in terms of fare? Also, identify the total amount spent by that rider.

2. Calculate the average distance traveled by riders for each city. Rank the cities by their average ride distance in descending order.

3. For each driver, determine the number of unique riders they've served. Identify drivers who've served at least 2 riders.

4. From the rides that occurred in May 2022, identify if there are any riders who took rides with at least 2 different drivers. If so, list their names.

5. A "Consistent Rider" is defined as a rider who has taken rides on at least 3 consecutive days in May 2022. List their name and city.
"""

### Solution ###

import pandas as pd

# Setup
df_riders = pd.read_csv('./Data/Uber/riders.csv')
df_rides = pd.read_csv('./Data/Uber/rides.csv')


# 1. Which rider has spent the most on rides in terms of fare? Also, identify the total amount spent by that rider.

# Group by rider_id, sum the fare, and find the rider with the maximum fare
max_fare_rider = df_rides.groupby('rider_id')['fare'].sum().idxmax()
total_fare = df_rides.groupby('rider_id')['fare'].sum().max()

rider_name = df_riders[df_riders['rider_id'] == max_fare_rider]['rider_name'].iloc[0]

print(f"The rider who spent the most is {rider_name} with a total fare of {total_fare:.2f}.")

# 2. Calculate the average distance traveled by riders for each city. Rank the cities by their average ride distance in descending order.

# Merge the dataframes on rider_id
merged_df = df_rides.merge(df_riders, on='rider_id')

# Group by city and calculate the average distance
average_distance_per_city = merged_df.groupby('city')['distance'].mean().sort_values(ascending=False)
print(average_distance_per_city)

# 3. For each driver, determine the number of unique riders they've served. Identify drivers who've served at least 2 riders.

unique_riders_per_driver = df_rides.groupby('driver_id')['rider_id'].nunique()
drivers_atleast_2_riders = unique_riders_per_driver[unique_riders_per_driver >= 2].index.tolist()

print(f"Drivers who've served at least 2 riders are: {', '.join(drivers_atleast_2_riders)}")

# 4. From the rides that occurred in May 2022, identify if there are any riders who took rides with at least 2 different drivers. If so, list their names.

# Filter rides in May 2022
may_rides = df_rides[df_rides['date'].str.startswith('2022-05')]

# Group by rider and count unique drivers
unique_drivers_per_rider = may_rides.groupby('rider_id')['driver_id'].nunique()

# Filter riders with at least 2 unique drivers
riders_2_drivers = unique_drivers_per_rider[unique_drivers_per_rider >= 2].index.tolist()

rider_names = df_riders[df_riders['rider_id'].isin(riders_2_drivers)]['rider_name'].tolist()

print(f"Riders who took rides with at least 2 different drivers in May 2022 are: {', '.join(rider_names)}")


# 5. A "Consistent Rider" is defined as a rider who has taken rides on at least 3 consecutive days in May 2022. List their name and city.

# Convert the date in df_rides to datetime
df_rides['date'] = pd.to_datetime(df_rides['date'])

# Filter for rides in May 2022
may_rides = df_rides[(df_rides['date'] >= '2022-05-01') & (df_rides['date'] <= '2022-05-31')]

# Group by rider_id and date, then reset the index for easier processing
grouped_rides = may_rides.groupby(['rider_id', 'date']).size().reset_index()

# Calculate the difference in days for each row per rider
grouped_rides['day_diff'] = grouped_rides.groupby('rider_id')['date'].diff().dt.days

print(grouped_rides)

# Using shift to identify rows where difference is 1 day (consecutive) for both current and previous day
grouped_rides['consecutive_count'] = ((grouped_rides['day_diff'] == 1) & (grouped_rides.groupby('rider_id')['day_diff'].shift() == 1)).astype(int)

print(grouped_rides)

# Filter riders with at least 3 consecutive days
consistent_riders = grouped_rides.groupby('rider_id')['consecutive_count'].sum()
print(consistent_riders)

consistent_riders = consistent_riders[consistent_riders >= 1]

# Extract their name and city
consistent_rider_details = df_riders.merge(consistent_riders, left_on='rider_id', right_index=True)[['rider_id', 'rider_name', 'city']]

print(consistent_rider_details)

