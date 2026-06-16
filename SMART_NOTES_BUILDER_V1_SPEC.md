# SMART_NOTES_BUILDER_V1_SPEC.md

# AI Implementation Instructions

You are building this project exactly as specified.

Rules:

- Do not add authentication.
- Do not add user accounts.
- Do not add cloud storage.
- Do not add CSS frameworks.
- Do not add JavaScript frameworks.
- Do not add ORM libraries.
- Do not add features not explicitly listed.
- Use Flask.
- Use SQLite.
- Use python-docx.
- Use plain HTML templates.
- Follow the route table exactly.
- Follow the database schema exactly.
- Follow the folder structure exactly.

## Section 1 - Project Overview

### Project Name

Smart Notes Builder

### Goal

Convert handwritten lecture notes into organized study notes.

The application is:

- Single User
- Local First
- Desktop Browser
- Flask Application

Authentication is out of scope.
Hosting is out of scope.

---

## Section 2 - Functional Requirements

### FR-001 Subject Management

User must be able to:

- Create Subject
- Delete Subject
- View Subjects

### FR-002 Settings

User must be able to:

- Store Gemini API Key
- Update Gemini API Key

### FR-003 Upload Notes

User must be able to upload:

- 1 to 8 images

Formats:

- jpg
- jpeg
- png

Maximum:

- 10 MB per image

### FR-004 AI Processing

System must:

- Receive images
- Send to Gemini
- Generate clean notes
- Return formatted content

### FR-005 DOCX Generation

System must:

- Create one DOCX entry per upload session

Example:

User uploads 5 images

Result:

- 1 DOCX

Not 5 DOCX files.

### FR-006 Subject Export

User must be able to:

- Download complete subject notes

System merges all DOCX entries.

---

## Section 3 - Non Functional Requirements

### NFR-001

Application must work offline except Gemini requests.

### NFR-002

Images must not be permanently stored.

### NFR-003

Subject creation must complete in under 1 second.

### NFR-004

Duplicate subjects prohibited.

---

## Section 4 - Directory Structure

```text
smart_notes/

app.py

config.json

notes.db

subjects/

templates/

static/

services/
```

---

## Section 5 - Database Design

### subjects

