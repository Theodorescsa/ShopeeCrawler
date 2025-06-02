import json, os, time
from crawler_by_search import *
from crawler_by_shop import *
from slugify import slugify 
from pathlib import Path
from utils import find_to_driver, parse_num_ratings
from dotenv import load_dotenv
import os

# Tải biến môi trường từ file .env
load_dotenv()

# Lấy các giá trị
chrome_path = os.getenv('CHROME_PATH')
profile_path = os.getenv('PROFILE_PATH')
profile_name = os.getenv('PROFILE_NAME')

if __name__ == "__main__":
    driver = find_to_driver(chrome_path, profile_path, profile_name)
    Path("results").mkdir(exist_ok=True)

    # shopee_search_by_shop(driver, 'yody.official')  
    # urls = crawler_item_url_by_shop(driver)
    with open(r"D:\Python\crawler\data\url\item_urls.json", "r", encoding="utf-8") as f:
        urls = json.load(f)

    print(f"🔢 Đã đọc {len(urls)} URL từ file JSON.")
    for url in urls:
        # driver = find_to_driver(
        #     r'C:\Program Files\Google\Chrome\Application\chrome.exe',
        #     r'D:\User Data',
        #     r'Profile 5'
        # )
        driver.get(url)
        time.sleep(5)
        html = driver.page_source

        item_info = crawler_item_info_by_shop(html)
        rating_count = parse_num_ratings(item_info.get("num_ratings", "0"))
        if rating_count == 0:
            print("Bị block tại url:", url)
            break
        max_pages = (rating_count // 6) + 1 if rating_count > 0 else 1
        print(f"🔢 Tổng đánh giá: {rating_count} => Dự kiến crawl {max_pages} trang")
        rating_item_info = crawl_all_ratings(driver, wait_time=2, max_pages=max_pages)

        data = {
            "product": item_info,
            "ratings": rating_item_info
        }

        product_name = item_info.get("name", "product")
        filename = f"results/{slugify(product_name)}.json"

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"✅ Saved: {filename}")
