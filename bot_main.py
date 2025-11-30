# bot_main.py
import logging
import tempfile
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from config import TOKEN, CHANNEL_URL, ACCOUNT_USERNAME, DEVELOPER_USERNAME
from bot_functions import main_menu, download_youtube
import os

# ======== Logging ========
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ======== أوامر البداية ========
def start_cmd(update, context):
    user = update.effective_user
    txt = (
        f"🎉 مرحباً {user.first_name}!\n\n"
        "أنا بوت التحميل — أرسل رابط يوتيوب أو رابط صورة/ملف وسأقوم بتحميله لك.\n\n"
        f"القناة: {CHANNEL_URL}\nالحساب: {ACCOUNT_USERNAME}\nالمطور: {DEVELOPER_USERNAME}\n\n"
        "اختر من الأزرار أدناه أو أرسل الرابط مباشرة 👇"
    )
    update.message.reply_text(txt, reply_markup=main_menu())

# ======== التعامل مع الضغط على الأزرار ========
def callback_handler(update, context):
    query = update.callback_query
    query.answer()
    data = query.data

    if data == "yt":
        query.edit_message_text("🎬 أرسل رابط يوتيوب الآن، سأقوم بتحميله لك.", reply_markup=main_menu())
    elif data == "img":
        query.edit_message_text("🖼 أرسل رابط صورة أو ملف الآن، سأقوم بتحميله لك.", reply_markup=main_menu())
    elif data == "morning":
        text = "🌞 أذكار الصباح:\n" \
               "سبحان الله، الحمد لله، لا إله إلا الله، الله أكبر ... (أذكار طويلة جدًا هنا)"
        query.edit_message_text(text, reply_markup=main_menu())
    elif data == "evening":
        text = "🌙 أذكار المساء:\n" \
               "أعوذ بالله من الشيطان الرجيم، بسم الله ... (أذكار طويلة جدًا هنا)"
        query.edit_message_text(text, reply_markup=main_menu())
    else:
        query.edit_message_text("تم.", reply_markup=main_menu())

# ======== معالجة الرسائل ========
def handle_message(update, context):
    msg = update.message
    text = msg.text or ""
    signature = f"\n\n🔗 {CHANNEL_URL} | 👨‍💻 {DEVELOPER_USERNAME}"

    if not text.startswith(("http://", "https://")):
        msg.reply_text("📨 أرسل رابط لتحميله أو اختر من القائمة:", reply_markup=main_menu())
        return

    msg.reply_text(f"🔍 جاري معالجة الرابط...{signature}")

    # يوتيوب
    if "youtube.com" in text or "youtu.be" in text:
        try:
            filepath, title = download_youtube(text)
            with open(filepath, "rb") as f:
                msg.reply_video(video=f, caption=f"🎬 {title}{signature}")
            os.remove(filepath)
        except Exception as e:
            msg.reply_text(f"❌ خطأ في تحميل اليوتيوب: {e}{signature}")
        return

    # صور وملفات
    try:
        r = requests.get(text, stream=True, timeout=30)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".bin") as tmp:
            for chunk in r.iter_content(8192):
                if chunk:
                    tmp.write(chunk)
            tmp_path = tmp.name
        content_type = r.headers.get("content-type", "").lower()
        if "image" in content_type:
            with open(tmp_path, "rb") as f:
                msg.reply_photo(photo=f, caption=f"✅ تم تحميل الصورة{signature}")
        else:
            with open(tmp_path, "rb") as f:
                msg.reply_document(document=f, caption=f"✅ تم تحميل الملف{signature}")
        os.unlink(tmp_path)
    except Exception as e:
        msg.reply_text(f"❌ حدث خطأ: {e}{signature}")

# ======== Main ========
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start_cmd))
    dp.add_handler(CallbackQueryHandler(callback_handler))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    print("🚀 البوت جاهز على Render")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
