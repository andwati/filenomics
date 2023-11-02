# Image File Uploader in Flask
A file uploader built with Python, Flask


# Stack
flask
optipng
lepton
# Features
- [x] Metadata Purging: Removes metadata from uploaded files (except color profile and orientation).
- [x] [Space Optimization:](https://optipng.sourceforge.net/) Losslessly compresses PNG and other file formats using optipng.
- [x] [JPEG Compression: Lepton JPEG Compression in Rust.](https://github.com/microsoft/lepton_jpeg_rust)  the Lepton compression library is designed for lossless compression of baseline and progressive JPEGs up to 22%.
- [x] Filename Handling: Generates random URL/filenames using temporary files, or secures user-requested filenames if provided.
- [x] Upload Size Limit: Enforces a predefined maximum size limit for each uploaded file.
- [x] Extension Control: Restricts uploads to only allow specific file extensions.
- [x] Authentication: Requires a password to be included in the cURL request for uploading files.
- [x] URL Response: Returns the URL pointing to the successfully uploaded file.
- [ ] Write tests for coverage

# Building

