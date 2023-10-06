import os
import subprocess

from .config import OPTIPNG_EXTENSIONS, PURGE_EXTENSIONS
from .main import app


def post_process(extension, output):
    # Remove metadata from files (images and videos)
    if extension.lower() in PURGE_EXTENSIONS:
        app.logger.info("Attempting exiftool purge")
        subprocess.call(
            [
                "exiftool",
                "-overwrite_original",
                "-all=",
                "-tagsfromfile",
                "@",
                "-orientation",
                "-icc_profile",
                output,
            ]
        )

    # optimize png,tiff
    if extension.lower() in OPTIPNG_EXTENSIONS:
        app.logger.info("Optimising PNG with optipng")
        subprocess.call(["optipng", output])

    # optimize jpg with lepton
    if extension.lower() in ("jpg", "jpeg"):
        filename_without_extension = output.rsplit(".", 1)[0]
        app.logger.info("compressing JPG with lepton")
        subprocess.call(["lepton", output])
        #  check if .lep file was successfully created(lepton will create a 0 bit file even if it fails)
        if (
            os.path.isfile(
                os.path.join(
                    app.config["UPLOAD_FOLDER"], filename_without_extension + ".lep"
                )
            )
            and os.stat(
                os.path.join(
                    app.config["UPLOAD_FOLDER"], filename_without_extension + ".lep"
                )
            )
            != 0
        ):
            os.remove(output)
        else:
            app.logger.error("No matching .lep found, returning .jpg")
