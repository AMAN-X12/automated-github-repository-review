from fastapi import APIRouter, Request, HTTPException
import logging 
import hashlib
import hmac
import os
import json
from dotenv import load_dotenv
load_dotenv()
logging.basicConfig(level = logging.INFO)
logger = logging.getLogger(__name__)
from app.workers.review_worker import review_pull_request

router = APIRouter()
@router.post("/webhook")
async def webhook_receiver(request:Request):
    githubSecret = request.headers.get("X-Hub-Signature-256")
    if not githubSecret:
        raise HTTPException(
            status_code=401,
            detail="missing github secret"
        )
    localSecret = os.getenv("GITHUB_WEBHOOK_SECRET")
    body = await request.body()
    expectedSecret= "sha256=" + hmac.new(localSecret.encode("utf-8"),
                                         body ,
                                         hashlib.sha256).hexdigest()
    if not hmac.compare_digest(
        expectedSecret,
        githubSecret        
    ):
        raise HTTPException(
            status_code=401,
            detail="invalid webhook signature"
        )
    eventType = request.headers.get("X-GitHub-Event")
    if eventType == "pull_request":
        payload =   json.loads(body)
        action = payload.get("action")
        allowed_actions = ["opened", "reopened", "synchronize"]
        if action not in allowed_actions:
            return {"status": "ignored", "message": f"Action {action} ignored"}
        logger.info(f"processing pr action : {action}")
        repoName = payload.get("repository", {}).get("full_name","unknown_repo" )
        prNum = payload.get("pull_request", {}).get("number","unknown number")
        prAuthor = payload.get("pull_request", {}).get("user", {}).get("login","unknown_author")
        installation_id=payload.get("installation",{}).get("id")
        logger.info(f"rpository : {repoName}")
        logger.info(f"pull req number {prNum}")
        logger.info(f"owner {prAuthor}")
        logger.info(f"status {action}")
        logger.info(f"installation id : {installation_id}")
        if not installation_id :
            raise HTTPException(
                status_code=401,
                detail="installation id missing "
            )
        review_pull_request.delay(repoName,prNum,installation_id)
        logger.info("Task sent to background worker successfull")
        return {
            "status": "successfull",
            "message" : f"pr from app.workers.review_worker import review_pull_request"
        }
        
    return {
        "status" :"ignored",
        "message" : f"Event : {eventType} ignored"
    }

