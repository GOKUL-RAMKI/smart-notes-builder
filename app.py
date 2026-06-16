"""
Smart Notes Builder - Flask Application

A single-user, local-first application for organizing lecture notes using AI processing.
"""

import sqlite3
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for
from services.subject_service import (
    create_subject,
    delete_subject,
    get_subjects,
    get_subject_by_id
)
from services.config_service import load_api_key, save_api_key


# Initialize Flask application
app = Flask(__name__)

# Configuration
DB_PATH = "notes.db"
SUBJECTS_FOLDER = "subjects"
SCHEMA_FILE = "database/schema.sql"


def _initialize_database():
    """
    Initialize database if missing.
    
    Startup behavior (Section 33):
    - Create database if missing
    - Create subjects folder if missing
    - Create config.json if missing (handled by config_service)
    """
    # Create subjects folder if missing
    subjects_path = Path(SUBJECTS_FOLDER)
    subjects_path.mkdir(exist_ok=True)
    
    # Create database if missing
    if not Path(DB_PATH).exists():
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Read and execute schema
        with open(SCHEMA_FILE, "r") as f:
            schema = f.read()
        
        cursor.executescript(schema)
        conn.commit()
        conn.close()
    
    # Ensure config.json exists (handled by config_service)
    load_api_key()


# ============================================================================
# Routes - Home Page
# ============================================================================

@app.route("/")
def home():
    """
    Home page route (Section 22).
    
    GET /
    
    Display:
    - All subjects
    - Create Subject form
    - Upload Notes link
    - Settings link
    """
    try:
        subjects = get_subjects()
    except Exception as e:
        subjects = []
    
    return render_template("home.html", subjects=subjects)


# ============================================================================
# Routes - Settings Page
# ============================================================================

@app.route("/settings", methods=["GET", "POST"])
def settings():
    """
    Settings page route (Section 22).
    
    GET /settings
    - Display current API key
    
    POST /settings
    - Form field: gemini_api_key (Section 23)
    - Save API key
    - Redirect to /settings
    """
    if request.method == "POST":
        # Handle POST: save API key
        api_key = request.form.get("gemini_api_key", "")
        
        try:
            save_api_key(api_key)
        except Exception as e:
            # In case of error, still redirect but API key may not be saved
            pass
        
        return redirect(url_for("settings"))
    
    # Handle GET: display current API key
    try:
        api_key = load_api_key()
    except Exception as e:
        api_key = ""
    
    return render_template("settings.html", api_key=api_key)


# ============================================================================
# Routes - Subject Management
# ============================================================================
@app.route("/subjects/create", methods=["POST"])
def create_subject_route():

    subject_name = request.form.get("subject_name", "").strip()

    print("SUBJECT:", subject_name)

    try:
        result = create_subject(subject_name)
        print("CREATED:", result)

    except ValueError as e:
        print("VALUE ERROR:", e)

    except Exception as e:
        print("ERROR:", e)

    return redirect(url_for("home"))

@app.route("/subjects/delete/<int:subject_id>", methods=["POST"])
def delete_subject_route(subject_id):
    """
    Delete subject route (Section 22).
    
    POST /subjects/delete/<id>
    
    Process:
    - Delete subject folder
    - Delete DOCX files
    - Delete database record
    - Redirect to home
    """
    try:
        delete_subject(subject_id)
    except Exception as e:
        # Error handling - could show error message in future
        pass
    
    return redirect(url_for("home"))


# ============================================================================
# Routes - Subject Page
# ============================================================================

@app.route("/subject/<int:subject_id>")
def subject_page(subject_id):
    """
    Subject page route (Section 22).
    
    GET /subject/<id>
    
    Display:
    - Subject name
    - Entries list
    - Download button
    - Delete button
    """
    try:
        subject = get_subject_by_id(subject_id)
    except Exception as e:
        # Subject not found - redirect to home
        return redirect(url_for("home"))
    
    return render_template("subject.html", subject=subject)


# ============================================================================
# Routes - Upload Page
# ============================================================================

@app.route("/upload")
def upload_page():
    """
    Upload page route (Section 22).
    
    GET /upload
    
    Display:
    - Subject dropdown
    - Image upload
    - Preserve Images checkbox
    - Process button
    """
    try:
        subjects = get_subjects()
    except Exception as e:
        subjects = []
    
    return render_template("upload.html", subjects=subjects)


# ============================================================================
# Application Initialization
# ============================================================================

if __name__ == "__main__":
    # Initialize application on startup
    _initialize_database()
    
    # Run Flask development server
    app.run(debug=True)
