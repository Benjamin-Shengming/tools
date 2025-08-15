#!/usr/bin/env python3


from qutil.filesystem import folder
from qutil.log.log import setup_logger
import argparse


def main():
    parser = argparse.ArgumentParser(
        description="Sample CLI using qutil.filesystem"
    )
    parser.add_argument(
        "--folder",
        default="./",
        help="Directory path to investigate",
        
    )
    args = parser.parse_args()

    folder_instance = folder.FolderHelper(args.folder)

    print("======= All files: ========")
    for x in folder_instance.list_file(
        recursive=True
    ):
        print(x)  # List files in the current directory

    print("======= All folders: ========")
    for x in folder_instance.list_dir(
        recursive=True
    ):  # List folders in the current directory  
        print(x)

    print("======= Search first folder: ========")
    first_folder = folder_instance.search_first_dir(
        recursive=True
    )
    print(first_folder)

    print("======= Search last folder: ========")
    last_folder = folder_instance.search_last_dir(
         recursive=True
    )
    print(last_folder)


    print("======= Search first file: ========")
    first_file = folder_instance.search_first_file(
        condition_func=lambda f: f.endswith(".rpm"), recursive=True
    )
    print(first_file)

    print("======= Search last file: ========")
    last_file = folder_instance.search_last_file(
        condition_func=lambda f: f.endswith(".rpm"), recursive=True
    )
    print(last_file)