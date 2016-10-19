from __future__ import unicode_literals, print_function
import os.path
from ds_store import DSStore, DSStoreEntry
import shutil
import weakref
import datetime

PSEUDO_USER_TRASH = os.path.expanduser("~/.Trash/")
TRASH_DS_FP = os.path.join(PSEUDO_USER_TRASH, ".DS_Store")


class FinderTrash(object):
    __initialized = False
    __singleton_proxy = None
    __open_trash = None

    @staticmethod
    def __new__(cls, *args, **kwargs):
        if FinderTrash.__singleton_proxy is not None:
            print("Returning mirror from __new__")
            return FinderTrash.__singleton_proxy
        else:
            obj = super(FinderTrash, cls).__new__(cls)
            FinderTrash.__singleton_proxy = weakref.proxy(obj)
        return obj

    def __init__(self):
        type(self).__initialized = True
        type(self).__open_trash = DSStore.open(TRASH_DS_FP, "r+")

    @classmethod
    def _add_trash_entry(cls, fp):
        unique_entry_name = entry_name = os.path.basename(fp)
        entry_src = os.path.dirname(fp) + "/"

        trash_dst = os.path.join(PSEUDO_USER_TRASH, os.path.basename(fp))

        if os.path.exists(trash_dst):
            fname, dot, ftype = entry_name.rpartition(".")
            if dot != ".":
                fname, ftype = ftype, fname
            unique_entry_name = "".join((fname, " ",
                                         unicode(datetime.datetime.now().time().isoformat()).replace(":", "."),
                                         dot, ftype))

        ptbN = DSStoreEntry(unique_entry_name, 'ptbN', 'ustr', unicode(entry_name))
        ptbL = DSStoreEntry(unique_entry_name, 'ptbL', 'ustr', unicode(entry_src))
        cls.__open_trash.insert(ptbN)
        cls.__open_trash.insert(ptbL)
        # self.trash_dss[entry_name]['ptbN'] = ('ustr', entry_name)
        # self.trash_dss[entry_name]['ptbL'] = ('ustr', entry_src)

        return unique_entry_name

    @classmethod
    def move_to_trash(cls, fp):
        trash_fn = cls._add_trash_entry(fp)
        trash_dst = os.path.join(PSEUDO_USER_TRASH, trash_fn)
        shutil.move(fp, trash_dst)

    @classmethod
    def close(cls):
        cls.__open_trash.close()

    def __del__(self):
        FinderTrash.__initialized = False
        self.close()


if __name__ == '__main__':
    ft = FinderTrash()
    ft2 = FinderTrash()
    ft2.move_to_trash(os.path.expanduser('~/TEMP/foo.txt'))

