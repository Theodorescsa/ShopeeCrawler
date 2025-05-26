import subprocess
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
def scroll_to_bottom(driver, pause_time=1.0, step=300, delay=0.05):

    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        for i in range(0, last_height, step):
            driver.execute_script(f"window.scrollTo(0, {i});")
            time.sleep(delay)

        time.sleep(pause_time)

        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            break
        last_height = new_height
def find_to_driver(chrome_path, user_data_dir, profile_name, retry=5):
    """
    Mở Chrome bằng remote debugging port và kết nối với Selenium.
    """
    # Mở Chrome bằng subprocess nếu chưa có
    subprocess.Popen([
        chrome_path,
        "--remote-debugging-port=9222",
        f"--user-data-dir={user_data_dir}",
        f"--profile-directory={profile_name}"
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Cố gắng kết nối lại nhiều lần nếu chưa khởi động xong
    for attempt in range(retry):
        try:
            options = Options()
            options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
            driver = webdriver.Chrome(options=options)
            print("✅ Connected to Chrome via remote debugging.")
            return driver
        except WebDriverException as e:
            print(f"⏳ Waiting for Chrome (attempt {attempt + 1}/{retry})...")
            time.sleep(2)
    raise RuntimeError("❌ Không thể kết nối tới Chrome với remote debugging.")
def find_to_driver_incognito():
    chrome_options = Options()
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--dns-prefetch-disable")
    driver = webdriver.Chrome(options=chrome_options)
    return driver