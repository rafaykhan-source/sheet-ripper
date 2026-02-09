import argparse

from sheets.utilities import get_spreadsheet_id


def get_args():
    parser = argparse.ArgumentParser(
        prog="sheets",
        description="Download and Upload Google Sheets.",
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-u",
        "--url",
        help="The spreadsheet url.",
    )
    group.add_argument(
        "-id",
        "--identifier",
        help="The spreadsheet identifier.",
    )
    parser.add_argument(
        "-t",
        "--target",
        default="",
        help="The target sheet name. Defaults to first sheet of the spreadsheet.",
    )
    parser.add_argument(
        "-r",
        "--range",
        default="A:Z",
        help="The range to copy.",
    )
    args = parser.parse_args()
    if args.url:
        args.identifier = get_spreadsheet_id(args.url)
    if args.target:
        args.range = args.target + "!" + args.range
    return args
