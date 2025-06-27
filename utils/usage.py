from utils.cosmos import get_container
from utils.referrals import has_unlocked_referral

container = get_container("usage")

DAILY_LIMIT = 5

def has_free_access(user_id):
    # Check if user is already unlocked via referrals
    if has_unlocked_referral(user_id):
        return True

    try:
        item = container.read_item(item=user_id, partition_key=user_id)
        return item.get("count", 0) < DAILY_LIMIT
    except:
        return True  # No usage found, allow access

def increment_usage(user_id):
    try:
        item = container.read_item(item=user_id, partition_key=user_id)
    except:
        item = {
            "id": user_id,
            "userId": user_id,
            "count": 0
        }

    item["count"] = item.get("count", 0) + 1
    container.upsert_item(item)
