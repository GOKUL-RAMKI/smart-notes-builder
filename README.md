# Smart Notes Builder

Smart Notes Builder is a local-first Flask application that converts handwritten lecture notes into structured, searchable study notes using Google's Gemini models.

The application accepts one or more images of handwritten notes, processes them using Gemini OCR and reasoning capabilities, and generates organized DOCX documents for long-term storage and revision.

---

## Features

### Subject Management

* Create subjects
* Delete subjects
* Store notes separately for each subject
* Automatic subject folder creation

### AI Note Processing

* Supports JPG, JPEG, and PNG images
* Multiple image upload (up to 8 images per upload)
* Gemini-powered handwriting recognition
* Automatic spelling correction
* Duplicate content removal
* Structured note generation
* Diagram description generation
* Table preservation using Markdown-style formatting

### Document Generation

* Generate timestamped DOCX files
* Optional preservation of original uploaded images
* Download individual lecture notes
* Merge all lecture notes of a subject into a single document
* Download complete subject notes

### Model Management

* Configure Gemini API key
* Dynamically discover available Gemini models
* Switch models from the Settings page without changing code

### Local-First Design

* No cloud storage
* Notes stored locally
* SQLite database
* Simple Flask-based architecture
* Single-user desktop workflow

---

## Technology Stack

### Backend

* Python
* Flask
* SQLite

### AI

* Google Gemini API
* google-genai SDK

### Document Processing

* python-docx
* docxcompose
* Pillow

---

## Project Structure

```text
smart_notes/
│
├── app.py
├── config.json
├── notes.db
├── requirements.txt
│
├── database/
│   └── schema.sql
│
├── services/
│   ├── config_service.py
│   ├── gemini_service.py
│   ├── document_service.py
│   └── subject_service.py
│
├── templates/
│   ├── home.html
│   ├── upload.html
│   ├── settings.html
│   ├── subject.html
│   └── manage_subjects.html
│
└── subjects/
    └── <subject folders>
```

---

## Installation

### 1. Clone Repository

```bash
git clone <repository-url>
cd smart_notes
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
```

Activate:

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configuration

### Gemini API Key

Obtain a Gemini API key from:

https://aistudio.google.com/api-keys

Open:

```text
Settings
```

and save your API key.

---

## Running the Application

```bash
python app.py
```

Default URL:

```text
http://127.0.0.1:5000
```

---

## Usage

### Create a Subject

1. Open Manage Subjects
2. Create a subject
3. Open Upload Notes

### Upload Notes

1. Select subject
2. Upload images
3. Choose whether to preserve original images
4. Submit

### Generate Notes

The application will:

* Extract text from images
* Combine information from multiple pages
* Clean formatting
* Generate structured notes
* Save a DOCX document

### Download Notes

You can:

* Download individual lecture entries
* Download complete merged subject notes

---

## Limitations

* Maximum 8 images per upload
* Maximum 10 MB per image
* Requires an active Gemini API key
* Single-user application
* Local storage only

---

## License

Personal project for educational and learning purposes.
