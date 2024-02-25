"""
**Title: Spotify User Insights**

Instruction: Provided below are tables that resemble Spotify's user and playlist data. Solve the problem sets involving Pandas DataFrames.

Hint: Time yourself. Strive to solve each question within 7 to 8 minutes. Moreover, practice explaining your solution out loud.

### DataFrames

# df_user_activity
|--------|-----------|----------|--------------|-----------|
| user_id| username  | country  | last_active  | premium  |
|--------|-----------|----------|--------------|-----------|
| S101   | John      | US       | 2023-05-01   | True     |
| S102   | Jane      | UK       | 2023-05-04   | False    |
| S103   | Emily     | IN       | 2023-05-03   | True     |
| S104   | Mike      | CA       | 2023-05-02   | False    |
| S105   | Sara      | AU       | 2023-05-05   | True     |
| S106   | Luke      | NZ       | 2023-05-06   | False    |
| S107   | Ella      | US       | 2023-05-05   | True     |
| S108   | Max       | UK       | 2023-05-04   | False    |

# df_playlists
|--------|-------------|-------------|------------|
| user_id| playlist_id | song_count  | genre      |
|--------|-------------|-------------|------------|
| S101   | PL101       | 20          | Pop        |
| S101   | PL102       | 15          | Rock       |
| S102   | PL103       | 25          | Classical  |
| S103   | PL104       | 30          | Jazz       |
| S104   | PL105       | 10          | Pop        |
| S105   | PL106       | 20          | Hip-Hop    |
| S106   | PL107       | 5           | Rock       |
| S107   | PL108       | 15          | Jazz       |
| S108   | PL109       | 20          | Classical  |

# df_listens
|--------|-------------|-------------|------------|
| user_id| song_id     | listen_date | listen_time|
|--------|-------------|-------------|------------|
| S101   | SG101       | 2023-05-01  | 3:30       |
| S102   | SG102       | 2023-05-02  | 4:15       |
| S103   | SG103       | 2023-05-03  | 2:45       |
| S104   | SG101       | 2023-05-02  | 4:00       |
| S105   | SG104       | 2023-05-04  | 5:00       |
| S106   | SG105       | 2023-05-06  | 3:15       |
| S107   | SG102       | 2023-05-04  | 4:30       |
| S108   | SG106       | 2023-05-05  | 5:15       |

### Questions

1. Identify the top 3 premium users who have listened to music the most in terms of total time in the month of May 2023.

2. Determine the most popular genre among users from the US.

3. For each country, find the user who has the highest number of songs in their playlists.
"""

### Solution ###

import pandas as pd

# Setup
df_listens = pd.read_csv('./Data/Spotify/listens.csv')
df_playlists = pd.read_csv('./Data/Spotify/playlists.csv')
df_user_activity = pd.read_csv('./Data/Spotify/user_activity.csv')

# 1. Identify the top 3 premium users who have listened to music the most in terms of total time in the month of May 2023.

# Convert listen_time to timedelta
df_listens['listen_time'] = pd.to_timedelta(df_listens['listen_time'] + ':00')

# Filter for premium users
premium_users = df_user_activity[df_user_activity['premium'] == True]

# Get total listen time by user
total_listen_time = df_listens.groupby('user_id')['listen_time'].sum()

# Merge the dataframes to get total listen time for each premium user
merged_df = premium_users.merge(total_listen_time, on='user_id')

# Sort and get top 3 premium users
top_3_premium_users = merged_df.nlargest(3, 'listen_time')
print(top_3_premium_users[['user_id', 'listen_time']])

# 2. Determine the most popular genre among users from the US.

# Filter for US users
us_users = df_user_activity[df_user_activity['country'] == 'US']['user_id']

# Filter playlists for US users
us_genres = df_playlists[df_playlists['user_id'].isin(us_users)]

# Identify the most popular genre
popular_genre_us = us_genres['genre'].value_counts().idxmax()
print(f"Most popular genre in US: {popular_genre_us}")

# 3. For each country, find the user who has the highest number of songs in their playlists.

# Calculate total song count for each user
playlist_songs = df_playlists.groupby('user_id')['song_count'].sum().reset_index()

# Merge to get total song count for each user
merged_df = df_user_activity.merge(playlist_songs, on='user_id')

# Identify the user with the highest song count for each country
top_users_per_country = merged_df.loc[merged_df.groupby('country')['song_count'].idxmax()]
print(top_users_per_country[['country', 'username', 'song_count']])
