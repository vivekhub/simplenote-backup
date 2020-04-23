# simplenote-backup

A small python based script to backup all your simplenote.com scripts.  


## Background

Simplenote is a fairly lightweight multiplatform note-taking application with
markdown support. One of the interesting things about simplenote is that it
allows only text based notes which is great for developers like me who want to
maintain a lot of textual content.  I use simplenote for a lot of my note
taking needs and  I have the native app both on my laptop and on my phones and
use it to take extensive notes about everything and anything. 

While simplenote takes care of sync and backup of notes, I wanted a way to keep
my own backup in a format that is easily searchable.  Also what
would happen if they decide to close down the service? Hence was born the
backup.  

This backup makes a copy of all your personal simplenotes and keeps it in a
SQLite database so it is fully searchable and queryable.


## How to use it

The usage is pretty straight forward.   Run the script with your simplenote
userid and password and specify how you want the backup to be done ie. To a
SQLite database or to a file. 

Every time you run the script, it will get all your notes and attempt to sync
with the existing database if one exists and update notes to their latest
version.  If you want a fresh backup to be created use the "-c" option.

    usage: snbackup.py [-h] [-v] -u USER -p PASSWORD [-c] (-s SQLITE | -j JSON)

    optional arguments:
      -h, --help            show this help message and exit
      -v, --verbose         Print progress messages
      -u USER, --user USER  Your simplenote userid
      -p PASSWORD, --password PASSWORD
                            Your simplenote password
      -c, --create          Create a fresh backup
      -s SQLITE, --sqlite SQLITE
                            SQLite3 database where the data will be stored
      -j JSON, --json JSON  JSON file where the data will be stored


## Dependancies

All the python dependancies are listed in requirements.txt. It uses the
simplenote python library for accessing the notes.

## License

This software is released under the MIT license.  
