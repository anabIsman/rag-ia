from django.conf import settings
from django.db import models
from pgvector.django import VectorField


class Document(models.Model):
    """Un document source (PDF/DOCX) téléversé pour ingestion. Cf. cahier V4.1, F1/F2."""

    class Status(models.TextChoices):
        UPLOADED = "UPLOADED", "Uploaded"
        PROCESSING = "PROCESSING", "Processing"
        INDEXED = "INDEXED", "Indexed"
        FAILED = "FAILED", "Failed"

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="documents"
    )
    file = models.FileField(upload_to="documents/%Y/%m/")
    original_filename = models.CharField(max_length=255)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.UPLOADED
    )
    failure_reason = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.original_filename} ({self.status})"


class DocumentChunk(models.Model):
    """Un passage indexé d'un document, avec métadonnées de traçabilité (F5/D8)."""

    document = models.ForeignKey(
        Document, on_delete=models.CASCADE, related_name="chunks"
    )
    page = models.PositiveIntegerField()
    section = models.CharField(max_length=255, blank=True, default="")
    chunk_index = models.PositiveIntegerField()
    start_offset = models.PositiveIntegerField()
    end_offset = models.PositiveIntegerField()
    text = models.TextField()
    # Dimension alignée sur settings.EMBEDDING_DIM (intfloat/multilingual-e5-small = 384)
    embedding = VectorField(dimensions=384, null=True)

    class Meta:
        indexes = [models.Index(fields=["document", "chunk_index"])]
        ordering = ["document", "chunk_index"]

    def __str__(self) -> str:
        return f"{self.document_id} chunk#{self.chunk_index} (p.{self.page})"
