from flask import Flask, render_template, request
from threading import Thread
from flask.helpers import send_file, url_for
from downloader import downloader

app = Flask('')


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/result', methods=['POST'])
def result():
    playlist = request.form['playlist']
    zip_path = downloader(playlist)
    return send_file(zip_path, as_attachment=True)


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")


@app.errorhandler(500)
def error(e):
    return render_template("500.html")


app.run()
