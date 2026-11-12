# Simple File Upload Website for Fedora Linux

A minimal, clean web app that lets you upload files via a browser. Built with Python + Flask.

## Features

- Drag-and-drop or click-to-browse upload
- List of uploaded files with download links
- Delete individual files
- File type allow-list + 2 GB size limit
- Secure filename handling (no path traversal)
- Dark, modern UI

## Requirements

- Fedora Linux (works on any recent version)
- Python 3.9+

## Quick Start on Fedora

```bash
# 1. Install Python tooling (if not already present)
sudo dnf install python3 python3-pip python3-virtualenv

# 2. Go into the project directory
cd fedora-upload-site

# 3. Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run the development server
python3 app.py
```

Then open your browser to:

- Local:   http://127.0.0.1:5000
- Network: http://<your-fedora-ip>:5000

## Production notes (recommended)

The built-in Flask server is fine for testing. For anything exposed to a network:

1. Set a strong secret key:
   ```bash
   export SECRET_KEY="a-long-random-string"
   ```

2. Use a proper WSGI server, e.g. Gunicorn:
   ```bash
   pip install gunicorn
   gunicorn -b 0.0.0.0:5000 -w 2 app:app
   ```

3. Put Nginx or Caddy in front as a reverse proxy and enable HTTPS.

4. Add authentication (this demo has none).

5. Consider moving uploads outside the web root and serving them through a controlled endpoint.

## Configuration

Edit the top of `app.py` to change:

- `ALLOWED_EXTENSIONS` – which file types are accepted
- `MAX_CONTENT_LENGTH` – maximum upload size (bytes)
- Upload folder location

## Security warning

This is a **simple demo**. It has no user authentication. Anyone who can reach the server can upload and delete files. Do not expose it to the public internet without adding auth, rate limiting, and proper hardening.

## License

Public domain / CC0 – do whatever you want with it.
