from qutil.filesystem import folder
from qutil.log.log import setup_log
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

    folder_instance = folder.FolderHelper()

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


    print("======= Search first file: ========")
    first_file = folder_instance.search_first_file(
        condition_func=lambda f: f.endswith(".py"), recursive=True
    )
    print(first_file)