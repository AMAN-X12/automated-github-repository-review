import time 
import logging 
import jwt

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
    
