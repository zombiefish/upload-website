#!/usr/bin/env python3
"""
Simple file-upload website
Uses Flask. Run with: python3 app.py
"""

import os
from pathlib import Path
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    send_from_directory,
    abort,
)
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge

# ---------- Configuration ----------
UPLOAD_FOLDER = Path(__file__).parent / "uploads"
ALLOWED_EXTENSIONS = {
    "txt", "pdf", "png", "jpg", "jpeg", "gif", "webp",
    "zip", "tar", "gz", "bz2", "xz",
    "mp3", "mp4", "webm", "ogg",
    "doc", "docx", "xls", "xlsx", "ppt", "pptx",
    "csv", "json", "md", "log",
}
MAX_CONTENT_LENGTH = 2 * 1024 * 1024 * 1024  # 2 GB
# MAX_CONTENT_LENGTH = 32 * 1024 * 1024  # 32 MB

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = str(UPLOAD_FOLDER)
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH
app.secret_key = os.environ.get("SECRET_KEY", "change-me-in-production-please")

# Ensure upload directory exists
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)


def allowed_file(filename: str) -> bool:
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


@app.route("/")
def index():
    files = sorted(
        [f.name for f in UPLOAD_FOLDER.iterdir() if f.is_file()],
        key=str.lower,
    )
    return render_template("index.html", files=files)


@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        flash("No file part in the request.", "error")
        return redirect(url_for("index"))

    file = request.files["file"]

    if file.filename == "":
        flash("No file selected.", "error")
        return redirect(url_for("index"))

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Avoid overwriting existing files by adding a suffix if needed
        dest = UPLOAD_FOLDER / filename
        counter = 1
        while dest.exists():
            name, ext = os.path.splitext(filename)
            dest = UPLOAD_FOLDER / f"{name}_{counter}{ext}"
            counter += 1

        file.save(dest)
        flash(f"Uploaded successfully: {dest.name}", "success")
    else:
        flash(
            "File type not allowed. Allowed: "
            + ", ".join(sorted(ALLOWED_EXTENSIONS)),
            "error",
        )

    return redirect(url_for("index"))


@app.route("/uploads/<path:filename>")
def uploaded_file(filename):
    # Prevent directory traversal
    safe_name = secure_filename(filename)
    if not (UPLOAD_FOLDER / safe_name).is_file():
        abort(404)
    return send_from_directory(app.config["UPLOAD_FOLDER"], safe_name)


@app.route("/delete/<path:filename>", methods=["POST"])
def delete_file(filename):
    safe_name = secure_filename(filename)
    target = UPLOAD_FOLDER / safe_name
    if target.is_file():
        target.unlink()
        flash(f"Deleted: {safe_name}", "success")
    else:
        flash("File not found.", "error")
    return redirect(url_for("index"))


@app.errorhandler(RequestEntityTooLarge)
def handle_too_large(e):
    flash(f"File too large. Maximum size is {MAX_CONTENT_LENGTH // (1024*1024)} MB.", "error")
    return redirect(url_for("index"))


if __name__ == "__main__":
    # Development server – for production use gunicorn or similar
    app.run(host="0.0.0.0", port=5000, debug=True)
