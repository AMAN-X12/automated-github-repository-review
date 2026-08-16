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
from app.services.github_service import generate_JWS_Token

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
        repoName = payload.get("repository", {}).get("full_name","unknown_repo" )
        prNum = payload.get("pull_request", {}).get("number","unknown number")
        prAuthor = payload.get("pull_request", {}).get("user", {}).get("login","unknown_author")
        logger.info(f"rpository : {repoName}")
        logger.info(f"pull req number {prNum}")
        logger.info(f"owner {prAuthor}")
        logger.info(f"status {action}")
        with open("automated-pr-reviewer-private-token.pem","r") as f :
            privateKey = f.read()
        if privateKey is None:
            raise HTTPException(
                status = 401,
                detail= "missing private key "
            )
        jwtToken = generate_JWS_Token(os.getenv("GITHUB_APP_ID") , privateKey=privateKey)
        logger.info(f"jwt token successfully created")
        return {
            "status": "successfull",
            "message" : f"pr event : {eventType} logged"
        }

    return {
        "status" :"ignored",
        "message" : f"Event : {eventType} ignored"
    }

