from flask import Blueprint, jsonify
from bs4 import BeautifulSoup
import json

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

bp = Blueprint("crawling", __name__)

# service = Service(executable_path="/usr/bin/chromedriver-linux64/ chromedriver")

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--single-process")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome()

# driver = webdriver.Chrome(service=service, options=chrome_options)

url = "https://www.google.com"
driver.get(url)

# case 0 - DevToolsActivePort file doesn't exist 로 실패
# driver = webdriver.Chrome()
# case 1 - 실패 path 지정하라고 뜸.
# driver = webdriver.Chrome("./chromedriver", chrome_options=chrome_options)
# case 2 - DevToolsActivePort file doesn't exist 로 실패
# driver = webdriver.Chrome(
#     executable_path="/usr/bin/chromedriver", chrome_options=chrome_options
# )
# case 3 -  (unknown error: DevToolsActivePort file doesn't exist) (The process started from chrome location /usr/bin/chromium is no longer running, so ChromeDriver is assuming that Chrome has crashed.)
# driver = webdriver.Chrome(chrome_options=chrome_options)

# options = Options()
# options.binary_location = (
#     "/usr/bin/google-chrome"  # Chrome binary location specified here
# )


# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--no-sandbox")
# # chrome_options.add_argument("--single-process")
# chrome_options.add_argument("--disable-dev-shm-usage")
# chrome_options.add_argument("--remote-debugging-port=9222")  # 포트 변경?


# path = "/usr/bin/chromedriver"
# # driver = webdriver.Chrome(path, chrome_options=chrome_options)


# driver = webdriver.Chrome(
#     chrome_options=chrome_options,
# )

# service = Service(executable_path="./chromedriver.exe")


# url = "https://www.google.com"
# driver.get(url)


def get_today_menu(li_element):
    menu_info = []

    dl_elements = li_element.find_all("dl")

    for dl in dl_elements:
        dd_elements = dl.find_all("dd", class_="ddCafeTeriaInfo")

        # dd 태그에서 정보를 가져와서 줄바꿈 문자로 분할
        for dd in dd_elements:
            text = dd.get_text(strip=False)
            text = text.replace("\n\n", "-")
            items = text.split("-")

            if items:
                for i in range(len(items)):
                    menu_name = items[i].strip()  # 메뉴 이름

                    # Null 값인 경우 무시
                    if not menu_name:
                        continue

                    # 결과 리스트에 추가
                    menu_info.append(menu_name)

    return menu_info


# 일주일 동안의 식단 정보를 가져오는 함수
def get_weekly_menus(soup):
    weekly_menus = {}
    ul_element = soup.select_one("ul#ulWeekDtInfo")  # ul 태그 선택

    if ul_element:
        li_elements = ul_element.find_all("li")  # 모든 li 태그 선택

        for li_element in li_elements:
            # 날짜 정보 가져오기
            span = li_element.select_one("p span").get_text(strip=True)
            day = li_element.select_one("p b").get_text(strip=True)
            date_info = f"{span} {day}"  # 날짜 정보 형식 수정
            menus = get_today_menu(li_element)
            weekly_menus[date_info] = menus
            print(date_info)  # 날짜 정보 출력
            print(menus)  # 메뉴 정보 출력

    return weekly_menus


# 해당 URL의 HTML을 BeautifulSoup 객체로 반환하는 함수
def get_html(url: str) -> BeautifulSoup:
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    return soup


@bp.route("/crawling")
def crawling():
    website_url = "https://www.dongduk.ac.kr/kor/life/cafeteria.do"

    soup = get_html(website_url)
    weekly_menus = get_weekly_menus(soup)

    return json.dumps(weekly_menus, ensure_ascii=False, indent=4)
