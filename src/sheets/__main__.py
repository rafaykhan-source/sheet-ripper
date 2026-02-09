from sheets.cli import get_args
from sheets.service import SheetService
from sheets.utilities import get_logger
from sheets.writer import CSVWriter


def main() -> None:
    logger = get_logger()
    logger.debug("Loaded logging configuration.")

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
