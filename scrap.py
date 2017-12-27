import time
from collections import namedtuple
from random import randint
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys


Credentials = namedtuple('Credentials', ['username', 'password'])


def init_driver(driver_path):
    driver = webdriver.Chrome(driver_path)
    driver.wait = WebDriverWait(driver, 10)
    return driver


def get_credentials(path):
    with open(path, "r") as f:
        lines = f.readlines()
        account = Credentials(username=lines[0], password=lines[1])
    return account


def login(driver, credentials):
    driver.get("http://www.glassdoor.com/profile/login_input.htm")
    try:
        user_field = driver.wait.until(EC.presence_of_element_located(
            (By.NAME, "username")))
        pw_field = driver.find_element_by_class_name("signin-password")
        login_button = driver.find_element_by_id("signInBtn")
        user_field.send_keys(credentials.username)
        user_field.send_keys(Keys.TAB)
        time.sleep(1)
        pw_field.send_keys(credentials.password)
        time.sleep(1)
        login_button.click()
    except TimeoutException:
        print("TimeoutException! Username/password field or login button not found on glassdoor.com")


def get_total_pages(driver, url):
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    total_rev_str = soup.find('a', {'class': 'eiCell cell reviews active'}).find('span', {'class': 'num h2'}).text
    total_rev = int(total_rev_str)
    total_pages = total_rev // reviews_per_page
    return total_pages


def parse_reviews_HTML(reviews):
    data = []
    for review in reviews:
        date = review.find("time", { "class" : "date" }).getText().strip()
        data.append(date)
    return data


if __name__ == '__main__':
    chromium_path = "/usr/local/bin/chromedriver"
    reviews_per_page = 10
    companyName = "sandvik"
    companyURL = "https://www.glassdoor.com/Reviews/Sandvik-Reviews-E10375.htm"

    driver = init_driver(chromium_path)
    credentials = get_credentials("account.txt")
    login(driver=driver, credentials=credentials)

    total_pages = get_total_pages(driver=driver, url=companyURL)

    d = []

    for page_no in range(1, total_pages):
        print('Processing page: {}'.format(page_no))
        currentURL = '{}_P{}.htm'.format(companyURL[:companyURL.rfind('.')], page_no)
        driver.get(currentURL)
        some_int = randint(5, 10)
        driver.execute_script("window.scrollTo(0, {})".format(100 * some_int))
        time.sleep(some_int)
        HTML = driver.page_source
        soup = BeautifulSoup(HTML, "html.parser")
        reviews = soup.find_all("li", {"class": ["empReview", "padVert"]})
        dates = parse_reviews_HTML(reviews)
        d.extend(dates)
