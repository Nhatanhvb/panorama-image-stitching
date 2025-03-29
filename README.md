# Tạo Ảnh Panorama

## Mô tả
Dự án này sử dụng thuật toán ghép ảnh để tạo ra một ảnh panorama từ nhiều ảnh chồng lấp. Chương trình hỗ trợ tự động phát hiện và ghép nối các ảnh để tạo ra kết quả liền mạch.

## Tính năng
- Phát hiện và ghép nối các đặc trưng tự động.
- Hỗ trợ cắt ảnh (crop) để loại bỏ các vùng thừa.
- Tùy chọn lưu ảnh kết quả vào thư mục mong muốn.

## Cài đặt
1. Clone repository:
   ```bash
   git clone https://github.com/your-repo/panorama-image-stitching.git
   ```
2. Di chuyển vào thư mục dự án:
   ```bash
   cd panorama-image-stitching
   ```
3. Cài đặt các thư viện cần thiết:
   ```bash
   pip install opencv-python-headless numpy imutils
   ```

## Hướng dẫn sử dụng
1. Chạy chương trình:
   ```bash
   python "BTL XLA Panorama.py"
   ```
2. Chọn các ảnh cần ghép từ hộp thoại.
3. Tùy chọn "Crop ảnh" nếu muốn cắt bỏ các vùng thừa.
4. Chọn thư mục lưu ảnh kết quả.
5. Ảnh panorama sẽ được hiển thị và lưu vào thư mục đã chọn.

## Ví dụ
### Ảnh đầu vào:
- `image1.jpg`
- `image2.jpg`

### Kết quả:
- `panorama_YYYYMMDD_HHMMSS.jpg` (được lưu trong thư mục đã chọn).


