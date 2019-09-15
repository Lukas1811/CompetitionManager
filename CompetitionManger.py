from flask import Flask

from Backend.logger import Logger as log
from Backend.API import API

DATABASE_FOLDER = "./Database/"

if __name__ == "__main__":
    app = Flask(__name__)

    api = API(app, DATABASE_FOLDER)

    log.info("Starting server...")
    app.run()