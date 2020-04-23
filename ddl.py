#!/usr/bin/env python

import sqlite3


def InitializeSQLite3(conn):
    c = conn.cursor()
    
    drop_sntags = 'drop table if exists sn_tag;'
    c.execute(drop_sntags)

    drop_sn = 'drop table if exists sn_note;'
    c.execute(drop_sn)
    c.close()
    c = conn.cursor()


    create_sn = "create table if not exists \
        sn_note (key text primary key, \
        createdate timestamp, \
        modifydate timestamp, \
        deleted INTEGER, \
        version INTEGER, \
        content TEXT, \
        publishurl INTEGER, \
        shareurl TEXT);"

    c.execute(create_sn)


    create_sntags = "create table if not exists sn_tag(\
            ID INTEGER PRIMARY KEY AUTOINCREMENT, \
            tag TEXT, \
            note INTEGER, \
            FOREIGN KEY(note) REFERENCES sn_note(key));"

    c.execute(create_sntags)


def FinalizeDB(conn):
    c = conn.cursor()
    c.execute('create index idx_sntags on sn_tag(tag);')
    c.execute('create index idx_keyversion on sn_note(key, version);')


if __name__ == '__main__':
    conn = sqlite3.connect('snbackup.sqlite3')
    InitializeSQLite3(conn)
    FinalizeDB(conn)
