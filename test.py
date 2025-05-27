import json
import math

# Đường dẫn đến file gốc
input_file = "data/url/item_urls_update.json"

# Đọc danh sách URL
with open(input_file, "r", encoding="utf-8") as f:
    urls = json.load(f)

# Số lượng file muốn chia
num_parts = 4
total_urls = len(urls)
chunk_size = math.ceil(total_urls / num_parts)

# Chia và lưu từng phần
for i in range(num_parts):
    start = i * chunk_size
    end = start + chunk_size
    chunk = urls[start:end]

    output_file = f"data/url/item_urls_part{i+1}.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(chunk, f, ensure_ascii=False, indent=2)

    print(f"✅ Đã tạo {output_file} với {len(chunk)} URL")
