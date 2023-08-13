import re

import requests
from telegram import Update
from telegram.ext import Application, ContextTypes, CommandHandler, MessageHandler, filters

from const.const import TOKEN, MAIN_LINK, HTTP_TAG, HTTPS_TAG, TRIANGLE, WORD_TO_DELETE
from web_scrape.scraping import get_links
from web_scrape.one_article import get_article
from web_scrape.utils import get_last_page, download_image


mess_dict = {}
job_queue = None


async def message_deleting(ctx: ContextTypes.DEFAULT_TYPE):
    global mess_dict
    for user_id in mess_dict.keys():
        for mess in mess_dict.get(user_id, []):
            await ctx.bot.delete_message(chat_id=user_id, message_id=mess)
    mess_dict = {}


def deletion_job():
    if job_queue is not None:
        print("Job started.")
        job_queue.run_repeating(message_deleting, interval=300, first=300)


async def mess_hdl(update: Update, ctx):
    text = update.message.text.strip()
    user_id = update.message.from_user.id
    message_id = update.message.message_id
    if user_id not in mess_dict:
        mess_dict[user_id] = []
    last_page = get_last_page()
    if text.isdigit():
        mess_dict[user_id].append(message_id)
        if 0 < int(text) <= int(last_page):
            messages = get_links(text)
            for msg in messages:
                link = MAIN_LINK + msg['link']
                mess = await update.message.reply_text(link)
                mess_dict[user_id].append(mess.message_id)
        mess = await update.message.reply_text(text=TRIANGLE, reply_to_message_id=message_id)
        mess_dict[user_id].append(mess.message_id)  # for deleting
    else:
        page = requests.get(text)
        if page.status_code == 200:
            article = get_article(text)
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
            await update.message.reply_text(text=TRIANGLE, reply_to_message_id=message_id)
        else:
            await update.message.reply_text("I don't understand.")
    deletion_job()


async def start_command(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    await update.message.reply_text(f'Welcome, {user.username}!')


if __name__ == "__main__":
    print("Starting the bot ...")
    app = Application.builder().token(TOKEN).connect_timeout(7).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(MessageHandler(filters.TEXT, mess_hdl))
    job_queue = app.job_queue
    print("Polling ...")
    app.run_polling(3)
