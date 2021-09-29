
<b> Overview - Sparkify Project (Postgres Implementation) </b>

This project is based on a hypothetical start-up company known as Sparkify. The business challenge is to develop a database which allows easy querying and analysis of data collected on songs and user activity on their music streaming app. One of the primary business questions at hand is how to analyze which songs users are listening to. Purpose of the Sparkify music database is to provide a repository for analysis of user song play data, which is currently hosted as a directory of JSON logs. 

In this project, postgres database will be leveraged with a star schema broken into five separate tables (shown below). The songplay table is the fact table while the user table, song table, artist table, and time table are each individual dimension tables.

1. Songplay_table
2. User_table
3. Song_table
4. Artist_table
5. Time_table

The breakdown follows a normal form and allows easy querying of artist information (location, name), song information (duration, year, title), user information (first name, last name,
gender, level), time data (hour, day, week, month, year, weekday), as well as song play information specific to session data including user id, start time, session id, location, etc. The star schema implemented allows for queries to be performed on session data from the fact table while also accessing specific information pertaining to users, time, and artist from the dimension tables. 
