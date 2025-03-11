import time
import random
import base64
import asyncio
import schedule
import threading
import os
import json
import requests
import logging
import firebase_admin
from firebase_admin import credentials, firestore
from telegram import Bot
from flask import Flask
from config import (
    AMAZON_ACCESS_KEY, AMAZON_SECRET_KEY, AMAZON_PARTNER_TAG,
    TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, AMAZON_CATEGORIES
)
from amazon_api_wrapper import AmazonApiWrapper

# ✅ Inizializza Firebase Firestore
firebase_credentials_json = os.getenv("FIREBASE_CREDENTIALS")
db = None  # 🔹 Evita l'errore "name 'db' is not defined"

if firebase_credentials_json:
    try:
        # 🔹 Crea un file temporaneo con la chiave Firebase
        temp_cred_path = "/tmp/firebase_credentials.json"
        with open(temp_cred_path, "w") as f:
            json.dump(json.loads(firebase_credentials_json), f)

        # 🔹 Usa il file per inizializzare Firebase
        cred = credentials.Certificate(temp_cred_path)
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        logging.info("✅ Firebase Firestore connesso correttamente!")
    except Exception as e:
        logging.error(f"❌ Errore inizializzazione Firebase: {e}")
else:
    logging.error("❌ Errore: Variabile FIREBASE_CREDENTIALS non trovata!")

# Inizializza l'API Amazon
amazon_api = AmazonApiWrapper()

# 🔹 Funzione per caricare gli ASIN già inviati da Firestore
def load_sent_asins():
    if db is None:
        return set()
    try:
        docs = db.collection("sent_asins").stream()
        return {doc.id for doc in docs}
    except Exception as e:
        logging.error(f"Errore nel caricamento degli ASIN da Firestore: {e}")
        return set()

# 🔹 Funzione per salvare un nuovo ASIN in Firestore
def save_sent_asin(asin):
    if db is None:
        return
    try:
        db.collection("sent_asins").document(asin).set({"timestamp": time.time()})
    except Exception as e:
        logging.error(f"Errore nel salvataggio dell'ASIN su Firestore: {e}")

# Carica gli ASIN già inviati
sent_asins = load_sent_asins()

# 🔹 Funzione per inviare un'offerta su Telegram
async def send_telegram(offer):
    try:
        bot = Bot(token=TELEGRAM_TOKEN)

        print("DEBUG - Offerta ricevuta:", offer)

        description = offer.get('description', '').strip()
        if not description:
            description = "\n".join(offer.get('features', [])) or "Nessuna descrizione disponibile."

        text = (
            "🔥 <b>LE MIGLIORI OFFERTE DEL WEB</b>\n\n"
            "🎉 <b>Super Offerta!</b>\n\n"
            "🔗 <a href='https://www.amazon.it/dp/{asin}?tag={tag}'>Apri nell'app Amazon</a>\n"
            "🔗 <a href='https://www.amazon.it/dp/{asin}?tag={tag}'>Apri nel browser</a>\n\n"
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

        # 🔹 Salva l'ASIN in Firestore
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
            if offer['asin'] not in sent_asins:
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
    job()

    app.run(host="0.0.0.0", port=8001)
