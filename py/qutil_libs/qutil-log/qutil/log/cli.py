from loguru import logger
from qutil.log.log import setup_logger 


def main():
    print("Log example")
    setup_logger(log_file="example.log", console_log=True, level="DEBUG")
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")

if __name__ == "__main__":
    main()
