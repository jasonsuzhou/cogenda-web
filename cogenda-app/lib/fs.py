#-*- coding:utf-8 -*-

import os
from os.path import join, dirname, abspath, exists, isfile
from os import walk, remove

import fnmatch
import shutil

open_file = open

#should be called like: locate('*.txt', '*.py', '*.acc', root=path)
def locate(*args, **kw):
    root = 'root' in kw and kw['root'] or os.curdir
    root_path = abspath(root)
    patterns = args

    return_files = {}
    for path, dirs, files in walk(root_path):
        for pattern in args:
            for filename in fnmatch.filter(files, pattern):
                return_files[join(path, filename)] = filename
                #return_files.append(join(path, filename))
    return return_files

def recursive_copy(from_path, to_path):
    shutil.copytree(from_path, to_path)

def move_dir(from_path, to_path):
    shutil.move(from_path, to_path)

def read_all_file(path):
    project_file = open_file(path, 'r')
    text = project_file.read()
    project_file.close()

    return text

def replace_file_contents(path, contents):
    project_file = open_file(path, 'w')
    project_file.write(contents)
    project_file.close()

def remove_file(path):
    remove(path)

def is_file(path):
    return isfile(path)
