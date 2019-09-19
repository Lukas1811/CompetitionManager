from flask import Flask

from Backend.logger import Logger as log
from Backend.API import API

from Frontend.Frontend import Frontend

DATABASE_FOLDER = "./Database/"

if __name__ == "__main__":
    app = Flask(__name__, template_folder=Frontend.HTML_DIR)

    api = API(app, DATABASE_FOLDER)
    frontend = Frontend(app)

    log.info("Starting server...")
    app.run()