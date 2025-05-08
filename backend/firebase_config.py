import os
import json
from firebase_admin import credentials, initialize_app, db  # Import đầy đủ các module cần thiết

# Lấy nội dung JSON từ biến môi trường
firebase_config = os.getenv("FIREBASE_CONFIG")
if not firebase_config:
    raise ValueError("Biến môi trường FIREBASE_CONFIG chưa được thiết lập!")

cred = credentials.Certificate(json.loads(firebase_config))

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://buhhhhhhh-default-rtdb.firebaseio.com/'
})

def get_database():
    return db.reference()
