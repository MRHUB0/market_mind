import os
import json
import firebase_admin
from firebase_admin import credentials, firestore

if not firebase_admin._apps:
    firebase_json = os.getenv("FIREBASE_ADMIN_JSON")
    if not firebase_json:
        raise ValueError("Missing FIREBASE_ADMIN_JSON environment variable")

    cred_dict = json.loads(firebase_json)
    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred)

db = firestore.client()

def track_referral(referrer_id, invitee_id):
    if referrer_id == invitee_id:
        return False, "Self-referral is not allowed."

    ref_doc = db.collection("referrals").document(referrer_id)
    ref_data = ref_doc.get().to_dict() or {"invitees": [], "unlocked": False}

    if invitee_id in ref_data["invitees"]:
        return False, "This invitee has already been tracked."

    ref_data["invitees"].append(invitee_id)
    if len(ref_data["invitees"]) >= 3:
        ref_data["unlocked"] = True
    ref_doc.set(ref_data)

    return True, f"Referral tracked. Total invites: {len(ref_data['invitees'])}"

def get_referral_credits(user_id):
    ref_data = db.collection("referrals").document(user_id).get().to_dict()
    return len(ref_data.get("invitees", [])) if ref_data else 0
