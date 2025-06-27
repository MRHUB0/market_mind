from utils.cosmos import get_container
from utils.referrals import get_referral_credits

container = get_container("usage")

BASE_DAILY_LIMIT = 5

def has_free_access(user_id):
    try:
        usage_item = container.read_item(item=user_id, partition_key=user_id)
        used = usage_item.get("count", 0)
    except:
        used = 0

    referral_credits = get_referral_credits(user_id)
    total_limit = BASE_DAILY_LIMIT + referral_credits

    return used < total_limit

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
