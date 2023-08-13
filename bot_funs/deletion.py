from telegram import Update
from telegram.ext import ContextTypes


async def delete_messages(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    last_mess = update.callback_query.message
    first_mess_id = last_mess.reply_to_message.message_id
    last_mess_id = last_mess.message_id
    chat_id = update.effective_chat.id
    for i in range(first_mess_id, last_mess_id+1):
        await ctx.bot.delete_message(chat_id=chat_id, message_id=i)
