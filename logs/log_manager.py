import logging

from Ross_git.src.app.config.app_config import get_section


def setup_logger():
    logging_config = get_section("logging")

    log_level_str = logging_config.get("log_level", "INFO").upper()
    log_format = logging_config.get("log_format", "%(asctime)s - %(levelname)s - %(message)s")
    enable_console = logging_config.get("enable_console", "true").lower() == "true"

    log_level = getattr(logging, log_level_str, logging.INFO)
    logger = logging.getLogger()

    if logger.hasHandlers():
        return logger

    formatter = logging.Formatter(log_format)
    logger.setLevel(log_level)

    if enable_console:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        logger.info("Console logging is enabled.")
    else:
        logger.info("Console logging is disabled.")

    return logger
