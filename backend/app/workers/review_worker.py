from celery import Celery

from app.core.config import settings

celery_app = Celery("review_worker", broker=settings.redis_url)


@celery_app.task
def review_pull_request(repository: str, pull_request_number: int):
    # TODO: Implement the review pipeline.
    # GitHub -> diff/context -> checks/RAG -> AI -> validation -> GitHub review
    return {"status": "queued"}
