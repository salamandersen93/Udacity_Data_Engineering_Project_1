# DROP TABLES

songplay_table_drop = """DROP TABLE IF EXISTS songplay_table"""
user_table_drop = """DROP TABLE IF EXISTS user_table"""
song_table_drop = """DROP TABLE IF EXISTS song_table"""
artist_table_drop = """DROP TABLE IF EXISTS artist_table"""
time_table_drop = """DROP TABLE IF EXISTS time_table"""
    
songplay_table_create = ("""CREATE TABLE IF NOT EXISTS songplay_table (songplay_id text, \
start_time text, user_id text, level text, song_id text, artist_id text, session_id text, location text, \
user_agent text)""")

user_table_create = ("""CREATE TABLE IF NOT EXISTS user_table (user_id text, \
first_name text, last_name text, gender text, level text)""")

    
song_table_create = ("""CREATE TABLE IF NOT EXISTS song_table (song_id text, title text, \
artist_id text, year int, duration int)""")

artist_table_create = ("""CREATE TABLE IF NOT EXISTS artist_table (artist_id text, \
name text, location text, latitude float, longitude float)""")

time_table_create = ("""CREATE TABLE IF NOT EXISTS time_table (start_time text, \
hour int, day int, week int, month text, year int, weekday text)
""")
    
# INSERT RECORDS

songplay_table_insert = ("""INSERT INTO songplay_table (songplay_id, start_time, user_id \
level, song_id, artist_id, session_id, location, user_agent) VALUES ( \
%s, %s, %s, %s, %s, %s, %s, s, %s)""")
# last %s is an input list (I think)
    
user_table_insert = ("""INSERT INTO user_table (user_id, first_name, last_name, gender, level) \
VALUES (%s, %s, %s, %s, %s)""")

song_table_insert = """INSERT INTO song_table (song_id, title, artist_id, year, duration) \
VALUES (%s, %s, %s, %s, %s)"""

artist_table_insert = ("""INSERT INTO artist_table (artist_id, name, location, latitude, longitude) \
VALUES (%s, %s, %s, %s, %s)""")


time_table_insert = ("""INSERT INTO time_table (start_time, hour, day, week, month, year, weekday) \
VALUES (%s, %s, %s, %s, %s, %s, %s)""")

# FIND SONGS
#Implement the song_select query in sql_queries.py to find the song ID and artist ID based on the title, artist name, and duration of a song.
song_select = ("""SELECT song_table.song_id, artist_table.artist_id FROM song_table JOIN artist_table ON (song_table.artist_id = artist_table.artist_id) WHERE \
song_table.title = %s AND artist_table.name = %s AND song_table.duration = %s""")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]