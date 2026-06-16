"""
Subject service module.

Manages subject creation, deletion, and retrieval operations.
Handles database interactions and filesystem operations for subject folders.
"""

import sqlite3
import os
import shutil
from pathlib import Path


# Configuration
DB_PATH = "notes.db"
SUBJECTS_FOLDER = "subjects"

# Invalid characters for subject names (Section 35.3)
INVALID_CHARS = {':', '?', '*', '|', '/', '\\', '<', '>', '"'}


def _get_connection():
    """
    Get a connection to the SQLite database.
    
    Returns:
        sqlite3.Connection: Database connection object
    """
    return sqlite3.connect(DB_PATH)


def _validate_subject_name(name: str) -> tuple:
    """
    Validate subject name against rules.
    
    Rules:
    - Must not be empty or whitespace only
    - Must not contain invalid characters: : ? * | / \\ < > "
    
    Args:
        name: Subject name to validate
        
    Returns:
        tuple: (is_valid: bool, error_message: str)
    """
    # Check for empty or whitespace only
    if not name or not name.strip():
        return False, "Subject name cannot be empty."
    
    # Check for invalid characters (Section 35.3)
    for char in name:
        if char in INVALID_CHARS:
            return False, "Subject name contains invalid characters."
    
    return True, ""


def _generate_folder_name(name: str) -> str:
    """
    Generate folder name from subject name.
    
    Algorithm (Section 7):
    - Trim spaces
    - Convert to lowercase
    - Replace spaces with underscores
    
    Args:
        name: Subject name
        
    Returns:
        str: Folder name
    """
    return "_".join(name.strip().lower().split())


def _subject_exists(name: str, exclude_id: int = None) -> bool:
    """
    Check if subject with the same name already exists (case-insensitive).
    
    Args:
        name: Subject name to check
        exclude_id: Optional subject ID to exclude from check
        
    Returns:
        bool: True if subject exists, False otherwise
    """
    conn = _get_connection()
    cursor = conn.cursor()
    
    query = "SELECT id FROM subjects WHERE LOWER(name) = LOWER(?)"
    params = [name]
    
    if exclude_id is not None:
        query += " AND id != ?"
        params.append(exclude_id)
    
    cursor.execute(query, params)
    exists = cursor.fetchone() is not None
    conn.close()
    
    return exists


def create_subject(name: str) -> dict:
    """
    Create a new subject.

    Process:
    - Validate subject name
    - Check duplicates
    - Generate folder name
    - Create subject folder
    - Insert database row
    """

    # Validate
    is_valid, error_msg = _validate_subject_name(name)
    if not is_valid:
        raise ValueError(error_msg)

    # Duplicate check
    if _subject_exists(name):
        raise ValueError("Subject already exists.")

    # Generate folder name
    folder_name = _generate_folder_name(name)

    # Ensure parent subjects directory exists
    subjects_path = Path(SUBJECTS_FOLDER)
    subjects_path.mkdir(parents=True, exist_ok=True)

    # Create subject folder
    subject_folder_path = subjects_path / folder_name

    try:
        subject_folder_path.mkdir(exist_ok=False)
    except FileExistsError:
        raise ValueError("Subject already exists.")
    except Exception as e:
        raise Exception(f"Failed to create subject folder: {str(e)}")

    conn = _get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO subjects (name, folder_name)
            VALUES (?, ?)
            """,
            (name, folder_name)
        )

        conn.commit()

        subject_id = cursor.lastrowid

        cursor.execute(
            """
            SELECT id, name, folder_name, created_at
            FROM subjects
            WHERE id = ?
            """,
            (subject_id,)
        )

        row = cursor.fetchone()

        return {
            "id": row[0],
            "name": row[1],
            "folder_name": row[2],
            "created_at": row[3]
        }

    except Exception as e:
        conn.rollback()

        try:
            if subject_folder_path.exists():
                shutil.rmtree(subject_folder_path)
        except Exception:
            pass

        raise Exception(f"Failed to create subject: {str(e)}")

    finally:
        conn.close()

def delete_subject(subject_id: int) -> None:
    """
    Delete a subject and all associated files.
    
    Process (Section 9):
    - Delete subject folder and all contents using shutil.rmtree()
    - Delete all DOCX files
    - Delete database record
    
    Args:
        subject_id: ID of the subject to delete
        
    Raises:
        Exception: If subject not found or deletion fails
    """
    conn = _get_connection()
    cursor = conn.cursor()
    
    try:
        # Step 1: Get subject folder path
        cursor.execute(
            "SELECT folder_name FROM subjects WHERE id = ?",
            (subject_id,)
        )
        row = cursor.fetchone()
        
        if not row:
            raise Exception(f"Subject with ID {subject_id} not found.")
        
        folder_name = row[0]
        subject_folder_path = Path(SUBJECTS_FOLDER) / folder_name
        
        # Step 2: Delete folder and all contents (including DOCX files)
        # Using shutil.rmtree() as required
        if subject_folder_path.exists():
            shutil.rmtree(subject_folder_path)
        
        # Step 3: Delete database record
        cursor.execute("DELETE FROM subjects WHERE id = ?", (subject_id,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise
    finally:
        conn.close()


def get_subjects() -> list:
    """
    Get all subjects.
    
    Returns:
        list: List of subject dictionaries, each with keys: id, name, folder_name, created_at
              Sorted by subject name
    """
    conn = _get_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT id, name, folder_name, created_at FROM subjects ORDER BY name"
    )
    rows = cursor.fetchall()
    conn.close()
    
    subjects = []
    for row in rows:
        subjects.append({
            "id": row[0],
            "name": row[1],
            "folder_name": row[2],
            "created_at": row[3]
        })
    
    return subjects


def get_subject_by_id(subject_id: int) -> dict:
    """
    Get a subject by ID.
    
    Args:
        subject_id: ID of the subject (Section 35.4)
        
    Returns:
        dict: Subject data with keys: id, name, folder_name, created_at
        
    Raises:
        Exception: If subject not found
    """
    conn = _get_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT id, name, folder_name, created_at FROM subjects WHERE id = ?",
        (subject_id,)
    )
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        raise Exception(f"Subject with ID {subject_id} not found.")
    
    return {
        "id": row[0],
        "name": row[1],
        "folder_name": row[2],
        "created_at": row[3]
    }
