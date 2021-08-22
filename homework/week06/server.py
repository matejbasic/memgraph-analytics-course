from flask import Flask

from graph_db import establish_connection
from dataset import generate_data

app = Flask("server")


@app.route('/')
def index():
    return 'Hello, World!'


def main():
    establish_connection()
    generate_data()
    app.run()


if __name__ == '__main__':
    main()
