import os
import os.path
import stat


def bin_check(sample1, target1):
    print target1
    return bool(sample1 % (target1 * 2) // target1)


def is_file_locked(fp1):
    return bin_check(os.stat(fp1).st_flags, stat.UF_IMMUTABLE)

