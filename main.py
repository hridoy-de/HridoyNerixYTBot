from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler,
    MessageHandler, filters, ContextTypes, CallbackQueryHandler
)
from config import BOT_TOKEN, ADMIN_ID

# Simple in-memory storage (later DB can be added)
users = {}

def get_user(uid):
    if uid not in users:
        users[uid] = {
            "ref": 0,
            "video_ok": 0,
            "balance": 0,
            "withdraw_unlocked": False
        }
    return users[uid]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    get_user(uid)
    text = (
        "👋 Welcome to Hridoy NerixYT Bot\n\n"
        "🔒 Withdraw Locked\n"
        "✅ শর্ত:\n"
        "• 18 জন Refer\n"
        "• 2টা YouTube ভিডিও (SS + Admin Approve)\n\n"
        "মেনু:\n"
        "/balance — ব্যালেন্স দেখুন\n"
        "/upload — ভিডিও Screenshot পাঠান\n"
    )
    await update.message.reply_text(text)

async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    u = get_user(update.effective_user.id)
    status = "🔓 UNLOCKED" if u["withdraw_unlocked"] else "🔒 LOCKED"
    await update.message.reply_text(
        f"💰 Balance: {u['balance']}৳\nWithdraw: {status}\n"
        f"Refer: {u['ref']}/18 | Video Approved: {u['video_ok']}/2"
    )

async def upload(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📸 ভিডিওর START ও END Screenshot পাঠাও (একটা করে পাঠালেও হবে)।\n"
        "Admin যাচাই করে Approve করবে।"
    )

async def photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.photo:
        return
    uid = update.effective_user.id
    caption = f"📸 Video Screenshot\nUser ID: {uid}\nApprove: /approve {uid}"
    await context.bot.send_photo(
        chat_id=ADMIN_ID,
        photo=update.message.photo[-1].file_id,
        caption=caption
    )
    await update.message.reply_text("✅ Screenshot পাঠানো হয়েছে, Admin যাচাই করবে।")

async def approve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    if not context.args:
        await update.message.reply_text("ব্যবহার: /approve USERID")
        return
    uid = int(context.args[0])
    u = get_user(uid)
    u["video_ok"] += 1
    if u["video_ok"] >= 2 and u["ref"] >= 18:
        u["withdraw_unlocked"] = True
    await update.message.reply_text("✅ Approved!")

async def add_ref(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    if not context.args:
        return
    uid = int(context.args[0])
    u = get_user(uid)
    u["ref"] += 1
    if u["video_ok"] >= 2 and u["ref"] >= 18:
        u["withdraw_unlocked"] = True
    await update.message.reply_text("➕ Refer added")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("balance", balance))
    app.add_handler(CommandHandler("upload", upload))
    app.add_handler(CommandHandler("approve", approve))
    app.add_handler(CommandHandler("addref", add_ref))
    app.add_handler(MessageHandler(filters.PHOTO, photo_handler))

    app.run_polling()

if __name__ == "__main__":
    main()
from flask import Flask
import threading
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running"

def run():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

threading.Thread(target=run).start()
