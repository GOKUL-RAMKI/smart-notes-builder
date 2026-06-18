"""
Smart Notes Builder - Flask Application
A single-user, local-first application for organizing lecture notes using AI processing.
"""
import os
from services.document_service import (
    create_docx_entry,
    merge_subject_docs,
    get_subject_entries,
)
import sqlite3
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, send_file
from services.subject_service import (
    create_subject,
    delete_subject,
    get_subjects,
    get_subject_by_id,
)
from services.config_service import (
    load_api_key,
    save_api_key,
    load_model,
    save_model,
    get_available_models,
)
from services.gemini_service import test_connection, process_notes
# Initialize Flask application
app = Flask(__name__)
# Configuration
DB_PATH = "notes.db"
SUBJECTS_FOLDER = "subjects"
SCHEMA_FILE = "database/schema.sql"
@app.route("/test-gemini")
def test_gemini_route():
    try:
        result = test_connection()
        return f"<h2>{result}</h2>"
    except Exception as e:
        if "429" in str(e) or "401" in str(e):
            return f"""
                <h1>Error 429</h1>
                <pre>{str(e)}</pre>
                <br>
                <a href="/upload">Back</a><br>
                <a href="/settings">Settings</a>
            """
        return f"""
            <h1>Error 503</h1>
            <pre>{str(e)}</pre>
            <br>
            <a href="/upload">Back</a>
        """
def _initialize_database():
    """Initialize database if missing."""
    subjects_path = Path(SUBJECTS_FOLDER)
    subjects_path.mkdir(exist_ok=True)
    if not Path(DB_PATH).exists():
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        with open(SCHEMA_FILE, "r") as f:
            schema = f.read()
        cursor.executescript(schema)
        conn.commit()
        conn.close()
    load_api_key()
# ============================================================================
# Routes - Home Page
# ============================================================================
@app.route("/")
def home():
    try:
        subjects = get_subjects()
    except Exception:
        subjects = []
    return render_template("home.html", subjects=subjects)
# ============================================================================
# Routes - Settings Page
# ============================================================================
@app.route("/settings", methods=["GET", "POST"])
def settings():
    if request.method == "POST":
        api_key = request.form.get("gemini_api_key", "")
        model_name = request.form.get(
            "gemini_model",
            "models/gemini-2.5-flash-lite",
        )
        try:
            save_api_key(api_key)
            save_model(model_name)
        except Exception as e:
            print(e)
        return redirect(url_for("settings"))
    try:
        api_key = load_api_key()
    except Exception:
        api_key = ""
    models = get_available_models()
    current_model = load_model()
    return render_template(
        "settings.html",
        api_key=api_key,
        models=models,
        current_model=current_model,
    )
@app.route("/models")
def list_models():
    from google import genai
    api_key = load_api_key()
    client = genai.Client(api_key=api_key)
    return "<br>".join([model.name for model in client.models.list()])
# ============================================================================
# Routes - Subject Management
# ============================================================================
@app.route("/subjects/manage")
def manage_subjects_page():
    """Manage Subjects page route."""
    try:
        subjects = get_subjects()
    except Exception:
        subjects = []
    return render_template("manage_subjects.html", subjects=subjects)
@app.route("/subjects/create", methods=["POST"])
def create_subject_route():
    subject_name = request.form.get("subject_name", "").strip()
    try:
        create_subject(subject_name)
    except Exception as e:
        print(e)
    # stay on manage page
    return redirect(url_for("manage_subjects_page"))
@app.route("/subjects/delete/<int:subject_id>", methods=["POST"])
def delete_subject_route(subject_id):
    try:
        delete_subject(subject_id)
    except Exception as e:
        print(e)
    # stay on manage page
    return redirect(url_for("manage_subjects_page"))
# ============================================================================
# Routes - Subject Page
# ============================================================================
@app.route("/subject/<int:subject_id>")
def subject_page(subject_id):
    try:
        subject = get_subject_by_id(subject_id)
    except Exception:
        return redirect(url_for("home"))
    subject_folder = f"subjects/{subject['folder_name']}"
    entries = get_subject_entries(subject_folder)
    return render_template("subject.html", subject=subject, entries=entries)
