from qutil.filesystem import folder
import argparse


def main():
    parser = argparse.ArgumentParser(
        description="Sample CLI using qutil.filesystem"
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List files in the current directory",
    )
    args = parser.parse_args()

    folder_instance = folder.FolderHelper()
    folder_instance.list_file(
        recursive=True
    )  # List files in the current directory
