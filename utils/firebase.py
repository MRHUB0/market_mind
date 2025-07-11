import os
import json
import firebase_admin
from firebase_admin import credentials

# Only initialize once
if not firebase_admin._apps:
    firebase_json = os.getenv("FIREBASE_ADMIN_JSON")
    if not firebase_json:
        raise ValueError("Missing FIREBASE_ADMIN_JSON environment variable")

    cred_dict = json.loads(firebase_json)
    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred)
