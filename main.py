import time
import random
import base64
import asyncio
import schedule
import threading
import os
import requests
import logging
from telegram import Bot
from flask import Flask
from config import (
    AMAZON_ACCESS_KEY, AMAZON_SECRET_KEY, AMAZON_PARTNER_TAG,
    TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, AMAZON_CATEGORIES
)
from amazon_api_wrapper import AmazonApiWrapper

# Configurazione GitHub
GITHUB_REPO = os.getenv("GITHUB_REPO")  # Formato: "username/repository"
GITHUB_FILE_PATH = os.getenv("GITHUB_FILE_PATH")  # Es. "data/sent_asins.txt"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# Inizializza l'API Amazon
amazon_api = AmazonApiWrapper()

# Funzione per caricare gli ASIN già inviati da GitHub
def load_sent_asins():
    try:
        url = f"https://raw.githubusercontent.com/{GITHUB_REPO}/main/{GITHUB_FILE_PATH}"
        response = requests.get(url)
        if response.status_code == 200:
            return set(response.text.splitlines())
        logging.warning("⚠️ Il file su GitHub non è stato trovato o è vuoto.")
    except Exception as e:
        logging.error(f"Errore nel caricamento degli ASIN da GitHub: {e}")
    return set()

# Funzione per salvare gli ASIN localmente
def save_sent_asins():
    try:
        with open("sent_asins.txt", "w") as file:
            file.write("\n".join(sent_asins))
    except Exception as e:
        logging.error(f"Errore nel salvataggio degli ASIN: {e}")

# Funzione per aggiornare il file su GitHub
def update_github():
    try:
        url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{GITHUB_FILE_PATH}"
        headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        logging.info(f"🔍 Controllo URL GitHub: {url}")
        response = requests.get(url, headers=headers)
        logging.info(f"🔍 Risposta GET GitHub: {response.status_code} - {response.text}")
        
        sha = response.json().get("sha", "") if response.status_code == 200 else None

        with open("sent_asins.txt", "r") as file:
            content = file.read()
            encoded_content = base64.b64encode(content.encode()).decode()

        data = {
            "message": "Aggiornamento sent_asins.txt",
            "content": encoded_content,
            "sha": sha,
        }

        response = requests.put(url, json=data, headers=headers)
        logging.info(f"🔍 Risposta PUT GitHub: {response.status_code} - {response.text}")
        
        if response.status_code in [200, 201]:
            logging.info("✅ ASIN aggiornati con successo su GitHub!")
        else:
            logging.error(f"❌ Errore aggiornamento GitHub: {response.json()}")
    except Exception as e:
        logging.error(f"❌ Errore update GitHub: {e}")

# Carica gli ASIN già inviati
sent_asins = load_sent_asins()

# Funzione per inviare un'offerta su Telegram
async def send_telegram(offer):
    try:
        bot = Bot(token=TELEGRAM_TOKEN)
        description = offer.get('description', '').strip() or "Nessuna descrizione disponibile."
        text = (
            "🔥 <b>LE MIGLIORI OFFERTE DEL WEB</b>\n\n"
            "🎉 <b>Super Offerta!</b>\n\n"
            "🔗 <a href='https://www.amazon.it/dp/{asin}?tag={tag}'>Apri nell'app Amazon</a>\n"
            "🔗 <a href='https://www.amazon.it/dp/{asin}?tag={tag}'>Apri nel browser</a>\n\n"
            "<b>Amazon</b>\n"
            "<b>{title}</b>\n\n"
            "{description}"
        ).format(asin=offer['asin'], tag=AMAZON_PARTNER_TAG, title=offer['title'], description=description)

        await bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=offer['image'], caption=text, parse_mode="HTML")
        sent_asins.add(offer['asin'])
        save_sent_asins()
        update_github()
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

# Pianificazione dell'invio automatico
def run_scheduler():
    schedule.every(29).to(55).minutes.do(job)
    while True:
        schedule.run_pending()
        time.sleep(60)

# Creazione di un server Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 Bot attivo e funzionante!"

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.info("🚀 Avvio del bot e del web server...")
    threading.Thread(target=run_scheduler, daemon=True).start()
    job()
    app.run(host="0.0.0.0", port=8001)
