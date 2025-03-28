#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
class FolderHelper(object):
    '''
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
    '''
    def __init__(self, folder_path, topdown=True):
        self.dir_path = folder_path
        self.topdown = topdown

    #  internal help functions to iterate files/folders and apply action
    def _apply_action_by_condition(self, action_func, condition_func):
        '''action_func and condition_func accept a path as first parameter'''
        for root, dirs, files in os.walk(self.dir_path, topdown=self.topdown):
            # handle files
            for f_name in files:
                f_path = os.path.join(root, f_name)
                if condition_func(f_path):
                    action_func(f_path)
            # handle dirs
            for d_name in dirs:
                d_path = os.path.join(root, d_name)
                if condition_func(d_path):
                    action_func(d_path)

    def _apply_file_action_by_condition(self, action_func, condition_func):
        '''action_func and condition_func accept a path as first parameter'''
        for root, _, files in os.walk(self.dir_path, topdown=self.topdown):
            # handle files
            for f_name in files:
                f_path = os.path.join(root, f_name)
                if condition_func(f_path):
                    action_func(f_path)

    def _apply_dir_action_by_condition(self, action_func, condition_func):
        '''action_func and condition_func accept path as first parameter'''
        for root, dirs, _ in os.walk(self.dir_path, topdown=self.topdown):
            # handle dirs
            for d_name in dirs:
                d_path = os.path.join(root, d_name)
                if condition_func(d_path):
                    action_func(d_path)

    # interfaces exposed
    def del_empty_sub_dir(self):
        '''
        remove all empty sub dirs
        '''
        self._apply_dir_action_by_condition(
            lambda d_path: os.rmdir(d_path),  # remove dir
            lambda d_path: len(os.listdir(d_path)) == 0  # if has no child
        )

    def del_empty_file(self):
        '''
        remove empty file(file size is zero)
        '''
        self._apply_file_action_by_condition(
            lambda f_path: os.remove(f_path),  # remove file
            lambda f_path: os.path.getsize(f_path) == 0  # if size is zero
        )

    def del_empty_child(self):
        '''
        remove empty file or dir(file size is zero, dir has no child)
        '''
        # del all empty files firstly because it will cause some dir empty
        self.del_empty_file()
        self.del_empty_sub_dir()

    def list_file(self, recursive=True):
        '''
        list files under folder
        if recursive:True,  list all files, including subdirectories' files
        if recursive:False,  only list direct child files
        '''
        for root, _, files in os.walk(self.dir_path, topdown=self.topdown):
            if not recursive and root != self.dir_path:
                continue
            for f_name in files:
                f_path = os.path.join(root, f_name)
                yield f_path

    def list_dir(self, recursive=True):
        '''
        list folders
        if recursive:True,  list all folders, including subdirectories' folders
        if recursive:False,  only list direct child folders
        '''
        for root, dirs, _ in os.walk(self.dir_path, topdown=self.topdown):
            if not recursive and root != self.dir_path:
                continue
            # handle folder
            for d_name in dirs:
                d_path = os.path.join(root, d_name)
                yield d_path
