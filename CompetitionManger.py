from flask import Flask

from Backend.logger import Logger as log
from Backend.API import API

from Frontend.Frontend import Frontend

DATABASE_FOLDER = "./Database/"
UPLOAD_FOLDER = "./Database/"
ALLOWED_EXTENSIONS = set(["json"])

if __name__ == "__main__":
    app = Flask(__name__, template_folder=Frontend.HTML_DIR)
    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

    api = API(app, DATABASE_FOLDER)
    frontend = Frontend(app)

    log.info("Starting server...")
    app.run()