from fastapi import FastAPI
from app.api.webhooks import router

app = FastAPI( 
              title = "repository reviewer",
              description ="an ai powered repository code reviewer",
              version ="1.0")
app.include_router(router)
@app.get("/")
async def root():
    return {"message" : "running"}

#ngrok http --url=phoniness-spiritism-expensive.ngrok-free.dev 8000
#celery -A app.workers.review_worker.celery_app worker --loglevel=info --pool=solo
