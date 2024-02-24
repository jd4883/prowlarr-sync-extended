import logging


logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
)
logging.Formatter("[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s")

def log_print(log: str, level: "info"):
    if level == "info":
        logging.info(log)
    elif level == "error":
        logging.error(log)
    elif level == "debug":
        logging.debug(log)
