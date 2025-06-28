referral_data = {}  # Replace with Firestore or Cosmos DB later

def track_referral(referrer_id, invitee_id):
    if referrer_id == invitee_id:
        return False, "Self-referral is not allowed."

    if referrer_id not in referral_data:
        referral_data[referrer_id] = {
            "invitees": set(),
            "unlocked": False
        }

    ref = referral_data[referrer_id]
    if invitee_id in ref["invitees"]:
        return False, "This invitee has already been tracked."

    ref["invitees"].add(invitee_id)

    if len(ref["invitees"]) >= 3:
        ref["unlocked"] = True

    return True, f"Referral tracked. Total invites: {len(ref['invitees'])}"
