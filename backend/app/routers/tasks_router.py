from fastapi import APIRouter
from app.worker.tasks import fetch_all_rss_feeds

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/trigger_collection")
async def trigger_collection():
    """
    Triggers the Celery task to fetch all RSS feeds in the background.
    """
    task = fetch_all_rss_feeds.delay()
    return {"message": "Data collection task has been triggered.", "task_id": task.id}
