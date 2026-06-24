import os
import sqlite3
from pathlib import Path

from flask import Flask, redirect, render_template, request, send_file, url_for
from services.config_service import (
    get_available_models,
    load_api_key,
    load_model,
    save_api_key,
    save_model,
)
from services.document_service import (
    create_docx_entry,
    get_subject_entries,
    merge_subject_docs,
)
from services.gemini_service import process_notes, test_connection
from services.subject_service import (
    create_subject,
    delete_subject,
    get_subject_by_id,
    get_subjects,
)
from google import genai

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

# Routes - Home Page
@app.route("/")
def home():
    try:
        subjects = get_subjects()
    except Exception:
        subjects = []
    return render_template("home.html", subjects=subjects)



# Routes - Settings Page
@app.route("/settings", methods=["GET", "POST"])
def settings():
    test_result = None
    if request.method == "POST":
        action = request.form.get("action")
        api_key = request.form.get("gemini_api_key", "")
        model_name = request.form.get(
            "gemini_model",
            "models/gemini-2.5-flash-lite",
        )
        if action == "save":

            try:
                save_api_key(api_key)
                save_model(model_name)

                return redirect(
                    url_for("settings")
                )

            except Exception as e:
                test_result = {
                    "success": False,
                    "message": str(e)
                }

        elif action == "test":

            try:
                save_api_key(api_key)
                save_model(model_name)
                
                result = test_connection()

                test_result = {
                    "success": True,
                    "message": str(result)
                }

            except Exception as e:

                test_result = {
                    "success": False,
                    "message": str(e)
                }

    try:
        api_key = load_api_key()
    except Exception:
        api_key = ""

    try:
        models = get_available_models()
        settings_error = None

    except Exception:

        models = [
            "models/gemini-2.5-flash-lite"
        ]

        settings_error = (
            "Unable to load Gemini models. "
            "Please check your API key."
        )

    current_model = load_model()

    return render_template(
        "settings.html",
        api_key=api_key,
        models=models,
        current_model=current_model,
        test_result=test_result,
        settings_error=settings_error
    )

@app.route("/models")
def list_models():
    api_key = load_api_key()
    client = genai.Client(api_key=api_key)
    return "<br>".join([model.name for model in client.models.list()])



# Routes - Subject Management

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



# Routes - Subject Page

@app.route("/subject/<int:subject_id>")
def subject_page(subject_id):
    try:
        subject = get_subject_by_id(subject_id)
    except Exception:
        return redirect(url_for("home"))
    subject_folder = f"subjects/{subject['folder_name']}"
    entries = get_subject_entries(subject_folder)
    return render_template("subject.html", subject=subject, entries=entries)

# Routes - Upload Page

@app.route("/upload", methods=["GET", "POST"])
def upload_page():
    success = None
    error = None
    file_name = None
    subject_id = None
    try:
        subjects = get_subjects()
    except Exception:
        subjects = []

    if request.method == "POST":

        subject_id = request.form.get("subject_id")
        preserve_files = request.form.getlist("preserve_files")

        if not subject_id:
            error = "Please select a subject."

        else:

            files = request.files.getlist("images")
            files = [f for f in files if f and f.filename]

            if len(files) == 0:
                error = "Please upload at least one image."

            elif len(files) > 8:
                error = "Maximum 8 images allowed."

            else:

                allowed_extensions = {
                    "jpg",
                    "jpeg",
                    "png"
                }

                image_data_list = []

                try:

                    for file in files:

                        extension = (
                            file.filename
                            .rsplit(".", 1)[-1]
                            .lower()
                        )

                        if extension not in allowed_extensions:
                            raise ValueError(
                                "Only JPG, JPEG and PNG files are allowed."
                            )

                        image_bytes = file.read()

                        if len(image_bytes) > 10 * 1024 * 1024:
                            raise ValueError(
                                "Image exceeds 10 MB limit."
                            )

                        image_data_list.append(
                            {
                                "filename": file.filename,
                                "bytes": image_bytes,
                                "mime_type": file.mimetype,
                            }
                        )

                    notes = process_notes(
                        image_data_list
                    )

                    subject = get_subject_by_id(
                        int(subject_id)
                    )

                    subject_folder = (
                        f"subjects/{subject['folder_name']}"
                    )

                    docx_path = create_docx_entry(
                        subject_folder=subject_folder,
                        notes=notes,
                        images=image_data_list,
                        preserve_files=preserve_files,
                    )

                    file_name = (
                        Path(docx_path).name
                    )

                    success = (
                        f"{subject['name']} notes saved successfully."
                    )

                except Exception as e:

                    if (
                        "401" in str(e)
                        or
                        "429" in str(e)
                    ):
                        error = (
                            "Invalid Gemini API key. "
                            "Check Settings."
                        )
                    else:
                        error = str(e)

    return render_template(
        "upload.html",
        subjects=subjects,
        success=success,
        error=error,
        file_name=file_name,
        subject_id=subject_id,
    )

# Routes - Download / Delete Entries

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



# Application Initialization

if __name__ == "__main__":
    _initialize_database()
    app.run(debug=True)
