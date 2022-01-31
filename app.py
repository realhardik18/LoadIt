from flask import Flask, render_template, request
from threading import Thread
from flask.helpers import send_file, url_for
from downloader import downloader
from flask import after_this_request
import os
import io

app = Flask('')


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/result', methods=['POST'])
def result():
    playlist = request.form['playlist']
    file_path = downloader(playlist)
    return_data = io.BytesIO()
    with open(file_path, 'rb') as fo:
        return_data.write(fo.read())
    return_data.seek(0)
    os.remove(file_path)
    return send_file(return_data, mimetype='application/zip',
                     attachment_filename='songs.zip')


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")


@app.errorhandler(500)
def error(e):
    return render_template("500.html")


app.run()
