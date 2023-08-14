import re

import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update

from const.const import MAIN_LINK, HTTP_TAG, HTTPS_TAG, WORD_TO_DELETE
from web_scrape.one_article import get_article
from web_scrape.scraping import get_links
from web_scrape.utils import get_last_page, download_image


def key_b():
    keyboard = [[InlineKeyboardButton("Delete", callback_data="delete_messages")]]
    return InlineKeyboardMarkup(keyboard)


async def mess_hdl(update: Update, ctx):
    text = update.message.text.strip()
    message_id = update.message.message_id
    last_page = get_last_page()
    if text.isdigit():
        if 0 < int(text) <= int(last_page):
            links = get_links(text)
            for link in links:
                link = MAIN_LINK + link
                await update.message.reply_text(link)
            text = f"Go to\nPage {text}"
    else:
        page = requests.get(text)
        if page.status_code == 200:
            article = get_article(text)
            text = f"Go to\n{article[0]}"
            for part in article:
                if part.startswith(HTTP_TAG) \
                        or part.startswith(HTTPS_TAG):
                    filename = 'image.jpg'
                    download_image(part, filename)
                    with open(filename, 'rb') as file:
                        await update.message.reply_photo(photo=file)
                else:
                    if WORD_TO_DELETE[1] in part:
                        part = re.sub(WORD_TO_DELETE[1], '', part)
                    await update.message.reply_text(part)
        else:
            await update.message.reply_text("I don't understand.")
    await update.message.reply_text(text=text, reply_markup=key_b(), reply_to_message_id=message_id)
