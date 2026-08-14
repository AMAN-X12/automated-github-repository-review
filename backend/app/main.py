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

    