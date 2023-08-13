from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

from web_scrape.scraping import br_removing
from web_scrape.utils import get_content


def get_article(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    page_source = driver.page_source
    driver.quit()
    text = br_removing(BeautifulSoup(page_source, 'html.parser'))
    content = get_content(text)
    return content
