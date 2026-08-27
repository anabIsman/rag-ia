import logging

from celery import shared_task

from .models import Document

logger = logging.getLogger(__name__)


@shared_task
def ingest_document(document_id: int) -> None:
    """
    Pipeline d'ingestion — cf. cahier V4.1, section 7.
    Étapes à implémenter dans l'ordre :
      1. [FAIT] passage à PROCESSING
      2. parsing PDF/DOCX (pypdf / python-docx) + métadonnées page/section
      3. chunking (document_id, page, section, chunk_index, start_offset, end_offset)
      4. calcul des embeddings (intfloat/multilingual-e5-small, cf. settings.EMBEDDING_MODEL_NAME)
      5. indexation vectorielle + lexicale (pgvector + PostgreSQL FTS)
      6. passage à INDEXED, ou FAILED + failure_reason en cas d'erreur
    """
    document = Document.objects.get(id=document_id)
    document.status = Document.Status.PROCESSING
    document.save(update_fields=["status", "updated_at"])

    try:
        # TODO(semaine 1) : parsing, chunking, embeddings, indexation.
        raise NotImplementedError("Pipeline d'ingestion à implémenter — semaine 1.")
    except Exception as exc:  # noqa: BLE001 - on capture large ici pour tracer FAILED proprement
        logger.exception("Échec de l'ingestion pour le document %s", document_id)
        document.status = Document.Status.FAILED
        document.failure_reason = str(exc)
        document.save(update_fields=["status", "failure_reason", "updated_at"])
