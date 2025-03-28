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

def apply_command_to_files(files, command):
    # if it is a single file, apply the command to it
    for file in files:
        # Replace placeholder with the actual file path using string formatting
        formatted_command = command.format(file)
        # Apply the command to the file
        pr.print(formatted_command)
        ret = run_cmd(formatted_command, log=pr)
        pr.print(ret)