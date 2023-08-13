import requests
from bs4 import BeautifulSoup

from const.const import MAIN_LINK, WORD_TO_DELETE
from web_scrape.scraping import br_removing


def get_last_page():
    response = requests.get(MAIN_LINK)
    if response.status_code == 200:
        soup = br_removing(BeautifulSoup(response.content, 'html.parser'))
        return soup.find_all('a', class_='swchItem')[3].find('span').get_text()


def download_image(url, filename):
    response = requests.get(url)
    with open(filename, 'wb') as file:
        file.write(response.content)


def get_content(html_content):
    content_list = []
    links_list = []
    current_text = ""
    title = html_content.find('h1')
    if title:
        content_list.append(title.text)
    content_div = html_content.find('div', class_='entry')
    if content_div:
        for element in content_div.find_all(['p', 'img', 'iframe'], recursive=True):
            if element.name == 'img':
                if current_text:
                    content_list.append(current_text.strip())
                    current_text = ""
                content_list.append(MAIN_LINK + element['src'])
            elif element.name == 'iframe':
                links_list.append(element['src'])
            elif element.name == 'p' and element.text != '' and WORD_TO_DELETE[0] not in element.text:
                links = element.find_all('a')
                for link in links:
                    links_list.append(link['href'])
                item = element.text
                if len(current_text + "\n\n" + item) > 4096:
                    content_list.append(current_text.strip())
                    current_text = item
                else:
                    current_text += "\n\n" + item
    if current_text:
        content_list.append(current_text.strip())
    for link in links_list:
        content_list.append(link)
    return content_list
