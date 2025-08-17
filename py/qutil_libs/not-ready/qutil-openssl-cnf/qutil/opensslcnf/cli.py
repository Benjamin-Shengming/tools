from qutil.opensslcnf.parser import OpensslCnf
import argparse
from qutil.log.log import setup_logger 
from loguru  import logger

def parse_args(): 
    parser = argparse.ArgumentParser(description="Sample CLI show openssl configuration")
    parser.add_argument("--cnf", default= "/usr/lib/ssl/openssl.cnf", help="path to openssl configuration")
    parser.add_argument("--debug", default= False, action="store_true", help="show debug information")
    args = parser.parse_args()
    setup_logger(console_log=args.debug, level="DEBUG" if args.debug else "INFO")
    return args
    
def main():
    args = parse_args()
    cnf = OpensslCnf.load(args.cnf)
    logger.debug(f"Loaded openssl configuration from {args.cnf}")
    logger.debug(f"Configuration: {cnf}")
    cnf.print_ast_tree()


