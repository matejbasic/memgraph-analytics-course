from argparse import ArgumentParser


def parse_args():
    parser = ArgumentParser(description="A recipes stream machine powered by Memgraph.")
    parser.add_argument(
        "--interval",
        type=int,
        help="Interval for sending data in seconds.")
    return parser.parse_args()
