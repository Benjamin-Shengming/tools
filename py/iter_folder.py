#!/usr/bin/env python3
import os
import sys
import subprocess
import argparse
from lib.color_print import ColorPrint
from lib.log import setup_logger
from lib.local_shell import run_cmd 

log = setup_logger('iter_folder_logger')
pr = ColorPrint(log)

def filter_files(files, filter_func):
    """Filter files using a lambda function."""
    return [file for file in files if filter_func(file)]

def filter_files_by_ext(files, ext):
    """Filter files by extension."""
    return [file for file in files if file.endswith(ext)]

def list_files(folder_path, recursive=True):
    """List all files in a folder, optionally recursively."""
    file_list = []
    for root, dirs, files in os.walk(folder_path):
        if not recursive:
            dirs.clear()  # Do not recurse into subdirectories
        for file in files:
            file_path = os.path.join(root, file)
            file_list.append(file_path)
    return file_list


def apply_command_to_files(files, command):
    # if it is a single file, apply the command to it
    for file in files:
        # Replace placeholder with the actual file path using string formatting
        formatted_command = command.format(file)
        # Apply the command to the file
        ret = run_cmd(formatted_command, log=pr)
        pr.print(ret)