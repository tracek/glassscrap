import time
from collections import namedtuple
from random import randint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException


Credentials = namedtuple('Credentials', ['username', 'password'])

class WebParsingException(Exception):
    def __init__(self, msg, original_exception):
        super(WebParsingException, self).__init__(msg + (": %s" % original_exception))
        self.original_exception = original_exception

def get_credentials(path):
    with open(path, "r") as f:
        lines = f.read().splitlines()
        account = Credentials(username=lines[0], password=lines[1])
    return account


class WebCrawler(object):

    def __init__(self):
        self.driver = webdriver.Chrome("/usr/local/bin/chromedriver")
        self.login()
        self.pages_visited = 0

    def login(self):
        self.driver.get("http://www.glassdoor.com/profile/login_input.htm")
        credentials = get_credentials("account.txt")
        try:
            user_field = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))
            pw_field = self.driver.find_element_by_class_name("signin-password")
            login_button = self.driver.find_element_by_id("signInBtn")
            user_field.send_keys(credentials.username)
            user_field.send_keys(Keys.TAB)
            time.sleep(1)
            pw_field.send_keys(credentials.password)
            time.sleep(1)
            login_button.click()
        except TimeoutException:
            print("TimeoutException! Username/password field or login button not found on glassdoor.com")

    def get_total_pages(self, url):
        reviews_per_page = 10
        self.driver.get(url)
        total_rev_present = EC.presence_of_element_located((By.CSS_SELECTOR, '.eiCell.cell.reviews.active'))
        total_rev_element = WebDriverWait(self.driver, 10).until(total_rev_present)
        total_rev_str = total_rev_element.find_element_by_css_selector('.num.h2').text
        total_rev = int(total_rev_str)
        total_pages = total_rev // reviews_per_page
        return total_pages

    def __next__(self):
        xpath = '//*[@id="FooterPageNav"]/div/ul/li[7]/a'
        try:
            element = self.driver.find_element_by_xpath(xpath)
            next_page_address = element.get_property('href')
            self.driver.get(next_page_address)
            self.pages_visited += 1

            some_int = randint(5, 10)
            self.driver.execute_script("window.scrollTo(0, {})".format(100 * some_int))
            time.sleep(some_int)
            html = self.driver.page_source
            yield html

        except NoSuchElementException as ex:
            if self.pages_visited > 0:
                raise StopIteration
            else:
                raise WebParsingException('Unable to find the NEXT button at all', ex)

    def __iter__(self):
        return self


    def get_next_page(self):
        xpath = '//*[@id="FooterPageNav"]/div/ul/li[7]/a'
        try:
            element = self.driver.find_element_by_xpath(xpath)
            next_page_address = element.get_property('href')
            self.driver.get(next_page_address)
            self.pages_visited += 1
            time.sleep(1)
        except NoSuchElementException:
            if self.pages_visited > 0:
                return None
            else:
                raise WebParsingException('Unable to find the NEXT button at all')


if __name__ == '__main__':
    crawler = WebCrawler()
