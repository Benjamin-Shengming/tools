#!/usr/bin/env python3

import argparse

from iter_folder import filter_files, list_files, apply_command_to_files 

def parse_args():
  parser = argparse.ArgumentParser(description="Apply a command to all files in a folder.")
  parser.add_argument("-p", "--path", type=str, help="Path to the folder containing the files.")
  parser.add_argument("-c", "--command", type=str, 
                      default="ffmpeg -i '{0}' -c:v copy -c:a copy '{0}'.output.mp4",
                      help="Command to apply to each file, use {} as a placeholder for the file path.")
  args = parser.parse_args()
  return args

def main():
  args = parse_args()
  files = list_files(args.path)
  files = filter_files(files, lambda f: f.endswith('.mp4') or f.endswith('.mkv') or f.endswith('.avi'))
  apply_command_to_files(files, args.command)

if __name__ == "__main__":
  main()