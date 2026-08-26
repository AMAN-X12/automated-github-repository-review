import time 
import logging 
import jwt
import httpx
logger=logging.getLogger(__name__)
def generate_JWS_Token(appID, privateKey):
    timeNow= int (time.time())
    print(f"time now :{timeNow}")
    payload = {
        "iat" : timeNow - 60 ,
        "exp" : timeNow + (10*60),
        "iss" : appID
        
    }
    print(f"exp time now :{timeNow + (10*60)}")
    return jwt.encode(
        payload,
        privateKey,
        algorithm="RS256")

async def get_installation_token(installationID, jwtToken):
    url = f"https://api.github.com/app/installations/{installationID}/access_tokens"
    headers = {
             "Authorization": f"Bearer {jwtToken}",
             "Accept" : "application/vnd.github+json",
             "X-GitHub-Api-Version":"2026-03-10"
        }        
    async with httpx.AsyncClient() as client :
            response = await client.post(
                url,
                headers=headers
            )
    response.raise_for_status()
    data = response.json()
    installationToken = data["token"]  
    return installationToken 
    
async def get_pull_req(repoName, prNum, installationToken):
    url = f"https://api.github.com/repos/{repoName}/pulls/{prNum}"
    headers = {
             "Authorization": f"Bearer {installationToken}",
             "Accept" : "application/vnd.github+json",
             "X-GitHub-Api-Version":"2026-03-10"
        }
    async with httpx.AsyncClient() as client:
        response = await client.get(
            url,
            headers=headers
        )
    response.raise_for_status()
    data = response.json()
    return {
        "title" : data["title"],
        "description" : data["body"],
        "base_branch" : data["base"]["ref"],
        "head_branch" : data["head"]["ref"]
    }
    
async def get_changed_files(repoName , prNum , installationToken):
    url = f"https://api.github.com/repos/{repoName}/pulls/{prNum}/files"
    headers = {
             "Authorization": f"Bearer {installationToken}",
             "Accept" : "application/vnd.github+json",
             "X-GitHub-Api-Version":"2026-03-10"
        }
    async with httpx.AsyncClient() as client:
        response = await client.get(url,headers=headers)
    response.raise_for_status()
    dataList = response.json()
    changedFIles=[]
    for data in dataList:
        changedFIles.append({
            "fileName" : data["filename"],
            "fileStatus" : data["status"],
            "added_lines": data["additions"],
            "removed_lines":data["deletions"],
            "patch" : data.get("patch",{}),
            "number_of_changes" : data["changes"]           
    }
        )
    return changedFIles

async def get_pull_request_difference(repoName , prNum , installationToken):
    url =f"https://api.github.com/repos/{repoName}/pulls/{prNum}"
    headers = {
             "Authorization": f"Bearer {installationToken}",
             "Accept" : "application/vnd.github.diff",
             "X-GitHub-Api-Version":"2026-03-10"
        }
    async with httpx.AsyncClient() as client :
        response = await client.get(url,headers=headers)
    response.raise_for_status()
    return response.text

async def postReview(repoName , prNum , installationToken, AiResponse):
    commentsPayload = []
    for finding in AiResponse.findings:
        formatedBody = (
            f" **{finding.severity.upper()}** - {finding.category}\n\n"
            f"{finding.explanation}\n\n"
            f"**Suggestion:** {finding.suggestion}"
        )
        commentsPayload.append({
            "path": finding.file,
            "line": finding.line,
            "body": formatedBody
        })
    if commentsPayload :
            summary = f"Code review completed. found {len(commentsPayload)} issue found in pull req"
            eventType = "COMMENT"
    else :
            summary = "Code review completed. No issue Found in pull req"
            eventType = "APPROVE"
    paylaod = {
        "body" : summary,
        "event" : eventType,
        "comments":commentsPayload
    }
    url = f"https://api.github.com/repos/{repoName}/pulls/{prNum}/reviews"
    headers = {
             "Authorization": f"Bearer {installationToken}",
             "Accept" : "application/vnd.github+json",
             "X-GitHub-Api-Version":"2026-03-10"
        }
    async with httpx.AsyncClient() as client :
        response = await client.post (url,json=paylaod,headers=headers)
    if response.status_code in (200,201):
        logger.info("successfully made a post req to github")
    else :
        logger.info("post req to gihub failed")
        
    