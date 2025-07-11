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
DAILY_LIMIT = 10

def has_free_access(user_id):
    doc_ref = db.collection("usage").document(user_id)
    doc = doc_ref.get()
    if not doc.exists:
        return True
    return doc.to_dict().get("count", 0) < DAILY_LIMIT

def increment_usage(user_id):
    doc_ref = db.collection("usage").document(user_id)
    doc = doc_ref.get()
    if doc.exists:
        count = doc.to_dict().get("count", 0) + 1
        doc_ref.set({"count": count})
    else:
        doc_ref.set({"count": 1})
