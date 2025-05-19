#!/usr/bin/env python3

import argparse
from qutil.cli.fac import FuncAsCmd
from qutil.console.color_print import ColorPrint
from qutil.log.log import setup_logger
from qutil.shell.local import run as run_cmd
from qutil.filesystem.folder import FolderHelper
import logging
import os

setup_logger()
pr = ColorPrint()
fac = FuncAsCmd()


def is_video_file(file):
    """Check if the file is a video file."""
    video_exts = ['.mp4', '.mkv', '.avi', '.mov',
                  '.flv', '.wmv', '.webm', '.mpeg', '.mpg', '.m4v']
    for ext in video_exts:
        if file.endswith(ext):
            return True
    return False


def is_audio_file(file):
    """Check if the file is an audio file."""
    audio_exts = ['.mp3', '.wav', '.flac', '.aac', '.ogg']
    for ext in audio_exts:
        if file.endswith(ext):
            return True
    return False


def filter_files(files, i_keywords, e_keywords):
    """Filter files based on include and exclude keywords."""
    if i_keywords:
        files = [f for f in files if include_keywords(
            get_file_name(f), i_keywords)]
    if e_keywords:
        files = [f for f in files if exclude_keywords(
            get_file_name(f), e_keywords)]
    return files


def get_files(folder_path, recursive=True):
    """List all files in a folder, optionally recursively."""
    if os.path.isfile(folder_path):
        return [folder_path]

    fh = FolderHelper(folder_path)
    return fh.list_file(recursive=recursive)


def get_folders(folder_path, recursive=True):
    """List all folders in a folder, optionally recursively."""
    if os.path.isfile(folder_path):
        return [folder_path]

    fh = FolderHelper(folder_path)
    return fh.list_dir(recursive=recursive)


def get_files_and_folders(folder_path, recursive=True):
    """List all files and folders in a folder, optionally recursively."""
    if os.path.isfile(folder_path):
        return [folder_path]

    fh = FolderHelper(folder_path)
    files = fh.list_file(recursive=recursive)
    folders = fh.list_dir(recursive=recursive)
    return list(files) + list(folders)


def get_opertion_objects(args):
    """Get the operation type."""
    if args.type == "file":
        return get_files(args.path, args.recursive)
    elif args.type == "folder":
        return get_folders(args.path, args.recursive)
    elif args.type == "both":
        return get_files_and_folders(args.path, args.recursive)
    else:
        raise ValueError(
            "Invalid operation type. Use 'file', 'folder', or 'both'.")


def get_file_name(file):
    """Get the file name without path but with ext."""
    return os.path.basename(file)


def detect_max_vol(file):
    """Detect the max volume of a file."""
    command = f"ffmpeg -hide_banner -i '{
        file}' -af 'volumedetect' -vn -sn -dn -f null -"
    ret = run_cmd(command, log=pr)
    lines = ret.split("\n")
    for line in lines:
        if "max_volume" in line and ":" in line:
            vol = line.split(":")[-1].strip().split(" ")[-2].strip()
            return float(vol)


def new_ext(file, ext):
    """Change the file extension."""
    return os.path.splitext(file)[0] + ext


def include_keywords(file, kws):
    """Check if the file name contains all keywords."""
    for keyword in kws:
        if keyword not in file:
            return False
    return True


def exclude_keywords(file, kws):
    """Check if the file name contains any keywords."""
    for keyword in kws:
        if keyword in file:
            return False
    return True
# ==================================================
# ffmpeg commands


@fac.as_cmd(default=True)
def rename(args):
    pr.print("===== rename files=====")
    files = get_files_and_folders(args.path, args.recursive)
    files = [x for x in files if is_video_file(x) or is_audio_file(x)]

    # detect volume
    ret = list(map(detect_max_vol, files))
    for f, v in zip(files, ret):
        pr.print(f"{f}: {v}dB")


@fac.as_cmd()
def remove(args):
    pr.print("===== Delete Files=====")
    files = get_files(args.path, args.recursive)
    files = filter_files(files, args.include, args.exclude)
    commands = list(map(lambda x: "rm '{0}'".format(x), files))
    for c in commands:
        ret = run_cmd(c, log=pr)
        pr.print(ret)


@fac.as_cmd()
def run_cmd_str(args):
    pr.print("===== Run Command String =====")
    files = get_opertion_objects(args)
    files = [x for x in files if include_keywords(get_file_name(
        x),  args.include) and exclude_keywords(get_file_name(x), args.exclude)]
    commands = list(map(lambda x: args.cmdstr.format("'{}'".format(x)), files))
    fails = []
    for f, cmd in zip(files, commands):
        ret = run_cmd(cmd, warn=True)
        if ret["exit_code"] != 0:
            pr.fail(f"{cmd}")
            pr.fail(f"{ret['stderr'] + ret['stdout']}")
            fails.append(f)
        else:
            pr.success(f"{cmd}")
            pr.success(f"{ret['stdout'] + ret['stderr']}")
        pr.print("\n")
    if fails:
        for f in fails:
            pr.fail(f"{f}")


# ==================================================
# must be last 2 functions
# ==================================================
def parse_args():
    parser = argparse.ArgumentParser(
        description="Apply a command to all files in a folder.")
    parser.add_argument("-p", "--path", type=str,
                        help="Path to the folder containing the files.")
    parser.add_argument("-r", "--recursive", action="store_true",
                        default=False,
                        help="Path to the folder containing files.")
    parser.add_argument("-i", "--include", nargs='+',
                        default=[],
                        help="keywords in file name should include")
    parser.add_argument("-e", "--exclude", nargs='+', default=[],
                        help="keywords in file name should be excluded")

    parser.add_argument("-s", "--cmdstr", default=None,
                        help="command string to be executed for each file, use {} as placeholder")
    parser.add_argument("-t", "--type", default="folder",
                        help="operate on folder or file, or both", )
    parser.add_argument("--debug", default=False,
                        help="debug mode", action="store_true")
    fac.add_funcs_as_cmds(parser, long_cmd_str="--command", short_cmd_str="-c")
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    if args.debug:
        pr.info("Debug mode enabled")
        setup_logger(level="DEBUG")
    else:
        setup_logger(level="INFO")
    fac.call_func_by_name(args.command, args)


if __name__ == "__main__":
    main()
