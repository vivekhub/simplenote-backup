import argparse


def ArgSetup():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-v",
        "--verbose",
        help="Print progress messages",
        action="store_true",
        required=False)
    parser.add_argument(
        "-u",
        "--user",
        help="Your simplenote userid",
        type=str,
        action="store",
        required=True)
    parser.add_argument(
        "-p",
        "--password",
        help="Your simplenote password",
        type=str,
        action="store",
        required=True)
    parser.add_argument(
        "-c",
        "--create",
        help="Create a fresh backup",
        default=False,
        action="store_true")

    store_group = parser.add_mutually_exclusive_group(required=True)
    store_group.add_argument(
        "-s",
        "--sqlite",
        default='snbackup.sqlite3',
        help="SQLite3 database where the data will be stored",
        type=str,
        action="store")
    store_group.add_argument(
        "-j",
        "--json",
        help="JSON file where the data will be stored",
        type=str,
        action="store")

    return parser


def ArgProcess(parser):
    return parser.parse_args()
