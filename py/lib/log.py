import logging
import logging.handlers

def setup_logger(name, log_file=None, level=logging.INFO):
    """Function to setup a logger with syslog and optional file logging"""
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

    # Syslog handler
    syslog_handler = logging.handlers.SysLogHandler(address='/dev/log')
    syslog_handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(syslog_handler)

    # File handler (optional)
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger