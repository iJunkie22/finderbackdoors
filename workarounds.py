from __future__ import print_function, unicode_literals
import os.path

ASEPSIS_CAGE = '/usr/local/.dscage/'
ASEPSIS_ON = os.path.isdir(ASEPSIS_CAGE)


def is_ds_store(path):
    return os.path.basename(path) == '.DS_Store'


def asepsis_mirror(path):
    return os.path.join(ASEPSIS_CAGE, os.path.abspath(path))


def found_in_cage(path):
    return ASEPSIS_ON and os.path.isfile(asepsis_mirror(path))


def ds_store_path(path):
    assert is_ds_store(path), '{} is not a .DS_Store path!'.format(path)
    caged_path = asepsis_mirror(path)
    return caged_path if os.path.exists(caged_path) else path

