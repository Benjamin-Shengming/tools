#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import os
import shutil 
from datetime import datetime  # <-- Fix: use standard datetime


def natural_path_compare(a, b):
    """
    Compare two paths using natural order (numbers as numbers, not strings).
    Returns -1 if a < b, 0 if a == b, 1 if a > b.
    """

    def split_key(path):
        # Split path into components, then split each component into digit/non-digit parts
        parts = []
        for part in re.split(r"[\/]", path):
            # Split into digit and non-digit chunks
            for chunk in re.split(r"(\d+)", part):
                if chunk.isdigit():
                    parts.append(int(chunk))
                else:
                    parts.append(chunk)
        return parts

    ka = split_key(a)
    kb = split_key(b)
    # Compare component-wise
    for x, y in zip(ka, kb):
        if x == y:
            continue
        if type(x) == type(y):
            return -1 if x < y else 1
        # Numbers come before strings
        return -1 if isinstance(x, int) else 1
    # If all components so far are equal, shorter path is less
    if len(ka) == len(kb):
        return 0
    return -1 if len(ka) < len(kb) else 1


class FolderHelper(object):
    """
    Class easy to manipulate files/folders under certain path
    Usage example:
        a_dir = FolderHelper("/testdir")
        a_dir.del_empty_sub_dir()   # remove all empty sub-directories
        a_dir.del_empty_file()      # remove all empty files, empty file: file size is zero
        a_dir.del_empty_child()     # remove all empty files and sub-directories
        a_dir.list_file(recursive=True)   # similar as linux command tree but yield file path
        a_dir.list_file(recursive=False)  # similar as linux command ls but yield file path
        a_dir.list_dir(recursive=True)    # similar as linux command tree but yield sub-folder path
        a_dir.list_dir(recursive=False)   # similar as linux command ls but yield sub-folder path

    TODO Add more functions
        del_file_by_extension(extension, recursive=True)
    """

    def __init__(self, folder_path="./", topdown=True):
        self.dir_path = folder_path
        self.topdown = topdown

    # Generic file and dir iterators
    def iter_files(self, recursive=True):
        for root, _, files in os.walk(self.dir_path, topdown=self.topdown):
            if not recursive and root != self.dir_path:
                continue
            for f_name in files:
                yield os.path.join(root, f_name)

    def iter_dirs(self, recursive=True):
        for root, dirs, _ in os.walk(self.dir_path, topdown=self.topdown):
            if not recursive and root != self.dir_path:
                continue
            for d_name in dirs:
                yield os.path.join(root, d_name)

    # Internal helpers using the iterators
    def _apply_file_action_by_condition(
        self, action_func, condition_func, recursive=True
    ):
        for f_path in self.iter_files(recursive=recursive):
            if condition_func(f_path):
                action_func(f_path)

    def _apply_dir_action_by_condition(
        self, action_func, condition_func, recursive=True
    ):
        for d_path in self.iter_dirs(recursive=recursive):
            if condition_func(d_path):
                action_func(d_path)

    # interfaces exposed
    def del_empty_sub_dir(self):
        """
        remove all empty sub dirs
        """
        self._apply_dir_action_by_condition(
            lambda d_path: os.rmdir(d_path),  # remove dir
            lambda d_path: len(os.listdir(d_path)) == 0,  # if has no child
        )

    def del_empty_file(self):
        """
        remove empty file(file size is zero)
        """
        self._apply_file_action_by_condition(
            lambda f_path: os.remove(f_path),  # remove file
            lambda f_path: os.path.getsize(f_path) == 0,  # if size is zero
        )

    def del_empty_child(self):
        """
        remove empty file or dir(file size is zero, dir has no child)
        """
        # del all empty files firstly because it will cause some dir empty
        self.del_empty_file()
        self.del_empty_sub_dir()

    def list_file(self, recursive=True):
        """
        list files under folder
        if recursive:True,  list all files, including subdirectories' files
        if recursive:False,  only list direct child files
        """
        yield from self.iter_files(recursive=recursive)

    def list_dir(self, recursive=True):
        """
        list folders
        if recursive:True,  list all folders, including subdirectories' folders
        if recursive:False,  only list direct child folders
        """
        yield from self.iter_dirs(recursive=recursive)

    def search_first_file(
        self, compare_func=natural_path_compare, condition_func=None, recursive=True
    ):
        """
        search the first file under folder
        if recursive:True,  search the first file, including subdirectories' files
        if recursive:False,  only search direct child files
        use compare_func to determine order
        use condition_func to filter files
        """
        first_file = None
        for f_path in self.list_file(recursive=recursive):
            if condition_func and not condition_func(f_path):
                continue
            if first_file is None or compare_func(f_path, first_file) < 0:
                first_file = f_path
        return first_file

    def search_first_dir(
        self, compare_func=natural_path_compare, condition_func=None, recursive=True
    ):
        """
        search the first dir under folder
        if recursive:True,  search the first dir, including subdirectories' dirs
        if recursive:False,  only search direct child dirs
        use compare_func to determine order
        use condition_func to filter dirs
        """
        first_dir = None
        for d_path in self.list_dir(recursive=recursive):
            if condition_func and not condition_func(d_path):
                continue
            if first_dir is None or compare_func(d_path, first_dir) < 0:
                first_dir = d_path
        return first_dir    

    def search_last_file(
        self, compare_func=natural_path_compare, condition_func=None, recursive=True
    ):
        """
        search the last file under folder
        if recursive:True,  search the last file, including subdirectories' files
        if recursive:False,  only search direct child files
        use compare_func to determine order
        use condition_func to filter files
        """
        last_file = None
        for f_path in self.list_file(recursive=recursive):
            if condition_func and not condition_func(f_path):
                continue
            if last_file is None or compare_func(f_path, last_file) > 0:
                last_file = f_path
        return last_file    

    def search_last_dir(
        self, compare_func=natural_path_compare, condition_func=None, recursive=True
    ):
        """
        search the last dir under folder
        if recursive:True,  search the last dir, including subdirectories' dirs
        if recursive:False,  only search direct child dirs
        use compare_func to determine order
        use condition_func to filter dirs
        """
        last_dir = None
        for d_path in self.list_dir(recursive=recursive):
            if condition_func and not condition_func(d_path):
                continue
            if last_dir is None or compare_func(d_path, last_dir) > 0:
                last_dir = d_path
        return last_dir

    def create_timestamp_subdir(self):
        """
        Create a subdirectory with the current timestamp under the folder.
        """
        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")  # <-- Fix: use datetime.now()
        subdir_path = os.path.join(self.dir_path, timestamp_str)   # <-- Fix: use self.dir_path
        os.makedirs(subdir_path, exist_ok=True)
        return subdir_path
