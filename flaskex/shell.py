from shutil import copy
from os import path, makedirs


def copyp(src, dst):
    parent_directory = path.dirname(dst)
    if not path.exists(parent_directory):
        makedirs(parent_directory)
    return copy(src, dst)
