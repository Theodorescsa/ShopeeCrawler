# ShopeeCrawler
# 🛍️ Shopee Shop Crawler

Một công cụ **Python + Selenium** giúp bạn crawl sản phẩm và đánh giá từ **một shop cụ thể** trên Shopee.

## 📁 Cấu trúc dự án

├── crawler_by_shop.py # Hàm crawl sản phẩm và đánh giá từ shop
├── utils.py # Hàm khởi tạo trình duyệt Selenium
├── main.py # Script chính để chạy toàn bộ quá trình crawl
├── results/ # Thư mục lưu file JSON kết quả
├── requirements.txt # Thư viện Python cần cài
└── README.md # Tài liệu hướng dẫn sử dụng

## ⚙️ Yêu cầu hệ thống

- Python 3.11+
- Google Chrome (đã cài trên máy)
- ChromeDriver phù hợp với phiên bản Chrome
- Hệ điều hành: Windows

---

## 📦 Cài đặt thư viện

```bash
pip install -r requirements.txt

🧰 Cấu hình trình duyệt
Code sử dụng Chrome ở chế độ remote debugging để sử dụng profile đã đăng nhập.
Cần cấu hình 3 tham số trong main.py:
find_to_driver(
    chrome_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',  # Đường dẫn Chrome
    user_data_dir=r'D:\User Data',                                          # Thư mục user data của Chrome
    profile_name=r'Profile 5'                                               # Tên profile bạn đang dùng để đăng nhập Shopee
)
🔑 Cách lấy đúng profile Chrome:
Gõ chrome://version trong thanh địa chỉ.
Profile Path: C:\Users\yourname\AppData\Local\Google\Chrome\User Data\Profile 5
Tách thành:

user_data_dir = C:\Users\yourname\AppData\Local\Google\Chrome\User Data

profile_name = Profile 5

🚀 Cách chạy
python main.py
✨ Chức năng chính
Mở trang shop Shopee từ truy cập vào 1 shop và lấy id của shop đó trên url
Dán lại vào file main.py
📝 Kết quả đầu ra
Ví dụ: results/ao-thun-nam-cotton.json
{
  "product": {
    "name": "Áo Thun Nam Cotton",
    "price": "250.000",
    "sold": "1,5k",
    "rating": "4.9",
    "num_ratings": "350",
    "sizes": ["M", "L", "XL"],
    "colors": ["Đen", "Trắng"],
    "stock_available": "120",
    "categories": ["Thời Trang", "Áo Nam"]
  },
  "ratings": [
    {
      "author": "nguyenvana",
      "date": "2024-05-20",
      "variant": "Size: M | Màu sắc: Trắng",
      "stars": 5,
      "comment": "Áo đẹp, chất vải tốt.",
      "chất liệu": "cotton",
      "màu sắc": "trắng",
      "đúng với mô tả": "đúng",
      "images": ["https://cf.shopee.vn/image1.jpg"],
      "videos": []
    },
    ...
  ]
}
💡 Gợi ý sử dụng nâng cao
Kết hợp dữ liệu này để phân tích cảm xúc người dùng hoặc thống kê sản phẩm theo phân loại.

Tích hợp với Power BI hoặc Excel để trực quan hóa dữ liệu đánh giá.

🛑 Lưu ý
Shopee có thể chặn bot. Hãy dùng Chrome profile thật đã login để tránh CAPTCHA.

Không nên crawl quá nhanh, nên giữ delay mặc định trong code (wait_time ≥ 2s).

Hạn chế gọi liên tục trong thời gian dài để tránh IP bị giới hạn.

Nếu gặp trường hợp verify capcha lỗi thì mở tab mới bên cạnh truy cập shopee.vn để thao tác vượt capcha, vượt thành công tắt web chạy lại code
