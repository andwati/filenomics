"""
configs
"""
ALLOWED_EXTENSIONS = set(
    [
        "txt",
        "pdf",
        "png",
        "jpg",
        "jpeg",
        "gif",
        "webm",
        "mp4",
        "zip",
        "rar",
        "doc",
        "docx",
        "flac",
        "mp3",
        "bmp",
        "pnm",
        "tiff",
        "3gp",
        "f4v",
        "m4a",
        "m4p",
        "m4v",
        "mov",
        "psd",
        "tiff",
        "tif",
        "mkv",
        "deb",
        "ogg",
        "sh",
        "aiff",
        "svg",
        "dmg",
        "heif",
        "heic",
    ]
)

OPTIPNG_EXTENSIONS = set(["png", "bmp", "gif", "pnm", "tiff"])

PURGE_EXTENSIONS = set(
    [
        "3gp",
        "f4v",
        "m4a",
        "m4p",
        "pdf",
        "gif",
        "jpg",
        "jpeg",
        "m4v",
        "mov",
        "mp4",
        "psd",
        "tiff",
        "tif",
        "png",
    ]
)

# Files that modern browsers should be able to show on the browser without the need to download them
STREAMABLE_EXTENSIONS = set(
    [
        "png",
        "bmp",
        "gif",
        "tiff",
        "mov",
        "mp4",
        "3gp",
        "jpg",
        "jpeg",
        "ogg",
        "mp3",
        "m4a",
        "pdf",
        "gif",
        "txt",
        "webm",
    ]
)
