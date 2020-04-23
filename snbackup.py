#!tusr/bin/env python

from datetime import datetime
import sqlite3
import simplenote
import ddl
import getpass
import args
import json

def SNTagsIter(SNEntries):
    for entry in SNEntries:
        for tag in entry['tags']:
            yield (tag, entry['key'])


def GetSimpleNoteEntires(userid, password, verbose=False):
    try:
        if verbose:
            print('Fetching notes from simplenote.com...')
        sn_conn = simplenote.Simplenote(userid, password)
        nlist = sn_conn.get_note_list()[0]
        if verbose:
            print('{0} Notes fetched from simplenote.com'.format(len(nlist)))
        return nlist
    except:  # For now we will ignore errors
        return []


def GetNotesIter(notes):
    for note in notes:
        yield (
            note['key'],
            datetime.fromtimestamp(note['createdate']),
            datetime.fromtimestamp(note['modifydate']),
            note['deleted'],
            note['version'],
            note['content'],
            note['publishURL'],
            note['shareURL'],
        )


def LoadSimpleNoteEntries(conn, userid, password, verbose=False):

    sn_entries = GetSimpleNoteEntires(userid, password)
    conn.text_factory = str
    c = conn.cursor()
    '''
        ?,\ # key
        ?,\ # createdate
        ?,\ # modifydate
        ?,\ # deleted
        ?,\ # version
        ?,\ # content
        ?,\ # publishurl
        ?,\ # shareurl
    '''
    c.executemany('insert into  sn_note values(?, ?, ?, ?, ?, ?, ?, ?);',
                  GetNotesIter(sn_entries))

    c.executemany('insert into sn_tag(tag, note)  values (?, ?)',
                  SNTagsIter(sn_entries))
    if verbose:
        print('Loaded {0} notes'.format(len(sn_entries)))


def BackupRecord(cursor, note, update=True):
    if update:
        notesql = "update sn_note set createdate = ?, modifydate = ?, deleted = ?, version = ?,  content = ?, publishurl = ?, shareurl = ? where key = ?;"
    else:
        notesql = 'insert into sn_note (createdate, modifydate, deleted, version, content, publishurl, shareurl, key) values (?, ?, ?, ?, ?, ?, ?, ?);'
    cursor.execute(notesql, (
        datetime.fromtimestamp(note['createdate']),
        datetime.fromtimestamp(note['modifydate']),
        note['deleted'],
        note['version'],
        note['content'],
        note['publishURL'],
        note['shareURL'],
        note['key'],
    ))
    cursor.execute('delete from sn_tag where note = ?', (note['key'], ))
    cursor.executemany('insert into sn_tag(tag, note)  values (?, ?)',
                       SNTagsIter([
                           note,
                       ]))


def SyncSimpleNoteEntries(conn, userid, password, verbose=False):
    sn_entries = GetSimpleNoteEntires(userid, password)
    conn.text_factory = str
    updated = 0
    added = 0
    entry_qry = 'select version from sn_note where key=?;'

    total = 0
    for entry in sn_entries:
        total += 1
        cursor = conn.execute(
            entry_qry,
            (entry['key'], ),
        )
        data = cursor.fetchone()
        update_cursor = conn.cursor()
        if data:
            # We will assume that only version is the check
            if data[0] < entry['version']:
                updated += 1
                # We should backup this record and its children
                BackupRecord(update_cursor, entry)
        else:  # This is a new record
            added += 1
            BackupRecord(update_cursor, entry, update=False)
    return (
        total,
        added,
        updated,
    )


def SyncDatabase(sqlitedbfile, userid, password, verbose=False):
    conn = sqlite3.connect(sqlitedbfile)
    if verbose:
        print('---- Loading notes ----')
    total, added, updated = SyncSimpleNoteEntries(
        conn, userid, password, verbose=verbose)

    if verbose:
        print('Total {0} Entries, Backup : added {1}, updated {2}'.format(
            total, added, updated))
    if verbose:
        print('----Finalizing DB----')
    conn.commit()
    conn.close()
    if verbose:
        print('----Completed----')


def LoadDatabase(sqlitedbfile, userid, password, verbose=False):
    conn = sqlite3.connect(sqlitedbfile)
    if verbose:
        print('---- Creating Tables ----')
    ddl.InitializeSQLite3(conn)
    if verbose:
        print('---- Loading notes ----')
    LoadSimpleNoteEntries(conn, userid, password, verbose=verbose)
    if verbose:
        print('----Finished Loading Notes ----')
        print('----Finalizing database ----')
    ddl.FinalizeDB(conn)
    conn.commit()
    conn.close()
    if verbose:
        print('----Completed----')


def WriteFile(filename, userid, password, verbose=False):
    with open(filename, 'w', encoding='utf-8') as f:
        sn_entries = GetSimpleNoteEntires(userid, password)
        json.dump(sn_entries, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    pargs = args.ArgProcess(args.ArgSetup())

    if pargs.json is not None:
        # This is a simple file backup.
        WriteFile(
            pargs.json, pargs.user, pargs.password, verbose=pargs.verbose)
    else:
        # This is a database based backup
        # Create database the first time?
        if pargs.create:
            LoadDatabase(
                pargs.sqlite, pargs.user, pargs.password, verbose=pargs.verbose)
        else: # Do a regular sync
            SyncDatabase(
                pargs.sqlite, pargs.user, pargs.password, verbose=pargs.verbose)
