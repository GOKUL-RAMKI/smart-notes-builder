# services/document_service.py
# Document service placeholder.
# Logic for create_docx_entry() and merge_subject_docs() will be implemented here.
import io

from docx.shared import Inches
from pathlib import Path
from datetime import datetime
from docx import Document

def create_docx_entry(subject_folder, notes, images, preserve_images) -> str:
    timestamp = datetime.now()
    filename = timestamp.strftime("%d-%m-%Y_%H-%M-%S.docx")

    subject_folder_path = Path(subject_folder)
    filepath = subject_folder_path/filename

    document = Document()

    document.add_paragraph("=================================")
    document.add_paragraph(timestamp.strftime("%d %b %Y %H:%M"))
    document.add_paragraph("=================================")
    document.add_paragraph("")
    if preserve_images:

        document.add_heading(
            "Original Images",
            level=2
        )

        for image in images:

            image_stream = io.BytesIO(
                image["bytes"]
            )

            document.add_picture(
                image_stream,
                width=Inches(5)
            )

            document.add_paragraph("")

    document.add_heading(
        "Generated Notes",
        level=2
    )
    document.add_paragraph(notes)
    print("TYPE:", type(notes))
    print("VALUE:", notes[:200])
    document.save(str(filepath))

    return str(filepath)
