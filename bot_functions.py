# bot_functions.py
import os
import tempfile
import requests
import yt_dlp
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from config import CHANNEL_URL, ACCOUNT_USERNAME, DEVELOPER_USERNAME

# إنشاء مجلد downloads
if not os.path.exists("downloads"):
    os.makedirs("downloads")

# ======== أزرار القوائم ========
def main_menu():
    kb = [
        [InlineKeyboardButton("🎬 تحميل يوتيوب", callback_data="yt")],
        [InlineKeyboardButton("🖼 تحميل صور/ملفات", callback_data="img")],
        [InlineKeyboardButton("📿 أذكار صباح", callback_data="morning")],
        [InlineKeyboardButton("🌙 أذكار مساء", callback_data="evening")],
        [
            InlineKeyboardButton("📢 قناتي", url=CHANNEL_URL),
            InlineKeyboardButton("👤 حسابي", url=f"https://t.me/{ACCOUNT_USERNAME.replace('@','')}")
        ]
    ]
    return InlineKeyboardMarkup(kb)

# ======== تحميل يوتيوب ========
def download_youtube(url):
    ydl_opts = {
        "format": "best[height<=720]/best",
        "outtmpl": "downloads/%(title)s.%(ext)s",
        "noplaylist": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filepath = ydl.prepare_filename(info)
    return filepath, info.get('title', 'video')
