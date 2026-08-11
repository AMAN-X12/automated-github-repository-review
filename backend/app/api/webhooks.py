from fastapi import APIRouter, Request

router = APIRouter(prefix="/webhooks", tags=["webhooks"])


@router.post("/github")
async def github_webhook(request: Request):
    # TODO:
    # 1. Verify GitHub webhook signature
    # 2. Parse event headers
    # 3. Ignore unsupported events
    # 4. Enqueue the review job
    return {"status": "received"}
