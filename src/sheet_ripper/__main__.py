import logging

from sheet_ripper.cli import get_args
from sheet_ripper.service import SheetService

# from sheet_ripper.utilities import get_logger
from sheet_ripper.writer import CSVWriter


def configure_logging() -> logging.Logger:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%m/%d/%Y %I:%M:%S %p",
    )
    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)
    logger.debug("Loaded logging configuration.")
    return logger


def main() -> None:
    logger = configure_logging()
    args = get_args()
    logger.info("Retrieved arguments: id %s | range: %s", args.identifier, args.range)

    service = SheetService()
    service.build_sheets()
    logger.info("Built Sheet Service.")

    values = service.get_sheet_values(args.identifier, args.range)

    writer = CSVWriter()
    writer.write("results.csv", values)
    logger.info("Wrote results.")


if __name__ == "__main__":
    main()
