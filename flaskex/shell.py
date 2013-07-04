from shutil import copy
from os import path, makedirs


def copyp(src, dst):
    ensure_exists(path.dirname(dst))
    return copy(src, dst)


def ensure_exists(target):
    if not path.exists(target):
        makedirs(target)
