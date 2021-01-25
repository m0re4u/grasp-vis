import os
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, current_app

import grasp_app.utils.data_loader as dl
load_dotenv()


def create_app(config_class=os.environ['APP_SETTINGS']):
    app = Flask(__name__, static_folder=str(Path('static').resolve()))
    app.config.from_object(config_class)

    from grasp_app.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app
