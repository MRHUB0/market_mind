import firebase_admin
from firebase_admin import credentials, auth
import os
import json

# Initialize Firebase Admin SDK
if not firebase_admin._apps:
    firebase_json_raw = os.getenv("FIREBASE_ADMIN_JSON")
    if not firebase_json_raw:
        raise Exception("FIREBASE_ADMIN_JSON not set in .env")

    firebase_json = json.loads(firebase_json_raw)
    firebase_json["private_key"] = firebase_json["private_key"].replace("\\n", "\n")

    cred = credentials.Certificate(firebase_json)
    firebase_admin.initialize_app(cred)

def verify_firebase_token(token):
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token["uid"]
    except Exception as e:
        return None
