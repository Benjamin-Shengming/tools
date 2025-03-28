#!/usr/bin/env python3

import argparse
from utils import apply_command_to_files 
from lib.fac import FuncAsCmd
from lib.color_print import ColorPrint 
from lib.log import setup_logger  
import os
from lib.folder import FolderHelper


log = setup_logger('ffmpeg_logger')
pr = ColorPrint(log)
fac = FuncAsCmd()

def is_video_file(file):
  """Check if the file is a video file."""
  return file.endswith('.mp4') or file.endswith('.mkv') or file.endswith('.avi') or file.endswith('.mov') or file.endswith('.flv') 

def is_audio_file(file):
  """Check if the file is an audio file."""
  return file.endswith('.mp3') or file.endswith('.wav') or file.endswith('.flac') or file.endswith('.aac') or file.endswith('.ogg') 


def get_files(folder_path, recursive=True):
  """List all files in a folder, optionally recursively."""
  if os.path.isfile(folder_path):
    return [folder_path]

  fh = FolderHelper(folder_path)
  return fh.list_file(recursive=recursive)

@fac.as_cmd(default=True)
def max_vol(args):
  pr.print("===== Max volume =====")
  pass 

@fac.as_cmd()
def to_mp4(args):
  pr.print("===== to MP4 =====")
  files = get_files(args.path, args.recursive)
  files = [x for x in files if is_video_file(x)] 
  files = [x for x in files if "output" not in x] 
  apply_command_to_files(files, "ffmpeg -y -i '{0}' -c:v copy -c:a copy '{0}.output.mp4'")

@fac.as_cmd()
def to_mp3(args):
  pr.print("===== to MP3 =====")
  files = get_files(args.path, args.recursive)
  files = [x for x in files if is_video_file(x) or is_audio_file(x)] 
  files = [x for x in files if "output" not in x] 
  files = [x for x in files if "mp3" not in x] 
  apply_command_to_files(files, "ffmpeg -y -i '{0}' -c:a libmp3lame -q:a 0 -map a '{0}.output.mp3'")










#==================================================
# must be last 2 functions
#==================================================
def parse_args():
  parser = argparse.ArgumentParser(description="Apply a command to all files in a folder.")
  parser.add_argument("-p", "--path", type=str, help="Path to the folder containing the files.")
  parser.add_argument("-r", "--recursive", action="store_true", default=False, help="Path to the folder containing the files.")
  fac.add_funcs_as_cmds(parser, long_cmd_str="--command", short_cmd_str="-c")
  args = parser.parse_args()
  return args

def main():
  args = parse_args()
  fac.call_func_by_name(args.command, args)


if __name__ == "__main__":
  main()