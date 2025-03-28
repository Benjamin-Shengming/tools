#!/usr/bin/env python3

import argparse
from iter_folder import filter_files, list_files, apply_command_to_files 
from fac import FuncAsCmd
from lib.color_print import ColorPrint 
from lib.log import setup_logger  


log = setup_logger('ffmpeg_logger')
pr = ColorPrint(log)
fac = FuncAsCmd()


@fac.as_cmd(default=True)
def max_vol(args):
  pr.print("===== Max volume =====")
  pass 

@fac.as_cmd()
def to_mp4(args):
  pr.print("===== to MP4 =====")
  files = list_files(args.path)
  files = filter_files(files, lambda f: f.endswith('.mp4') or f.endswith('.mkv') or f.endswith('.avi'))
  files = filter_files(files, lambda f: "output" not in f)
  apply_command_to_files(files, "ffmpeg -y -i '{0}' -c:v copy -c:a copy '{0}.output.mp4'")

@fac.as_cmd()
def to_mp3(args):
  pr.print("===== to MP3 =====")
  files = list_files(args.path)
  files = filter_files(files, lambda f: f.endswith('.mp4') or f.endswith('.mkv') or f.endswith('.avi'))
  files = filter_files(files, lambda f: "output" not in f and "mp3" not in f)
  apply_command_to_files(files, "ffmpeg -y -i '{0}' -c:a libmp3lame -q:a 0 -map a '{0}'.output.mp3")










#==================================================
# must be last 2 functions
#==================================================
def parse_args():
  parser = argparse.ArgumentParser(description="Apply a command to all files in a folder.")
  parser.add_argument("-p", "--path", type=str, help="Path to the folder containing the files.")
  fac.add_funcs_as_cmds(parser, long_cmd_str="--command", short_cmd_str="-c")
  args = parser.parse_args()
  return args

def main():
  args = parse_args()
  fac.call_func_by_name(args.command, args)


if __name__ == "__main__":
  main()