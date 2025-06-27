from datetime import datetime

# In-memory usage tracker (replace with Cosmos DB or Firestore later)
usage_db = {}

def get_today():
    return datetime.utcnow().strftime("%Y-%m-%d")

def check_usage(user_id):
    today = get_today()
    usage = usage_db.get(user_id, {})
    if usage.get("date") != today:
        # Reset daily usage
        usage_db[user_id] = {"date": today, "count": 0}
    return usage_db[user_id]["count"]

def increment_usage(user_id):
    today = get_today()
    if user_id not in usage_db or usage_db[user_id]["date"] != today:
        usage_db[user_id] = {"date": today, "count": 1}
    else:
        usage_db[user_id]["count"] += 1

def has_free_access(user_id):
    count = check_usage(user_id)
    return count < 5
