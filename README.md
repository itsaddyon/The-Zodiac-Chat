# The Zodiac Chat

A compact Flask web app that blends astrological themes with a simple chat-style interface. This repository is intentionally minimal so you can run, read, and extend the project quickly.

## Features
- Small, single-file Flask backend (`app.py`) for easy reading and modification.
- Minimal HTML frontend (`templates/index.html`) with a responsive layout.
- Simple dependency management via `requirements.txt`.

## Requirements
- Python 3.8+
- See `requirements.txt` for exact packages.

## Installation
1. Create and activate a virtual environment:

   - On Windows (PowerShell):

     ```powershell
     python -m venv venv
     .\\venv\\Scripts\\Activate.ps1
     ```

   - On Windows (cmd.exe):

     ```cmd
     python -m venv venv
     venv\\Scripts\\activate
     ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Run
1. Set the Flask app environment variable and run the server.

   - PowerShell:

     ```powershell
     $env:FLASK_APP = 'app.py'
     flask run
     ```

   - cmd.exe:

     ```cmd
     set FLASK_APP=app.py
     flask run
     ```

2. Open `http://127.0.0.1:5000` in your browser.

## Project Structure

- `app.py` — Flask application and route definitions.
- `requirements.txt` — Python dependencies.
- `templates/index.html` — Main HTML template.

## How to Use
- Visit the app in your browser, type a message or prompt, and interact with the simple chat UI. The app is designed for experimentation and learning — extend the routes and templates as you like.

## Contributing
- Improvements, bug fixes, and feature ideas are welcome. Create issues or pull requests. Suggested improvements:
  - Add persistent chat history
  - Integrate external astrology APIs
  - Add automated tests and CI

### Contributors
**Adarsh Arya**
Build for People

## License
This project uses a permissive license by default — add a `LICENSE` file if you need a specific license.

---
