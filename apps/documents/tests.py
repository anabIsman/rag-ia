from apps.documents.models import Document


def test_document_status_default_is_uploaded():
    assert Document.Status.UPLOADED == "UPLOADED"


def test_document_str_includes_status():
    doc = Document(original_filename="spec.pdf", status=Document.Status.PROCESSING)
    assert "PROCESSING" in str(doc)
