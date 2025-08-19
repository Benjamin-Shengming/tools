import argparse
import json
from qutil.log.log import setup_logger 

def parse_args(): 
    parser = argparse.ArgumentParser(description="Sample CLI using qutil.log")
    parser.add_argument("--command", default= "ls", help="command to run")
    parser.add_argument("--debug", default= False, action="store_true", help="show debug information")
    args = parser.parse_args()
    setup_logger(console_log=args.debug, level="DEBUG" if args.debug else "INFO")
    return args
    
def main():
    args = parse_args()
    pass

