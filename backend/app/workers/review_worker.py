from celery import Celery
from app.services.github_service import (generate_JWS_Token, get_installation_token,get_pull_req, get_changed_files,get_pull_request_difference,postReview)
from app.services.llm_service import (analyze_pr_diff)
from app.core.config import settings

celery_app = Celery("review_worker", broker=settings.redis_url)


@celery_app.task(bind = True, max_retries=3)
def review_pull_request(repository: str, pull_request_number: int, installation_id:int):
   try:
     with open("../automated-pr-reviewer-private-token.pem","r") as f :
            privateKey = f.read()
        if not privateKey:
            raise HTTPException(
                status_code  = 401,
                detail= "missing private key "
            )
        jwtToken = generate_JWS_Token(os.getenv("GITHUB_APP_ID") , privateKey=privateKey)
        logger.info(f"jwt token successfully created")  
        
        installationToken = await  get_installation_token(installation_id,jwtToken)
        if not installationToken:
            raise HTTPException(
                status_code=500,
                detail="installation token generation failed"
            )
        logger.info(f"installation token received successfully")
        prData= await get_pull_req(repoName , prNum , installationToken)
        logger.info(f"title of repository : {prData["title"]}")
        logger.info(f"description of repository : {prData["description"]}")
        logger.info(f"base repository : {prData["base_branch"]}")
        logger.info(f"head repository : {prData["head_branch"]}")
        
        fileChanged = await get_changed_files(repoName,prNum, installationToken)
        logger.info(f"files cahnegd meta deta are : {fileChanged}")
        
        prDifferences = await get_pull_request_difference(repoName, prNum, installationToken)
        logger.info(f"the differences in files includes : {prDifferences}")
        
        llmReview = await analyze_pr_diff(prDifferences)
        for finding in llmReview.findings:
            logger.info(f"[{finding.severity}] {finding.file}:{finding.line} - {finding.explanation} {finding.category} {finding.suggestion}")
        if llmReview.findings:
           await postReview(repoName,prNum,installationToken,llmReview)
           
     return {"status": "queued"}
    except Exception as e:
        raise self.retry(exc=e, countdown=10)

