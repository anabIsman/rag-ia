# RAG-ai

Projet portfolio — voir `Cahier-des-charges-Assistant-IA-RAG-v4.2.docx` pour le cahier des charges complet (verrouillé).

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