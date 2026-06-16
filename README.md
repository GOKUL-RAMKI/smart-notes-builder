# Smart Notes Builder

Smart Notes Builder is a local-first, desktop browser Flask application that converts handwritten lecture notes (uploaded as images) into organized, clean study notes in DOCX format using the Gemini API.

## Requirements

The application requires Python 3.8+ and the dependencies listed in `requirements.txt`.

## Project Structure

- `app.py`: Main Flask application entrypoint.
- `config.json`: Stores user-configured Gemini API key.
- `subjects/`: Local storage folder for subject subfolders and individual DOCX lecture entries.
- `temp/`: Temporary folder used for compiling or intermediate processing.
- `templates/`: Plain HTML templates for the user interface.
- `services/`: Encapsulated domain logic for Subject Management, Configuration, Gemini AI integration, and DOCX/Document compilation.
- `database/`: Database schema for the SQLite database.

## Setup & Running

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the application:
   ```bash
   python app.py
   ```
