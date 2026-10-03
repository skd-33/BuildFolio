"""
utils/file_manager.py — Helper functions for saving and managing user uploads safely.
"""

import os
import time
import re

# Base directory for all project uploads
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "uploads", "projects")

def get_project_upload_dir(project_id):
    """Returns the absolute path to the project's upload directory, creating it if it doesn't exist."""
    project_dir = os.path.join(UPLOAD_DIR, str(project_id))
    if not os.path.exists(project_dir):
        os.makedirs(project_dir, exist_ok=True)
    return project_dir

def sanitize_filename(filename):
    """Sanitizes a filename to prevent path traversal and remove unsafe characters."""
    # Keep only alphanumeric, dots, dashes, and underscores
    sanitized = re.sub(r'[^a-zA-Z0-9.\-_]', '', filename)
    if not sanitized:
        sanitized = "file"
    # Append a timestamp to ensure uniqueness and avoid overwriting
    name, ext = os.path.splitext(sanitized)
    timestamp = int(time.time() * 1000)
    return f"{name}_{timestamp}{ext}"

def save_uploaded_file(project_id, uploaded_file):
    """
    Saves a Streamlit UploadedFile to the local filesystem.
    Returns the relative file path to be stored in the database.
    """
    if uploaded_file is None:
        return None
    
    project_dir = get_project_upload_dir(project_id)
    safe_filename = sanitize_filename(uploaded_file.name)
    file_path = os.path.join(project_dir, safe_filename)
    
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Return a relative path like "uploads/projects/3/cover_12345.jpg"
    return f"uploads/projects/{project_id}/{safe_filename}"
