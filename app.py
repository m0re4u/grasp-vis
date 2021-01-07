import os

import data_loader as dl
from dotenv import load_dotenv
from flask import Flask, render_template

load_dotenv()


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])


@app.route('/')
def hello():
    txt = dl.load_naf('data/test.ec.final.naf').get_raw()
    return render_template('index.html', text=txt)

if __name__ == '__main__':
    app.run()
