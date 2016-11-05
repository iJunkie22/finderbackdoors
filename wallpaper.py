# coding: utf-8
from __future__ import unicode_literals, print_function
import sqlite3
import os.path

__author__ = 'ethan'


class WallDB(object):
    def __init__(self):
        self.db_fp = os.path.expanduser('~/Library/Application Support/Dock/desktoppicture.db')
        self.conn = sqlite3.connect(self.db_fp)
        self.conn.row_factory = sqlite3.Row
        self.cur = self.conn.cursor()

    def get_primary_wallpaper_path(self):
        self.cur.execute(
            '''SELECT rowid FROM pictures WHERE ((pictures.space_id IS NULL) AND (pictures.display_id IS NULL));''')
        pic_ids = [c[0] for c in self.cur]
        assert len(pic_ids) == 1
        pic_id_x = pic_ids[0]
        self.cur.execute(
            '''SELECT data_id FROM preferences WHERE ((preferences.picture_id == ?) AND (preferences.key == 1))''',
            (pic_id_x,))
        pref_rows = self.cur.fetchall()
        assert len(pref_rows) == 1

        pref_row_x = pref_rows[0]

        self.cur.execute(
            '''SELECT data.value from data WHERE (data.rowid == ?)''', pref_row_x
        )
        value_rows = self.cur.fetchall()
        assert len(value_rows) == 1
        return value_rows[0][0]

    def close(self):
        self.conn.close()

    def __del__(self):
        self.close()

if __name__ == '__main__':
    wdb = WallDB()
    print(wdb.get_primary_wallpaper_path())

