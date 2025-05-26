import json, os, time
from crawler_by_search import *
from crawler_by_shop import *
from slugify import slugify 
from pathlib import Path
from utils import find_to_driver
if __name__ == "__main__":
    driver = find_to_driver(
        r'C:\Program Files\Google\Chrome\Application\chrome.exe',
        r'D:\User Data',
        r'Profile 5'
    )

    Path("results").mkdir(exist_ok=True)

    shopee_search_by_shop(driver, 'anyoung.wear')  
    urls = crawler_item_url_by_shop(driver)
    for url in urls:
        driver = find_to_driver(
            r'C:\Program Files\Google\Chrome\Application\chrome.exe',
            r'D:\User Data',
            r'Profile 5'
        )
        driver.execute_script(f"window.open('{url}');")
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(6)
        html = driver.page_source

        item_info = crawler_item_info_by_shop(html)
        rating_item_info = crawl_all_ratings(driver, wait_time=2, max_pages=10)

        # Kết hợp dữ liệu
        data = {
            "product": item_info,
            "ratings": rating_item_info
        }

        # Tạo tên file từ tên sản phẩm
        product_name = item_info.get("name", "product")
        filename = f"results/{slugify(product_name)}.json"

        # Ghi ra file JSON
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"✅ Saved: {filename}")
        driver.close()