import configparser
import os
import re
import subprocess
from tempfile import mkstemp

from dotenv import load_dotenv
from flask import (
    Flask,
    abort,
    flash,
    make_response,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
)
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename

from filenomics.process import post_process
from filenomics.utils import allowed_file, generate_random_filename

from .config import ALLOWED_EXTENSIONS, STREAMABLE_EXTENSIONS

load_dotenv()


# Define BASE_DIR as the absolute path to the project's root directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

STATIC_DIR = os.path.join(BASE_DIR, "static")
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")

config = configparser.ConfigParser()
config.read(os.path.join(BASE_DIR, "filenomics.ini"))
# Get the PWHASH from the configuration file
# Hashed string generated with werkzeug.security.generate_password_hash
PWHASH = config.get("security", "PWHASH")

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 10 * 1000 * 1000
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")


@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        # check if the post request has the password part
        password = request.form.get("password")
        if not check_password_hash(PWHASH, password):
            flash("Invalid password")
            return abort(403)

        # check if the post request has the file part
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)

        file = request.files["file"]
        custom_extension = request.form.get("custom_extension")
        preserve_filename = request.form.get("preserve_filename")
        custom_filename = request.form.get("custom_filename")
        do_not_redirect = request.form.get("do_not_redirect")

        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)

        if file and (allowed_file(file.filename) or custom_extension):
            if custom_extension in ALLOWED_EXTENSIONS:
                extension = custom_extension
            else:
                if re.search(r"\..", file.filename):
                    extension = file.filename.rsplit(".", 1)[1].lower()
                else:
                    extension = "txt"

            if custom_filename:
                filename = secure_filename(custom_filename) + "." + extension
                output = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                if os.path.exists(output):
                    # if it exists create a temporary file with a unique name
                    fd, output = mkstemp(
                        prefix="",
                        dir=app.config["UPLOAD_FOLDER"],
                        suffix="_" + filename,
                    )
                    os.close(fd)

                    filename = os.path.basename(output)
                file.save(output)
            elif preserve_filename:
                filename = secure_filename(file.filename)
                output = os.path.join(app.config["UPLOAD_FOLDER"], filename)

                if os.path.exists(output):
                    output = mkstemp(
                        prefix="",
                        dir=app.config["UPLOAD_FOLDER"],
                        suffix="_" + filename,
                    )[1]
                file.save(output)
            else:
                output = mkstemp(
                    prefix="",
                    dir=app.config["UPLOAD_FOLDER"],
                    suffix="_" + generate_random_filename(file.filename),
                )[1]
                filename = os.path.basename(output)
                file.save(output)

                post_process(extension, output)

            if do_not_redirect:
                full_url = str(request.base_url) + str(filename) + ""
                return full_url
            else:
                if extension.lower() in STREAMABLE_EXTENSIONS:
                    return redirect(url_for("download_file", filename=filename))

        else:
            return abort(403)

    return render_template("index.n.html")


@app.route("/uploads/<filename>")
def download_file(filename):
    extension = filename.rsplit(".", 1)[1].lower()
    filename_without_extension = filename.rsplit(".", 1)[0]

    # if its jpeg try to find the .lep file that matches the name and stream that into the browser
    if extension == "jpeg" or extension == "jpg":
        app.logger.info(
            "Attempting to stream .lep file for" + filename_without_extension
        )
        matching_lep = os.path.join(
            app.config["UPLOAD_FOLDER"], filename_without_extension + ".lep"
        )

        if os.path.isfile(matching_lep):
            app.logger.info(
                f"Found matching .lep file for {filename_without_extension}"
            )
            args = ["lepton", "-"]
            with open(matching_lep, "rb") as inf:
                proc = subprocess.Popen(args, stdout=subprocess.PIPE, stdin=inf)
                output = subprocess.Popen.communicate(proc)
                proc.wait()
                app.logger.info("Lepton finished processing" + filename)
            response = make_response(output)
            response.headers.set("Content-Type", "image/jpeg")
            return response

    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)
