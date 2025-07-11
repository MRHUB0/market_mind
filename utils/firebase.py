import os
import json
import firebase_admin
from firebase_admin import credentials, auth

if not firebase_admin._apps:
    firebase_json = os.getenv("FIREBASE_ADMIN_JSON")
    if not firebase_json:
        raise ValueError("Missing FIREBASE_ADMIN_JSON environment variable")

    cred_dict = json.loads(firebase_json)
    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred)

def verify_firebase_token(token):
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token['uid']
    except Exception:
        return None
