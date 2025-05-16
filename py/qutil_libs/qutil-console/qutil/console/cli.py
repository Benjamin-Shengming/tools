from qutil.console import core
import argparse

def main():
    parser = argparse.ArgumentParser(description="Sample CLI using qutil.console")
    parser.add_argument("--greet", action="store_true", help="Print a greeting")
    args = parser.parse_args()

    if args.greet:
        print(core.hello())
