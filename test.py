from services.document_service import (
    merge_subject_docs
)

path = merge_subject_docs(
    "subjects/c"
)

print(path)