# RAG-ai


## Stack

- Backend : Django REST Framework
- Base : PostgreSQL + pgvector
- Async : Celery + Redis
- Embeddings : `intfloat/multilingual-e5-small` (auto-hébergé, cf. cahier section 6)
- LLM : Anthropic Claude API
- Frontend : Angular (à venir, semaine 3)
- CI/CD : GitHub Actions
- Déploiement : Docker + OVH Cloud

## Démarrer en local

```bash
cp .env.example .env     
docker compose build
docker compose up
```

L'API est disponible sur `http://localhost:8000`.

Pour lancer les migrations (première fois) :

```bash
docker compose run --rm web python manage.py migrate
docker compose run --rm web python manage.py createsuperuser
```

## Tests & lint

```bash
docker compose run --rm web ruff check .
docker compose run --rm web pytest
```

## Structure

```
config/            # settings Django, Celery, urls
apps/documents/     # upload, statut d'ingestion (F1/F2)
apps/retrieval/     # recherche hybride (F3) — à implémenter
apps/chat/          # chat, citations, refus explicite (F4-F6) — à implémenter
```

## Prochaines étapes (semaine 1, cf. cahier section 15)

1. Migration initiale (`Document`, `DocumentChunk`).
2. Implémenter le parsing PDF/DOCX dans `ingest_document` (pypdf / python-docx).
3. Chunking + calcul des embeddings (`sentence-transformers`, modèle `intfloat/multilingual-e5-small`).
4. Indexation vectorielle (pgvector) + lexicale (PostgreSQL FTS).
5. Premiers tests manuels sur documents courts.
