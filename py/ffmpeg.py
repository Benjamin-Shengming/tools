#!/usr/bin/env python3

import argparse
import os
from qutil.cli.fac import FuncAsCmd
from qutil.console.color_print import ColorPrint
from qutil.log.log import setup_logger
from qutil.shell.local import run as run_cmd
from qutil.filesystem.folder import FolderHelper


setup_logger()
pr = ColorPrint()
fac = FuncAsCmd()


def is_video_file(file):
    """Check if the file is a video file."""
    video_exts = [
        ".mp4",
        ".mkv",
        ".avi",
        ".mov",
        ".flv",
        ".wmv",
        ".webm",
        ".mpeg",
        ".mpg",
        ".m4v",
    ]
    for ext in video_exts:
        if file.endswith(ext):
            return True
    return False


def is_audio_file(file):
    """Check if the file is an audio file."""
    audio_exts = [".mp3", ".wav", ".flac", ".aac", ".ogg"]
    for ext in audio_exts:
        if file.endswith(ext):
            return True
    return False


def get_files(folder_path, recursive=True):
    """List all files in a folder, optionally recursively."""
    if os.path.isfile(folder_path):
        return [folder_path]

    fh = FolderHelper(folder_path)
    return fh.list_file(recursive=recursive)


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


# ==================================================
# ffmpeg commands


@fac.as_cmd(default=True)
def detect_vol(args):
    pr.print("===== detect max volume =====")
    files = get_files(args.path, args.recursive)
    files = [x for x in files if is_video_file(x) or is_audio_file(x)]

    # detect volume
    ret = list(map(detect_max_vol, files))
    for f, v in zip(files, ret):
        pr.print(f"{f}: {v}dB")


@fac.as_cmd(default=False)
def max_vol(args):
    pr.print("===== Max volume =====")
    files = get_files(args.path, args.recursive)
    files = [x for x in files if is_video_file(x) or is_audio_file(x)]

    # detect volume
    ret = list(map(detect_max_vol, files))
    for f, v in zip(files, ret):
        if v and v >= 0:
            continue
        new_file = new_ext(f, ".output.mp4")
        cmd = f"""ffmpeg -i '{f}' -af "volume={-v}
            dB" -c:v copy '{new_file}' """
        ret = run_cmd(cmd, log=pr)


@fac.as_cmd()
def to_mp4(args):
    pr.print("===== to MP4 =====")
    files = get_files(args.path, args.recursive)
    files = [x for x in files if is_video_file(x)]
    files = [x for x in files if "output" not in x]
    commands = list(
        map(
            lambda x: "ffmpeg -y -i '{0}' -c:v copy -c:a copy '{0}.output.mp4'".format(
                x
            ),
            files,
        )
    )
    rets = list(map(lambda x: run_cmd(x, log=pr), commands))
    for x in rets:
        if x:
            pr.print(x)


@fac.as_cmd()
def to_mp3(args):
    pr.print("===== to MP3 =====")
    files = get_files(args.path, args.recursive)
    files = [x for x in files if is_video_file(x) or is_audio_file(x)]
    pr.print(files)
    files = [x for x in files if "mp3" not in x]
    commands = list(
        map(
            lambda x: "ffmpeg -y -i '{0}' -c:a libmp3lame -q:a 0 -map a '{0}.mp3'".format(
                x
            ),
            files,
        )
    )
    for cmd in commands:
        run_cmd(cmd, log=pr)


# ==================================================
# must be last 2 functions
# ==================================================
def parse_args():
    parser = argparse.ArgumentParser(
        description="Apply a command to all files in a folder."
    )
    parser.add_argument(
        "-p",
        "--path",
        type=str,
        help="Path to the folder containing the files.",
    )
    parser.add_argument(
        "-r",
        "--recursive",
        action="store_true",
        default=False,
        help="Path to the folder containing the files.",
    )
    fac.add_funcs_as_cmds(parser, long_cmd_str="--command", short_cmd_str="-c")
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    fac.call_func_by_name(args.command, args)


if __name__ == "__main__":
    main()
