# webscrape/tests/test_crawler.py
import pytest
from selenium.webdriver.common.by import By
from webscrape.crawler import Crawler

@pytest.fixture(scope="module")
def crawler():
    crawler = Crawler()
    yield crawler
    crawler.quit()

def test_fetch(crawler):
    url = 'https://www.muji.us/collections/'
    html = crawler.fetch(url)
    assert '<title>Collections - MUJI USA</title>' in html

# def test_parse(crawler):
#     crawler.driver.get('http://example.com')
#     title = crawler.driver.find_element(By.TAG_NAME, 'title').get_attribute('innerText')
#     assert title == 'Example Domain'
