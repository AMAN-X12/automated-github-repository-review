from fastapi import APIRouter, Request, HTTPException
import logging 

logging.basicConfig(level = logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()
@router.post("/webhook")
async def webhook_receiver(request:Request):
    eventType = request.headers.get("X-GitHub-Event")
    if eventType == "pull_request":
        payload = request.json()
        action = payload.get("action")
        repoName = payload.get("repository", {}).get("full_name","unknown_repo" )
        prNum = payload.get("pull_request", {}).get("number","unknown number")
        prAuthor = payload.get("pull_request", {}).get("user", {}).get("login","unknown_author")
        logger.info(repoName)
        logger.info(prNum)
        logger.info(prAuthor)
        logger.info(action)
        return {
            "status": "successfull",
            "message" : f"pr event : {eventType} logged"
        }

    return {
        "status" :"ignored",
        "message" : f"Event : {eventType} ignored"
    }

