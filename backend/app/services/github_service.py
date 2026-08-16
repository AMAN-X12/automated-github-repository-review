import time 
import logging 
import jwt
import httpx

def generate_JWS_Token(appID, privateKey):
    timeNow= int (time.time())
    print(f"time now :{timeNow}")
    payload = {
        "iat" : timeNow ,
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
    
