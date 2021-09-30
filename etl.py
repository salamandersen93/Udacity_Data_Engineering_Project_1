import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *

"""
    Processing of song file with filepath passed via argument.
    Song data is extracted into pandas df and inserted into the song_table.
    Artist data is extracted into pandas df and inserted into artist_table.

    INPUTS:
    * cur the cursor variable
    * filepath the file path to the song file
    """

def process_song_file(cur, filepath):
    
    # insert song data
    df = pd.read_json(filepath, lines = True) 
    song_df = df[['song_id', 'title', 'artist_id', 'year', 'duration']]
    
    for i, row in song_df.iterrows():
        cur.execute(song_table_insert, list(row))
    
    # insert artist record
    artist_df = df[['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']]

    for i, row in artist_df.iterrows():
        cur.execute(artist_table_insert, list(row))

"""
    Processing of log file with filepath passed via argument.
    Log data is extracted into pandas df.
    Time dataframe created as copy and time columns created using dt in pandas.
    Time dataframe filtered for date and time columns and inserted into time_table.
    User dataframe created from log dataframe and inserted into user_table.
    
    Song_select query called on each row of the log dataframe using artist_id and song_id.
    Selected data inserted into songplay_table using songplay_table_insert query.

    INPUTS:
    * cur the cursor variable
    * filepath the file path to the song file
    """


def process_log_file(cur, filepath):
    # open log file
    df = pd.read_json (filepath, lines = True)

    # filter by NextSong action
    df = df[df['page'] == 'NextSong']

    # convert timestamp column to datetime
    t = df.copy()
    t['ts'] = pd.to_datetime(df['ts'], unit='ms')
    
    # insert time data records
    t['year'] = pd.DatetimeIndex(t['ts']).year
    t['month'] = pd.DatetimeIndex(t['ts']).month
    t['week'] = pd.DatetimeIndex(t['ts']).week
    t['day'] = pd.DatetimeIndex(t['ts']).day
    t['weekday'] = pd.DatetimeIndex(t['ts']).weekday
    t['hour'] = pd.DatetimeIndex(t['ts']).hour
    
        # converting df to dict
    df_dict = t.T.to_dict()

    list_of_time_data = []

    # only want dates
    for key, value in df_dict.items():
        entry = value
        dates_dict = {k: v for k, v in entry.items() if k in ['year', 'month', 'week', 'day', 'weekday', 'hour', 'ts']}
        list_of_time_data.append(dates_dict)
    
    time_df = pd.DataFrame(list_of_time_data)

    # want order consistent with SQL INSERT query
    time_df = time_df[['ts', 'hour', 'day', 'week', 'month', 'year', 'weekday']]

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[['userId', 'firstName', 'lastName', 'gender', 'level']]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None
        
        # insert songplay record
        songplay_data = [index, pd.to_datetime(row.ts, unit='ms'), row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent]
        cur.execute(songplay_table_insert, songplay_data)

"""
    Iterating through all json files residing in filepaths passed via arguments.
    Processes all files in data/song_data and data/log_data into functions passed via arguments.
    Commits updates in database and prints the number of files processed.

    INPUTS:
    * cur the cursor variable
    * conn the definition of the connection
    * filepath the file path to the song file
    * func the data processing function 
    """

def process_data(cur, conn, filepath, func):
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()