```sql
CREATE TABLE subjects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    folder_name TEXT UNIQUE NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

---

## Section 6 - Config Design

File:

`config.json`

Structure:

```json
{
  "gemini_api_key": ""
}
```

---

## Section 7 - Folder Naming

Input:

`Computer Networks`

Output:

`computer_networks`

Algorithm:

- Trim spaces
- Convert to lowercase
- Replace spaces with underscores

---

## Section 8 - Subject Creation

### Route

`POST /subjects/create`

### Validation

Reject:

- Empty
- Whitespace only
- Duplicate name

### Success

- Insert database row
- Create subject folder

---

## Section 9 - Subject Deletion

### Route

`POST /subjects/delete/<id>`

### UI

Confirmation required.

Delete Subject?

This action cannot be undone.

### Backend

- Delete folder
- Delete DOCX files
- Delete DB record

---

## Section 10 - Upload Page

Fields:

- Subject Dropdown
- Image Upload
- Preserve Original Images Checkbox
- Submit Button

---

## Section 11 - Upload Validation

### Image Count

Minimum: 1

Maximum: 8

### File Size

Maximum: 10 MB per image

### File Types

Allow:

- jpg
- jpeg
- png

---

## Section 12 - Gemini Service

File:

`services/gemini_service.py`

Function:

```python
process_notes(images)
```

Input:

```python
list[bytes]
```

Output:

```python
str
```

Prompt:

- These images belong to the same lecture.
- Read all visible content.
- Merge information.
- Remove duplicates.
- Correct spelling mistakes.
- Improve formatting.
- Preserve technical terminology.
- Generate clean study notes.
- Return plain formatted notes.

---

## Section 13 - DOCX Service

File:

`services/document_service.py`

Function:

```python
create_docx_entry()
```

Parameters:

- subject
- notes
- images
- preserve_images

Filename format:

`YYYY-MM-DD_HH-MM-SS.docx`

---

## Section 14 - DOCX Layout

Header:

```text
=================================
Java Notes Entry
16 Jun 2026 15:42
=================================
```

Body:

Generated Notes

Optional Images Section:

Shown only when:

`Preserve Images = True`

---

## Section 15 - RAM Handling

Allowed:

```python
image_bytes = file.read()
```

Not allowed:

```python
file.save(...)
```

---

## Section 16 - Subject Page

Display:

- Subject Name
- Entries List
- Download Button

Example:

- Java
- 16 Jun 2026
- 18 Jun 2026
- 20 Jun 2026

Download Complete Notes

---

## Section 17 - Download Service

Route:

`GET /download/<id>`

Process:

- Locate folder
- Read DOCX entries
- Sort by timestamp
- Merge entries
- Return final DOCX

Separator:

```text
=================================
16 Jun 2026 09:10
=================================
```

---

## Section 18 - Home Page

Content:

- Subjects List
- Upload Button
- Settings Button

---

## Section 19 - Settings Page

Routes:

- GET /settings
- POST /settings

Fields:

- Gemini API Key

---

## Section 20 - Service Layer

### subject_service.py

```python
create_subject()
delete_subject()
get_subjects()
get_subject_by_id()
```

### config_service.py

```python
load_api_key()
save_api_key()
```

### gemini_service.py

```python
process_notes()
```

### document_service.py

```python
create_docx_entry()
merge_subject_docs()
```

---

## Section 21 - Acceptance Tests

### Test 1

Create Subject

Verify:

- Folder created
- Database row exists

### Test 2

Create duplicate subject

Verify:

- Rejected

### Test 3

Upload image

Verify:

- Gemini response generated

### Test 4

Upload with preserve enabled

Verify:

- Images appear in DOCX

### Test 5

Upload with preserve disabled

Verify:

- No images in DOCX

### Test 6

Download complete notes

Verify:

- Merged DOCX generated

### Test 7

Delete subject

Verify:

- Folder deleted
- DOCX files deleted
- Database row deleted


---

# Section 22 - Flask Routes

## Home

GET /

Purpose:

Show all subjects

Template:

home.html

Data:

subjects = get_subjects()

---

## Settings Page

GET /settings

Purpose:

Display current API key

Template:

settings.html

---

## Save Settings

POST /settings

Form Fields:

gemini_api_key

Action:

save_api_key()

Redirect:

/settings

---

## Upload Page

GET /upload

Purpose:

Display upload form

Template:

upload.html

Data:

subjects

---

## Process Upload

POST /upload

Input:

subject_id

images[]

preserve_images

Output:

Success or Error

---

## Subject Page

GET /subject/<id>

Purpose:

Display subject entries

Template:

subject.html

---

## Create Subject

POST /subjects/create

Input:

subject_name

---

## Delete Subject

POST /subjects/delete/<id>

Input:

id

---

## Download Subject

GET /download/<id>

Returns:

Merged DOCX

---

# Section 23 - Form Field Names

## Create Subject Form

subject_name

## Settings Form

gemini_api_key

## Upload Form

subject_id

images

preserve_images

---

# Section 24 - subject_service.py

## create_subject(name: str)

Responsibilities:

- Validate
- Generate folder_name
- Insert DB row
- Create folder

## delete_subject(subject_id: int)

Responsibilities:

- Delete folder
- Delete files
- Delete DB row

## get_subjects()

Returns all subjects

## get_subject_by_id()

Returns one subject

---

# Section 25 - config_service.py

## load_api_key()

Returns string

## save_api_key(api_key)

Updates config.json

---

# Section 26 - gemini_service.py

## process_notes(images: list[bytes])

Returns string

Steps:

- Read API key
- Create Gemini client
- Attach uploaded images
- Send prompt
- Receive response
- Return text

Failure:

Raise Exception

---

# Section 27 - document_service.py

## create_docx_entry(
subject_folder,
notes,
images,
preserve_images
)

Responsibilities:

- Generate filename
- Create DOCX
- Insert timestamp
- Insert notes
- Optionally insert images
- Save file

Returns:

filepath

---

# Section 28 - merge_subject_docs()

Returns:

merged_docx_path

Algorithm:

1. Read folder
2. Find all .docx files
3. Sort filenames ascending
4. Create new DOCX
5. For each DOCX:
   - Insert separator
   - Copy content
   - Copy images
6. Save merged file
7. Return path

---

# Section 29 - Error Messages

Duplicate Subject:

Subject already exists.

Empty Subject:

Subject name cannot be empty.

Missing API Key:

Please configure Gemini API Key in Settings.

Too Many Images:

Maximum 8 images allowed.

Unsupported Type:

Only JPG, JPEG and PNG files are allowed.

File Too Large:

Image exceeds 10 MB limit.

Gemini Failure:

Unable to process notes.
Please try again.

---

# Section 30 - Home Page Layout

Smart Notes Builder

Subjects

Create Subject

Upload Notes

Settings

---

# Section 31 - Upload Page Layout

Upload Notes

Subject Dropdown

Image Upload

Preserve Images

Process Button

---

# Section 32 - Subject Page Layout

Java

Entries

Download Complete Notes

Delete Subject

---

# Section 33 - Startup Behavior

Application start:

- Create DB if missing
- Create subjects folder if missing
- Create config.json if missing

---

# Section 34 - Definition of Complete

Create Subject
→ Folder Created

Upload Images
→ Gemini Processes

Generate DOCX
→ Store DOCX

Download Subject
→ Merged DOCX Returned

Delete Subject
→ Everything Removed

# Section 35 - Specification Corrections (v1.1)

## 35.1 create_docx_entry Signature

Replace all previous definitions with:

```python
create_docx_entry(
    subject_name,
    subject_folder,
    notes,
    images,
    preserve_images
)
```

Purpose:

* subject_name → DOCX header display
* subject_folder → save location

---

## 35.2 Image Storage Clarification

Replace:

"Images must not be permanently stored."

With:

"Uploaded images must not be stored as standalone image files.

Images embedded inside generated DOCX files are permitted."

---

## 35.3 Subject Name Validation

Allowed characters:

* A-Z
* a-z
* 0-9
* space

Reject:

```text
:
?
*
|
/
\
<
>
"
```

Error:

```text
Subject name contains invalid characters.
```

---

## 35.4 get_subject_by_id Signature

Replace:

```python
get_subject_by_id()
```

With:

```python
get_subject_by_id(
    subject_id: int
)
```

---

## 35.5 API Key Precheck

Before any Gemini request:

```python
if not api_key:
    raise ValueError(
        "Please configure Gemini API Key in Settings."
    )
