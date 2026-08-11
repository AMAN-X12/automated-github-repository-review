# Architecture

Planned flow:

GitHub webhook
    -> FastAPI
    -> Redis/Celery
    -> GitHub PR diff/context
    -> deterministic checks + repository RAG
    -> AI review
    -> finding validation
    -> confidence filtering
    -> GitHub review
    -> PostgreSQL/dashboard

Keep this document updated when architectural decisions change.
