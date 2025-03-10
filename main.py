import time
import random
import asyncio
import schedule
import threading
from telegram import Bot
from flask import Flask
from config import (
    AMAZON_ACCESS_KEY, AMAZON_SECRET_KEY, AMAZON_PARTNER_TAG,
    TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, AMAZON_CATEGORIES
)
from amazon_api_wrapper import AmazonApiWrapper
import logging

# Inizializza l'API Amazon
amazon_api = AmazonApiWrapper()

# Memorizza gli ASIN inviati per evitare duplicati
sent_asins = set()

# Funzione per inviare un'offerta su Telegram
async def send_telegram(offer):
    try:
        bot = Bot(token=TELEGRAM_TOKEN)
        text = (
            f"🔥 *Offerta imperdibile su {offer['title']}!* 🔥\n\n"
            f"💰 *Prezzo:* {offer['price']}\n\n"
            f"⏳ *Ultimi pezzi disponibili!*\n\n"
            f"🔗 [Compra ora!](https://www.amazon.it/dp/{offer['asin']}?tag={AMAZON_PARTNER_TAG})"
        )
        await bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=offer['image'], caption=text, parse_mode="Markdown")
        sent_asins.add(offer['asin'])  # Aggiungi l'ASIN solo se l'invio è stato completato correttamente
        logging.info(f"✅ Offerta inviata: {offer['title'][:30]}...")
    except Exception as e:
        logging.error(f"❌ Errore invio Telegram: {str(e)}")

# Funzione principale per trovare e inviare offerte
def job():
    logging.info("⚡ Avvio ricerca offerte")
    category = random.choice(AMAZON_CATEGORIES)
    offers = amazon_api.get_offers(category)

    if offers:
        random.shuffle(offers)
        for offer in offers:
            if offer['asin'] not in sent_asins:
                asyncio.run(send_telegram(offer))
                break
    else:
        logging.info(f"⏭️ Nessuna offerta trovata nella categoria: {category}")

# Pianificazione dell'invio automatico delle offerte
def run_scheduler():
    schedule.every(29).to(55).minutes.do(job)
    while True:
        schedule.run_pending()
        time.sleep(60)

# Creazione di un server Flask (utile per Render/UptimeRobot)
app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 Bot attivo e funzionante!"

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.info("🚀 Avvio del bot e del web server...")
    threading.Thread(target=run_scheduler, daemon=True).start()

    # Avvio immediato della prima offerta
    job()

    app.run(host="0.0.0.0", port=8001)
