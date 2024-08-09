from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import urllib.parse

def google_search(query):
    driver = None
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(options=options)

        driver.get('https://www.google.com')
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'q'))
        )
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)
        time.sleep(3)

        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.g'))
        )
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        search_results = []
        for g in soup.find_all('div', class_='g'):
            link = g.find('a', href=True)
            if link:
                link_url = link['href']
                # Check if the URL is a Tiki.vn search URL
                print(link_url)
                # if "tiki.vn/search" in link_url:
                    # Verify and decode URL to ensure it contains search query parameters
                parsed_url = urllib.parse.urlparse(link_url)
                query_params = urllib.parse.parse_qs(parsed_url.query)
                if 'q' in query_params:
                    title = g.find('h3')
                    if title:
                        search_results.append({
                            'name': title.text,
                            'link': link_url
                        })

        return search_results

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if driver:
            driver.quit()

def search_google(object, value=None, describe=None):
    search_query = f"tiki.vn/search?q={object} giá {value} {describe}"
    # search_query = f"shopee.vn/search?keyword="
    results = google_search(search_query)
    print(results)
    return results

# Example usage
# links = search_google('điều hòa daikin', '', '')
# print(links)
# [{'name': 'Đèn Năng Lượng Mặt Trời Kitawa - Giá Rẻ, Bảo Hành 5 Năm', 'link': 'https://kitawa.vn/den-nang-luong-mat-troi-solar-light-kitawa'}, {'name': 'Đèn Năng Lượng Mặt Trời Rạng Đông - Điều Khiển Từ Xa', 'link': 'https://rangdongstore.vn/den-nang-luong-mat-troi-c-2201000029/'}, {'name': 'Xưởng đèn năng lượng mặt trời – CHIẾU SÁNG HIẾU KIỆT', 'link': 'https://hieukietsolar.com/'}, {'name': 'Đèn Led Siêu Sáng Năng Lượng Mặt Trời Giá Rẻ', 'link': 'https://dienquang.com/collections/den-led-solar-nang-luong-mat-troi'}, {'name': 'Báo Giá Đèn Năng Lượng Mặt Trời 300W Cao Cấp [Giảm ...', 'link': 'https://hainamsolar.net/den-led-nang-luong-mat-troi-300w/'}, {'name': 'Các mẫu đèn năng lượng mặt trời 100w Chính hãng Giá rẻ', 'link': 'https://tpsolar.vn/den-nang-luong-mat-troi-100w'}, {'name': 'Đèn Năng Lượng Mặt Trời Siêu Sáng Chống Nước IP67', 'link': 'https://garan.vn/collections/den-nang-luong-mat-troi'}, {'name': 'Đèn năng lượng mặt trời giá tốt nhất', 'link': 'https://sepower.vn/den-nang-luong-mat-troi-9-11.html'}, {'name': 'Đèn năng lượng mặt trời solar light 60w NT-SF60', 'link': 'https://ntechsolar.vn/den-nang-luong-mat-troi-solar-light-60w-nt-sf60'}]