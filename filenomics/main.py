import os
from pathlib import Path

from dotenv import load_dotenv
from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
)
from werkzeug.utils import secure_filename

load_dotenv()


# Define BASE_DIR as the absolute path to the project's root directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

STATIC_DIR = os.path.join(BASE_DIR, "static")
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")


ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}


app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 10 * 1000 * 1000
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def generate_random_filename(filename):
    import uuid

    ext = filename.rsplit(".", 1)[1].lower()
    return f"{uuid.uuid4()}.{ext}"


@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        # check if the post request has the file part
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)

        file = request.files["file"]

        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = generate_random_filename(file.filename)
            safe_filename = secure_filename(filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], safe_filename))
            return redirect(url_for("download_file", name=safe_filename))
        else:
            flash("Invalid file type")
            return redirect(request.url)

    return render_template("index.html")


@app.route("/uploads/<name>")
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)
