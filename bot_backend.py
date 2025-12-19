import uuid
from flask import Flask, redirect, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import threading

# 🔴 BOT TOKEN YAHAN DALO
BOT_TOKEN = "PASTE_YOUR_BOT_TOKEN"

app = Flask(__name__)

# Memory storage (simple)
VIDEOS = {}

# ================= BACKEND =================
@app.route("/stream/<vid>")
def stream(vid):
    q = request.args.get("q", "720")
    data = VIDEOS.get(vid)

    if not data:
        return "Invalid link", 404

    return redirect(data.get(q, data["720"]), code=302)

# ================= TELEGRAM BOT =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎬 3 Video Link Bot\n\n"
        "Use command:\n"
        "/add <480p_link> <720p_link> <1080p_link>"
    )

async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        l480, l720, l1080 = context.args
        vid = uuid.uuid4().hex[:8]

        VIDEOS[vid] = {
            "480": l480,
            "720": l720,
            "1080": l1080
        }

        base = "https://YOUR_RENDER_URL.onrender.com"

        msg = (
            "✅ Single Link Created\n\n"
            f"▶ 720p (default):\n{base}/stream/{vid}\n\n"
            f"▶ 480p:\n{base}/stream/{vid}?q=480\n"
            f"▶ 1080p:\n{base}/stream/{vid}?q=1080\n"
        )

        await update.message.reply_text(msg)

    except:
        await update.message.reply_text(
            "❌ Format galat hai\n\n"
            "Use:\n"
            "/add link480 link720 link1080"
        )

# ================= RUN BOTH =================
def run_flask():
    app.run(host="0.0.0.0", port=8000)

def run_bot():
    app_tg = ApplicationBuilder().token(BOT_TOKEN).build()
    app_tg.add_handler(CommandHandler("start", start))
    app_tg.add_handler(CommandHandler("add", add))
    app_tg.run_polling()

threading.Thread(target=run_flask).start()
run_bot()
