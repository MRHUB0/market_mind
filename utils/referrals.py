from utils.cosmos import get_container

container = get_container("referrals")

def track_referral(referrer_id, invitee_id):
    if referrer_id == invitee_id:
        return False, "Self-referral is not allowed."

    try:
        item = container.read_item(item=referrer_id, partition_key=referrer_id)
    except:
        item = {
            "id": referrer_id,
            "userId": referrer_id,
            "invitees": [],
            "unlocked": False
        }

    if invitee_id in item["invitees"]:
        return False, "This invitee has already been tracked."

    item["invitees"].append(invitee_id)

    if len(item["invitees"]) >= 3:
        item["unlocked"] = True

    container.upsert_item(item)
    return True, f"Referral tracked. Total invites: {len(item['invitees'])}"

def has_unlocked_referral(user_id):
    try:
        item = container.read_item(item=user_id, partition_key=user_id)
        return item.get("unlocked", False)
    except:
        return False
