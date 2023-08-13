from telegram import Update
from telegram.ext import Application, ContextTypes, CommandHandler, MessageHandler, filters, CallbackQueryHandler

from bot_funs.deletion import delete_messages
from bot_funs.message_handling import mess_hdl
from const.const import TOKEN


async def start_command(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    await update.message.reply_text(f'Welcome, {user.username}!')


if __name__ == "__main__":
    print("Starting the bot ...")
    app = Application.builder().token(TOKEN).connect_timeout(7).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(MessageHandler(filters.TEXT, mess_hdl))
    app.add_handler(CallbackQueryHandler(delete_messages))
    print("Polling ...")
    app.run_polling(3)
