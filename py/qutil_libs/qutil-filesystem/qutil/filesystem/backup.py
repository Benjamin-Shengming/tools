#!/usr/bin/env python3

# contains class Backup class which can backup files or folders and restore them to original path
import os
import shutil
from datetime import datetime
from pathlib import Path


def is_child(child_path, parent_path):
    child = Path(child_path).resolve()
    parent = Path(parent_path).resolve()
    try:
        child.relative_to(parent)
        return True
    except ValueError:
        return False


class Backup:
    def __init__(self, backup_path):
        self.backup_path = backup_path

    def backup_one(self, src_path):
        """
        Backup a single file or folder to the destination folder.
        """
        src_path = os.path.abspath(src_path)
        if not os.path.exists(src_path):
            raise FileNotFoundError(f"Source path '{src_path}' does not exist.")
        # treat the backup path as the new root of src_path
        # eg: /home/service/a.txt ==>  dest/home/service/a.txt
        dest_path = os.path.join(self.backup_path, src_path)

        (
            shutil.copytree(src_path, dest_path)
            if os.path.isdir(src_path)
            else shutil.copy2(src_path, dest_path)
        )
        return (src_path, dest_path)

    def restore_one(self, r_path):
        """r_path could be source path or dest path
        Restore a single file or folder from the destination folder to its original location.
        """
        r_path = os.path.abspath(r_path)
        # rpath is under dest , get rid fo dest prefix to get src_path
        if is_child(r_path, self.backup_path):
            src_path = Path("/") / Path(r_path).relative_to(self.backup_path)
            dest_path = r_path
        else:
            src_path = r_path
            dest_path = os.path.join(self.backup_path, src_path)
        if not os.path.exists(dest_path):
            raise FileNotFoundError(f"Backup file path '{dest_path}' does not exist.")

        (
            shutil.copytree(dest_path, src_path, dirs_exist_ok=True)
            if os.path.isdir(dest_path)
            else shutil.copy2(dest_path, src_path)
        )
        return (dest_path, src_path)

    def backup(self, src_path):
        """
        Backup a/multiple files or folders to the destination folder.
        """
        if src_path is None:
            raise ValueError("src_path cannot be None")

        # is src_path iterable
        try:
            for item in src_path:
                self.backup_one(item)
        except TypeError:
            self.backup_one(src_path)

    def restore(self, src_path):
        """
        Restore files or folders from the destination folder to its original location.
        """
        if src_path is None:
            src_path = self.src_dest_map.keys()

        # is src_path iterable
        try:
            for item in src_path:
                self.restore_one(item)
        except TypeError:
            self.restore_one(src_path)
