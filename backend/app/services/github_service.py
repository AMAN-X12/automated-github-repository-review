import time 
import logging 
import jwt
import httpx

def generate_JWS_Token(appID, privateKey):
    timeNow= int (time.time())
    print(f"time now :{timeNow}")
    payload = {
        "iat" : timeNow,
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
    data = response.json()
    installationToken = data["token"]  
    return installationToken 
    