# ============================================================================
# Routes - Upload Page
# ============================================================================
@app.route("/upload")
def upload_page():
    try:
        subjects = get_subjects()
    except Exception:
        subjects = []
    return render_template("upload.html", subjects=subjects)

@app.route("/upload", methods=["POST"])
def process_upload():
    subject_id = request.form.get("subject_id")
    preserve_files = request.form.getlist("preserve_files")
    if not subject_id:
        return "Please select a subject."
    files = request.files.getlist("images")
    files = [f for f in files if f and f.filename]
    if len(files) == 0:
        return "Please upload at least one image."
    if len(files) > 8:
        return "Maximum 8 images allowed."
    allowed_extensions = {"jpg", "jpeg", "png"}
    image_data_list = []
    for file in files:
        extension = file.filename.rsplit(".", 1)[-1].lower()
        if extension not in allowed_extensions:
            return "Only JPG, JPEG and PNG files are allowed."
        image_bytes = file.read()
        if len(image_bytes) > 10 * 1024 * 1024:
            return "Image exceeds 10 MB limit."
        image_data_list.append({"filename": file.filename,"bytes": image_bytes, "mime_type": file.mimetype})
    try:
        notes = process_notes(image_data_list)
        subject = get_subject_by_id(int(subject_id))
        subject_folder = f"subjects/{subject['folder_name']}"
        docx_path = create_docx_entry(
            subject_folder=subject_folder,
            notes=notes,
            images=image_data_list,
            preserve_files=preserve_files,
        )
        file_name = docx_path.split("\\")[-1]
        return f"""
            <h1>Notes Saved Successfully</h1>
            <br>
            <a href="/upload">Upload Another</a>
            <br><br>
            <a href="/subject/{subject_id}/download/{file_name}">Download {file_name}</a>
            <a href="/">Home</a>
        """
    except Exception as e:
        if "429" in str(e) or "401" in str(e):
            return f"""
                <h1>Error 429</h1>
                <pre>{str(e)}</pre>
                <br>
                <a href="/upload">Back</a><br>
                <a href="/settings">Settings</a>
            """
        return f"""
            <h1>Error 503</h1>
            <pre>{str(e)}</pre>
            <br>
            <a href="/upload">Back</a>
        """
# ============================================================================
# Routes - Download / Delete Entries
# ============================================================================
@app.route("/subject/<int:subject_id>/download")
def download_subject(subject_id):
    subject = get_subject_by_id(subject_id)
    subject_folder = f"subjects/{subject['folder_name']}"
    try:
        merged_file = merge_subject_docs(subject_folder)
    except ValueError as e:
        return f"<h1>Error</h1><pre>{str(e)}</pre><br><a href='/subject/{subject_id}'>Back</a>"
    return send_file(merged_file, as_attachment=True)
@app.route("/subject/<int:subject_id>/download/<path:entry_name>")
def download_entry(subject_id, entry_name):
    if ".." in entry_name:
        return "invalid file", 400
    if Path(entry_name).name != entry_name:
        return "invalid file", 400
    subject = get_subject_by_id(subject_id)
    subject_folder = f"subjects/{subject['folder_name']}"

    file_path = Path(subject_folder) / entry_name

    return send_file(file_path, as_attachment=True)

@app.route("/subject/<int:subject_id>/delete/<path:entry_name>", methods=["POST"])
def delete_entry(subject_id, entry_name):
    if ".." in entry_name:
        return "invalid file", 400
    if Path(entry_name).name != entry_name:
        return "invalid file", 400
    subject = get_subject_by_id(subject_id)
    subject_folder = f"subjects/{subject['folder_name']}"
    file_path = Path(subject_folder) / entry_name
    if not file_path.exists():
        return "File not found", 404
    os.remove(file_path)
    return redirect(url_for("subject_page", subject_id=subject_id))
# ============================================================================
# Application Initialization
# ============================================================================
if __name__ == "__main__":
    _initialize_database()
    app.run(debug=True)
