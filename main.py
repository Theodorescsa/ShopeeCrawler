import json, os, time
from crawler_by_search import *
from crawler_by_shop import *
from slugify import slugify 
from pathlib import Path
from utils import find_to_driver, parse_num_ratings
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
        rating_count = parse_num_ratings(item_info.get("num_ratings", "0"))
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
        driver.close()