import os
import json
from firebase_admin import credentials, initialize_app, db  # Import đầy đủ các module cần thiết

# Lấy nội dung JSON từ biến môi trường
firebase_config = os.getenv("FIREBASE_CONFIG")
if not firebase_config:
    raise ValueError("Biến môi trường FIREBASE_CONFIG chưa được thiết lập!")

# Chuyển chuỗi JSON thành dictionary
firebase_config_dict = json.loads(firebase_config)

# Khởi tạo Firebase Admin SDK
cred = credentials.Certificate(firebase_config_dict)
initialize_app(cred, {
    'databaseURL': 'https://buhhhhhhh-default-rtdb.firebaseio.com/'
})

# Hàm trả về tham chiếu đến database
def get_database():
    return db.reference()
