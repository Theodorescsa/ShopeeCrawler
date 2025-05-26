import time
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException

def shopee_search_by_shop(driver, shop_id):
    driver.get(f'https://shopee.vn/{shop_id}#product_list')
    time.sleep(5)

def crawler_item_url_by_shop(driver, wait_time=2, max_pages=10):
    all_urls = []
    page = 1

    while True:
        print(f"📄 Đang lấy URL sản phẩm ở trang {page}...")
        time.sleep(wait_time)  # đợi nội dung trang tải

        try:
            container = driver.find_element(By.CLASS_NAME, "shop-search-result-view")
            html = container.get_attribute("innerHTML")
        except NoSuchElementException:
            print("❌ Không tìm thấy danh sách sản phẩm.")
            break

        soup = BeautifulSoup(html, "html.parser")
        a_tags = soup.find_all("a", class_="contents")
        urls = ["https://shopee.vn" + a["href"] for a in a_tags if a.has_attr("href")]
        print(f"🔗 Tìm thấy {len(urls)} URL ở trang {page}")
        all_urls.extend(urls)

        # Xử lý click nút next
        try:
            next_btn = driver.find_element(By.CSS_SELECTOR, ".shopee-icon-button--right")
            if "disabled" in next_btn.get_attribute("class"):
                print("✅ Đã đến trang cuối cùng.")
                break

            print("➡️ Click nút next bằng JS...")
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth'});", next_btn)
            time.sleep(0.5)
            driver.execute_script("arguments[0].click();", next_btn)

            page += 1
            if page > max_pages:
                print("🚧 Đã đến giới hạn số trang.")
                break
        except (NoSuchElementException, ElementClickInterceptedException) as e:
            print("⚠️ Không thể click next:", e)
            break

    return all_urls


def crawler_item_info_by_shop(html: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")

    def get_text(selector):
        el = soup.select_one(selector)
        return el.get_text(strip=True) if el else ""

    def get_all_texts(selector):
        return [el.get_text(strip=True) for el in soup.select(selector)]

    def get_attribute(selector, attr):
        el = soup.select_one(selector)
        return el[attr] if el and el.has_attr(attr) else ""

    name = get_text("h1.vR6K3w")
    # Giá
    price = get_text("button.btn-solid-primary div.Rt4WYl")

    # Đã bán
    sold = get_text("div.aleSBU span.AcmPRb")

    # Rating
    rating = get_text("button.e2p50f > div.F9RHbS")

    # Số lượng đánh giá
    num_ratings = get_text("button.e2p50f:nth-of-type(2) > div.F9RHbS")


    sizes = []
    colors = []

    # Duyệt các section có tiêu đề để phân biệt size/màu
    for section in soup.select("section"):
        h2 = section.select_one("h2")
        if not h2:
            continue
        title = h2.get_text(strip=True).lower()
        options = [btn.get_text(strip=True) for btn in section.select("button.sApkZm")]

        if "màu sắc" in title:
            colors = options
        elif "size" in title or "kích cỡ" in title:
            sizes = options
    # Số lượng tồn kho
    stock_text = get_text("section:has(h2:contains('Số lượng')) div._9m0o30 + div")
    stock = stock_text.replace("sản phẩm có sẵn", "").strip()

    # Danh mục sản phẩm
    categories = get_all_texts("div.idLK2l a")

    return {
        "name": name,
        "price": price,
        "sold": sold,
        "rating": rating,
        "num_ratings": num_ratings,
        "sizes": sizes,
        "colors": colors,
        "stock_available": stock,
        "categories": categories
    }
    

def crawler_rating_info_by_shop(html: str) -> list:
    soup = BeautifulSoup(html, "html.parser")
    ratings = []

    for item in soup.select(".shopee-product-rating"):
        data = {}
        name_tag = item.select_one(".shopee-product-rating__author-name")
        data["author"] = name_tag.get_text(strip=True) if name_tag else ""

        time_tag = item.select_one(".shopee-product-rating__time")
        if time_tag:
            full_text = time_tag.get_text(strip=True)
            if "|" in full_text:
                date_part, category_part = full_text.split("|", 1)
                data["date"] = date_part.strip()
                data["variant"] = category_part.replace("Phân loại hàng:", "").strip()
            else:
                data["date"] = full_text.strip()
                data["variant"] = ""

        stars = item.select(".shopee-product-rating__rating svg")
        data["stars"] = len(stars)

        content_blocks = item.select("div[style*='white-space: pre-wrap;'] div")
        content = []
        extra_fields = {"chất liệu": "", "màu sắc": "", "đúng với mô tả": ""}
        for block in content_blocks:
            text = block.get_text(strip=True)
            lower = text.lower()
            if "chất liệu:" in lower:
                extra_fields["chất liệu"] = text.split(":")[-1].strip()
            elif "màu sắc:" in lower:
                extra_fields["màu sắc"] = text.split(":")[-1].strip()
            elif "đúng với mô tả:" in lower:
                extra_fields["đúng với mô tả"] = text.split(":")[-1].strip()
            else:
                content.append(text)

        data["comment"] = "\n".join(content).strip()
        data.update(extra_fields)

        image_tags = item.select(".rating-media-list__image-wrapper img")
        data["images"] = [img["src"] for img in image_tags if img.has_attr("src")]

        video_tags = item.select(".rating-media-list__zoomed-video-item")
        data["videos"] = [v["src"] for v in video_tags if v.has_attr("src")]

        ratings.append(data)

    return ratings


def crawl_all_ratings(driver, wait_time=2, max_pages=20):
    all_ratings = []
    page = 1

    while True:
        print(f"🧭 Crawling page {page}...")
        time.sleep(wait_time)  # đợi nội dung load
        html = driver.page_source
        ratings = crawler_rating_info_by_shop(html)
        if not ratings:
            print("⛔ Không còn đánh giá, dừng.")
            break
        all_ratings.extend(ratings)

        try:
            next_btn = driver.find_element(By.CSS_SELECTOR, ".shopee-icon-button--right")
            # Nếu button bị disable, thoát
            if "disabled" in next_btn.get_attribute("class"):
                print("✅ Đã đến trang cuối cùng.")
                break
            # Scroll đến nút nếu cần
            print("🔽 Đang scroll đến nút next...")
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth'});", next_btn)
            time.sleep(0.5)
            driver.execute_script("arguments[0].click();", next_btn)
            page += 1
            if page > max_pages:
                print("🚧 Đã đến giới hạn số trang (max_pages).")
                break
        except (NoSuchElementException, ElementClickInterceptedException) as e:
            print("❌ Không thể click nút next:", e)
            break

    return all_ratings
