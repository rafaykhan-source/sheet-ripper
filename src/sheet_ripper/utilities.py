import json

# import logging
# from logging.config import dictConfig


def _get_logging_config() -> dict:
    with open("logging.json") as f:
        return json.loads(f.read())


# def get_logger() -> logging.Logger:
#     config = _get_logging_config()
#     dictConfig(config)
#     logger = logging.getLogger(__name__)
#     return logger
#


def get_spreadsheet_id(url: str) -> str:
    return url.split("/")[-2]