```

---

## 35.6 Checkbox Handling

Implementation:

```python
preserve_images = (
    "preserve_images"
    in request.form
)
```

Unchecked checkbox evaluates to False.

---

## 35.7 Empty Upload Handling

Implementation:

```python
images = [
    f
    for f in request.files.getlist("images")
    if f.filename
]
```

Validation occurs after filtering.

---

## 35.8 Timestamp Rule

All timestamps use local system time.

Sorting uses filenames only.

Filesystem metadata must not be used.

---

## 35.9 Subject Deletion

Replace:

```text
Delete folder
Delete files
Delete DB row
```

With:

```text
Delete subject folder recursively.

Delete database record.
```

Implementation:

```python
shutil.rmtree(subject_folder)
```

---

## 35.10 Merged DOCX Location

Merged documents must never be stored inside:

```text
subjects/<subject_folder>/
```

Instead:

```text
temp/
```

Workflow:

```text
Generate merged document
↓
Return download
↓
Delete temporary file
```

Prevents merged documents from being merged into future exports.

---

## 35.11 Subject Folder Location

All subject folders must be created inside:

```text
subjects/
```

Example:

```text
subjects/java/
subjects/dbms/
subjects/computer_networks/
```

---

## 35.12 Route Validation Priority

POST /upload validation order:

1. API key exists
2. Images exist
3. Image count (1-8)
4. File type validation
5. File size validation
6. Gemini processing

Fail immediately on first validation error.

---

## 35.13 DOCX Merge Limitation

Implementation may use python-docx XML manipulation or any equivalent approach necessary to copy text and images.

Behavior is more important than implementation method.

Final requirement:

* All text preserved
* All images preserved
* Entries remain chronologically ordered

```
```
