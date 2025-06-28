from datetime import datetime, timedelta
from utils.cosmos import get_container

container = get_container("usage")  # Use the 'usage' container

MAX_FREE_USES = 10  # Free query limit

def has_free_access(user_id):
    query = """
    SELECT VALUE COUNT(1) FROM c 
    WHERE c.user_id = @user_id AND c._ts > @start_ts
    """
    params = [
        {"name": "@user_id", "value": user_id},
        {"name": "@start_ts", "value": int((datetime.utcnow() - timedelta(days=1)).timestamp())}
    ]
    result = list(container.query_items(
        query=query,
        parameters=params,
        enable_cross_partition_query=True
    ))
    return result[0] < MAX_FREE_USES

def increment_usage(user_id):
    container.upsert_item({
        "id": f"{user_id}-{datetime.utcnow().isoformat()}",
        "user_id": user_id,
        "timestamp": datetime.utcnow().isoformat()
    })
