import uuid

from .config import ALLOWED_EXTENSIONS


def allowed_file(filename):
    """
    Check if the file extension is allowed as well as extensionless files
    """
    return (
        "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    ) or not "." in filename


def generate_random_filename(filename):
    """
    Generate a random filename with the same extension as the original file
    """
    ext = filename.rsplit(".", 1)[1].lower()
    return f"{uuid.uuid4()}.{ext}"
