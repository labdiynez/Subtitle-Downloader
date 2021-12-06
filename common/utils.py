"""
This module is for common tool.
"""
import os
from urllib import request
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import wget


def get_season_number(string):
    """Get season number"""
    number = {
        '一': '1',
        '二': '2',
        '三': '3',
        '四': '4',
        '五': '5',
        '六': '6',
        '七': '7',
        '八': '8',
        '九': '9',
        '十': '10',
        '十一': '11',
        '十二': '12',
        '十三': '13',
        '十四': '14',
        '十五': '15',
        '十六': '16',
        '十七': '17',
        '十八': '18',
        '十九': '19',
        '二十': '20'
    }
    return str(number.get(string)).zfill(2) if number.get(string) else string.zfill(2)


def check_url_exist(url, print_error=False):
    """Check url exist"""
    try:
        request.urlopen(url)
    except HTTPError as exception:
        # Return code error (e.g. 404, 501, ...)
        if print_error:
            print('HTTPError: {}'.format(exception.code))
        return False
    except URLError as exception:
        # Not an HTTP-specific error (e.g. connection refused)
        if print_error:
            print('URLError: {}'.format(exception.reason))
        return False
    else:
        return True


def get_static_html(url):
    """Get static html"""
    try:
        headers = {
            'User-Agent': 'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        }
        req = request.Request(url, headers=headers)
        response = request.urlopen(req)
        return BeautifulSoup(response.read(), 'lxml')

    except HTTPError as exception:
        print(f"HTTPError: {exception.code}")
    except URLError as exception:
        print(f"URLError: {(exception.reason)}")


def get_dynamic_html(url, headless=True):
    """Get html render by js"""
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument('--headless')
    options.add_argument('window-size=1920,1080')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--autoplay-policy=no-user-gesture-required')
    options.add_argument('--lang=zh-TW')
    options.add_experimental_option(
        'prefs', {'intl.accept_languages': 'zh,zh_TW'})
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    driver = webdriver.Chrome('chromedriver', options=options)
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {
        "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})
    driver.get(url)
    driver.set_page_load_timeout(110)
    return driver


def find_visible_element_by_id(driver, id_text):
    return WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, id_text)))


def find_visible_element_by_xpath(driver, xpath):
    return WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, xpath)))


def find_visible_element_clickable_by_xpath(driver, xpath):
    return WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))


def find_present_element_by_xpath(driver, xpath):
    return WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))


def get_locale(driver):
    return driver.execute_script("return window.navigator.language")


def download_file(url, path):
    if check_url_exist(url):
        wget.download(url, out=path)
        print(f'\n{os.path.basename(path)}\t...下載完成')
    else:
        print("找不到檔案")


def convert_subtitle(folder_path, platform=''):
    if platform:
        os.system(
            f'python3 subtitle_tool.py "{folder_path}" -c -z {platform}')
    else:
        os.system(
            f'python3 subtitle_tool.py "{folder_path}" -c')


def merge_subtitle(folder_path, file_name):
    os.system(f'python3 subtitle_tool.py "{folder_path}" -m {file_name}')


def save_html(html_source, file='test.html'):
    with open(file, 'w') as writter:
        writter.write(str(html_source))