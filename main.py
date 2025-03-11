import time
import random
import asyncio
import schedule
import threading
import os
import logging
from telegram import Bot
from flask import Flask
from config import (
    AMAZON_ACCESS_KEY, AMAZON_SECRET_KEY, AMAZON_PARTNER_TAG,
    TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, AMAZON_CATEGORIES
)
from amazon_api_wrapper import AmazonApiWrapper

# 📂 Nome del file per salvare gli ASIN
ASIN_FILE = "sent_asins.txt"

# 🔹 Carica gli ASIN già inviati da un file locale
def load_sent_asins():
    if os.path.exists(ASIN_FILE):
        with open(ASIN_FILE, "r") as file:
            return set(file.read().splitlines())
    return set()

# 🔹 Salva un nuovo ASIN nel file locale
def save_sent_asin(asin):
    with open(ASIN_FILE, "a") as file:
        file.write(asin + "\n")

# ✅ Inizializza l'API Amazon
amazon_api = AmazonApiWrapper()
sent_asins = load_sent_asins()

# 🔹 Funzione per inviare un'offerta su Telegram
async def send_telegram(offer):
    try:
        bot = Bot(token=TELEGRAM_TOKEN)
        description = offer.get('description', '').strip() or "Nessuna descrizione disponibile."
        text = (
            "\U0001F525 <b>LE MIGLIORI OFFERTE DEL WEB</b>\n\n"
            "\U0001F389 <b>Super Offerta!</b>\n\n"
            "\U0001F517 <a href='https://www.amazon.it/dp/{asin}?tag={tag}'>Apri nell'app Amazon</a>\n"
            "\U0001F517 <a href='https://www.amazon.it/dp/{asin}?tag={tag}'>Apri nel browser</a>\n\n"
            "<b>Amazon</b>\n"
            "<b>{title}</b>\n\n"
            "{description}"
        ).format(
            asin=offer['asin'],
            tag=AMAZON_PARTNER_TAG,
            title=offer['title'],
            description=description
        )
        
        await bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=offer['image'], caption=text, parse_mode="HTML")
        sent_asins.add(offer['asin'])
        save_sent_asin(offer['asin'])
        logging.info(f"✅ Offerta inviata: {offer['title'][:30]}...")
    except Exception as e:
        logging.error(f"❌ Errore invio Telegram: {str(e)}")

# 🔹 Funzione principale per trovare e inviare offerte
def job():
    logging.info("⚡ Avvio ricerca offerte")
    category = random.choice(AMAZON_CATEGORIES)
    offers = amazon_api.get_offers(category)

    if offers:
        random.shuffle(offers)
        for offer in offers:
            if (
                offer['asin'] not in sent_asins and
                offer.get('discount', 0) >= 28 and  # 🔥 Sconto minimo del 28%
                category not in ["Movies", "Music"]  # 🚫 Esclude film e musica
            ):
                asyncio.run(send_telegram(offer))
                break
    else:
        logging.info(f"⏭️ Nessuna offerta trovata nella categoria: {category}")

# 🔹 Pianificazione dell'invio automatico delle offerte
def run_scheduler():
    schedule.every(29).to(55).minutes.do(job)
    while True:
        schedule.run_pending()
        time.sleep(60)

# 🔹 Creazione di un server Flask (utile per Render/UptimeRobot)
app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 Bot attivo e funzionante!"

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.info("🚀 Avvio del bot e del web server...")
    threading.Thread(target=run_scheduler, daemon=True).start()
    
    # 🔹 Avvio immediato della prima offerta
    asyncio.run(job())
    
    app.run(host="0.0.0.0", port=8001)
