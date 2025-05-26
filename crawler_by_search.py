import subprocess
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException

import os
from bs4 import BeautifulSoup

from utils import scroll_to_bottom
os.makedirs('data/url', exist_ok=True)


def shopee_search(driver,item,page_id=0):
    driver.get(f'https://shopee.vn/search?keyword={item}&page={page_id}')
    time.sleep(5)
def shopee_search_by_shop(driver, shop_id, page_id=0):
    driver.get(f'https://shopee.vn/{shop_id}#product_list')
    time.sleep(5)
def find_to_item(driver, item):
    scroll_to_bottom(driver) 
    time.sleep(2) 
    results = []
    items = driver.find_elements(By.CSS_SELECTOR, 'li.col-xs-2-4.shopee-search-item-result__item')
    count = 0
    for li in items:
        try:
            html = li.get_attribute('outerHTML')
            soup = BeautifulSoup(html, 'html.parser')
            count += 1
            if count>=13:
                print(html)
            # 1. Tên sản phẩm: thử selector chính xác hơn
            name_tag = soup.select_one('div.line-clamp-2.break-words.text-sm')
            if not name_tag:
                name_tag = soup.select_one('a.contents div.line-clamp-2.break-words.text-sm')
            name = name_tag.get_text(strip=True) if name_tag else ''

            # 2. Giá (có thể trong div chứa giá)
            price_tag = soup.select_one('div.flex-shrink.min-w-0.mr-1.truncate.text-shopee-primary')
            if not price_tag:
                price_tag = soup.select_one('span[data-sqe="price"]')
            price = price_tag.get_text(strip=True) if price_tag else ''

            # 3. Đánh giá sao
            rating_tag = soup.select_one('div.text-shopee-black87')
            if rating_tag and rating_tag.get_text(strip=True).replace('.', '', 1).isdigit():
                rating = rating_tag.get_text(strip=True)
            else:
                rating = ''
            # 4. Đã bán
            sold_tag = soup.select_one('div.flex.items-center > div:contains("Đã bán")')
            if not sold_tag:
                sold_tag = soup.find('div', string=lambda s: s and 'Đã bán' in s)
            sold = sold_tag.get_text(strip=True) if sold_tag else ''

            # 5. Nơi bán
            location_tag = soup.select_one('div.flex-shrink.min-w-0.truncate.text-shopee-black54')
            if not location_tag:
                location_tag = soup.select_one('div.items-center.flex._3Djp-K span')
            location = location_tag.get_text(strip=True) if location_tag else ''

            # 6. Phương thức giao hàng
            delivery_tag = soup.select_one('div._5W0f35')
            if not delivery_tag:
                for tag in soup.find_all('div'):
                    if tag and 'giao' in tag.get_text(strip=True).lower():
                        delivery_tag = tag
                        break
            delivery = delivery_tag.get_text(strip=True) if delivery_tag else ''

            # 7. Voucher (nếu có)
            voucher_tag = None
            for vtag in soup.find_all(string=True):
                if vtag and 'giảm' in vtag.lower():
                    voucher_tag = vtag
                    break
            voucher = voucher_tag.strip() if voucher_tag else ''

            # 8. Link sản phẩm (lấy href của a.contents chính xác nhất)
            a_tag = soup.select_one('a.contents[href]')
            url = a_tag['href'] if a_tag else ''

            results.append({
                "name": name,
                "price": price,
                "rating": rating,
                "sold": sold,
                "delivery": delivery,
                "location": location,
                "voucher": voucher,
                "url": url,
                "search_item": item
            })

        except Exception as e:
            print(f"Lỗi xử lý sản phẩm: {e}")

    return results
