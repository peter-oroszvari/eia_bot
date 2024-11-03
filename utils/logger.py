import logging


def setup_logger():
    logger = logging.getLogger("EIA_bot")
    logger.setLevel(logging.INFO)

    # Only add handler if it doesn't already exist
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


def get_logger(name=None):
    if name is None:
        return logging.getLogger("EIA_bot")
    else:
        child_logger = logging.getLogger(f"EIA_bot.{name}")
        child_logger.setLevel(logging.INFO)  # Ensure child loggers also log INFO
        return child_logger
