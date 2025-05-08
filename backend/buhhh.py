from flask import Flask, request, jsonify
import os
from backend.firebase_config import get_database
from flask_cors import CORS
from imagekitio import ImageKit

app = Flask(__name__)
db_ref = get_database().child('userList')  # Tham chiếu tới danh sách người dùng trong Firebase
CORS(app)  # Cho phép tất cả các nguồn truy cập
# Cấu hình ImageKit từ Environment Variables
imagekit = ImageKit(
    private_key=os.getenv("IMAGEKIT_PRIVATE_KEY"),  # Lấy từ biến môi trường
    public_key=os.getenv("IMAGEKIT_PUBLIC_KEY"),    # Lấy từ biến môi trường
    url_endpoint=os.getenv("IMAGEKIT_URL_ENDPOINT") # Lấy từ biến môi trường
)
# API để lấy danh sách người dùng
@app.route('/users', methods=['GET'])
def get_users():
    user_list = db_ref.get() or []
    return jsonify(user_list), 200
# API để thêm người dùng
@app.route('/users', methods=['POST'])
def add_user():
    data = request.json
    username = data.get('username')
    if not username:
        return jsonify({"error": "Tên người dùng không hợp lệ!"}), 400

    user_list = db_ref.get() or []
    if username in user_list:
        return jsonify({"error": "Người dùng đã tồn tại!"}), 400

    user_list.append(username)
    db_ref.set(user_list)
    return jsonify({"message": f"Đã thêm người dùng: {username}"}), 200

# API để xóa người dùng
@app.route('/users', methods=['DELETE'])
def delete_user():
    data = request.json
    username = data.get('username')
    if not username:
        return jsonify({"error": "Tên người dùng không hợp lệ!"}), 400

    user_list = db_ref.get() or []
    if username not in user_list:
        return jsonify({"error": "Người dùng không tồn tại!"}), 400

    user_list.remove(username)
    db_ref.set(user_list)
    return jsonify({"message": f"Đã xóa người dùng: {username}"}), 200

# Thư mục lưu trữ ảnh trên laptop
UPLOAD_FOLDER = 'uploaded_images'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Lưu file vào thư mục trên laptop
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    return jsonify({"message": "File uploaded successfully", "file_path": file_path}), 200
# API xử lý logic khi nhấn nút "buhh"
@app.route('/check', methods=['POST'])
def check():
    try:
        print("API /check được gọi")  # Ghi log khi API được gọi
        data = request.json
        username = data.get('username')
        print(f"Received username: {username}")  # Ghi log username nhận được

        # Lấy danh sách người dùng từ Firebase
        user_list = db_ref.get() or []
        print(f"User list from Firebase: {user_list}")  # Ghi log danh sách người dùng

        if username in user_list:
            if username == "ysiducw":
                return jsonify({"message": "Chào mừng Admin!"}), 200
            else:
                return jsonify({"message": f"Chào mừng {username}!"}), 200
        else:
            return jsonify({"error": "Tên người dùng không tồn tại hoặc không hợp lệ!"}), 400
    except Exception as e:
        print(f"Lỗi khi xử lý API /check: {e}")
        return jsonify({"error": "Lỗi server"}), 500
if __name__ == '__main__':
    app.run(debug=True)
