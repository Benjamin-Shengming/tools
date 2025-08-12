from qutil.shell import local 
import argparse
import json
from qutil.log import setup_logger 
logger.

def parse_args(): 
    parser = argparse.ArgumentParser(description="Sample CLI using qutil.log")
    parser.add_argument("--command", default= "ls", help="command to run")
    parser.add_argument("--debug", default= False, help="show debug information")
    setup_logger(console_log=args.debug, level="DEBUG" if args.debug else "INFO")
    args = parser.parse_args()
    return args
    
def main():

    if args.debug:
        logger.

    if args.command:
        result = local.run(args.command)
        print(json.dumps(result, indent=2))

