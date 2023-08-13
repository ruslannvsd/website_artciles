import requests
from bs4 import BeautifulSoup

from const.const import TO_BE_REPLACED, TO_BE_INSERTED, TITLE_ID, MAIN_LINK


def br_removing(br_soup):
    for br in br_soup.find_all(TO_BE_REPLACED):
        br.replace_with(TO_BE_INSERTED)
    return br_soup


def get_links(page):
    response = requests.get(MAIN_LINK + "/?page" + page)
    links = []
    if response.status_code == 200:
        soup = br_removing(BeautifulSoup(response.content, 'html.parser'))
        message_sections = soup.find_all('div', id=TITLE_ID)
        if message_sections:
            for section in message_sections:
                a_tag = section.find('a')
                if a_tag:
                    link = a_tag['href']
                    links.append(link)
    return links
