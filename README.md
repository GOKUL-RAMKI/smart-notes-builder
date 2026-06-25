# Smart Notes Builder

Smart Notes Builder is a **local-first Flask application** that converts handwritten lecture notes into structured, searchable study notes using Google's Gemini AI models.

The application accepts one or more images of handwritten notes, extracts and organizes the content using Gemini, and generates well-formatted Microsoft Word (DOCX) documents for revision and long-term storage.

---

## Features

###  Subject Management

* Create and delete subjects
* Automatic subject folder creation
* View all generated notes for each subject
* Download complete subject notes
* Delete individual note entries

###  AI Note Processing

* Supports **JPG**, **JPEG**, and **PNG**
* Upload up to **8 images** at once
* Gemini-powered handwriting recognition
* Automatic spelling correction
* Duplicate content removal
* Structured note generation
* Diagram explanation generation
* Table preservation
* Optional preservation of original uploaded images

###  Document Generation

* Timestamped DOCX generation
* Download individual lecture notes
* Merge all notes of a subject into a single document
* Download complete subject notes

###  Gemini Configuration

* Save Gemini API key
* Automatically discover available Gemini models
* Switch Gemini models from the Settings page
* Test Gemini connection directly from the application

###  Modern Interface

* Responsive user interface
* Dark mode / Light mode
* Image preview before upload
* Easy navigation between pages
* Simple local-first workflow

###  Local-First Design

* SQLite database
* Local document storage
* No cloud storage required
* No user account required
* Designed for personal use

---

# Technology Stack

## Backend

* Python
* Flask
* SQLite

## AI

* Google Gemini API
* google-genai SDK

## Document Processing

* python-docx
* docxcompose
* Pillow

## Frontend

* HTML5
* CSS3
* JavaScript

---

# Project Structure

```text
smart_notes/
│
├── app.py
├── requirements.txt
├── config.json
├── notes.db
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
├── static/
│   ├── css/
│   └── js/
│
├── templates/
│   ├── home.html
│   ├── upload.html
│   ├── manage_subjects.html
│   ├── subject.html
│   └── settings.html
│
└── subjects/
```

---

# Installation

## Clone Repository

```bash
git clone https://github.com/GOKUL-RAMKI/smart-notes-builder.git
cd smart-notes-builder
```

## Create Virtual Environment

```bash
python -m venv .venv
```

### Activate

Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

Linux / macOS

```bash
source .venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Configuration

Obtain a free Gemini API key from:

https://aistudio.google.com/api-keys

Inside the application:

```
Settings
→ Paste API Key
→ Select Gemini Model
→ Save
→ Test Connection
```

---

# Running the Application

```bash
python app.py
```

Open:

```
http://127.0.0.1:5000
```

---

# Usage

## 1. Create a Subject

* Open **Manage Subjects**
* Create a subject

## 2. Upload Notes

* Select a subject
* Upload handwritten note images
* Choose which images to preserve
* Click **Process Notes**

## 3. Generate Notes

The application automatically:

* Extracts handwritten text
* Combines multiple pages
* Removes duplicate content
* Corrects spelling
* Structures the notes
* Generates a DOCX file

## 4. Manage Notes

* Download individual lecture notes
* Download complete subject notes
* Delete unwanted note entries

---

# License

This project was developed for educational purposes and personal learning.
