from argparse import ArgumentParser, Namespace


def parse_args() -> Namespace:
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--app-host", default="0.0.0.0", help="Allowed host addresses.")
    parser.add_argument("--app-port", default=5000, type=int, help="App port.")
    parser.add_argument("--template-folder", default="public/template", help="The folder with flask templates.")
    parser.add_argument("--static-folder", default="public", help="The folder with flask static files.")
    parser.add_argument("--debug", default=True, action="store_true", help="Run web server in debug mode")
    return parser.parse_args()


args = parse_args()
