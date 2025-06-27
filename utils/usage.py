from utils.cosmos import get_container
from datetime import datetime

container = get_container("usage")

def get_today():
    return datetime.utcnow().strftime("%Y-%m-%d")

def has_free_access(user_id):
    today = get_today()
    try:
        item = container.read_item(item=user_id, partition_key=user_id)
        if item["date"] != today:
            return True  # It's a new day
        return item["count"] < 5
    except:
        return True  # No usage record yet

def increment_usage(user_id):
    today = get_today()
    try:
        item = container.read_item(item=user_id, partition_key=user_id)
        if item["date"] == today:
            item["count"] += 1
        else:
            item["count"] = 1
            item["date"] = today
        container.upsert_item(item)
    except:
        container.upsert_item({
            "id": user_id,
            "userId": user_id,
            "date": today,
            "count": 1
        })
