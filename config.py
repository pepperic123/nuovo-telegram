# Credenziali Amazon
AMAZON_ACCESS_KEY = "AKPAV0YTNY1740423739"
AMAZON_SECRET_KEY = "g0N1qt9tB2AUB+chkTDjakR3nafgqmkGkfr77/2h"
AMAZON_PARTNER_TAG = "new1707-21"
AMAZON_HOST = "webservices.amazon.it"  # Endpoint per l'Italia
AMAZON_RESOURCES = [
    "ItemInfo.Title",
    "Offers.Listings.Price",
    "Images.Primary.Large"
]

AMAZON_COUNTRY = "IT"  # Codice paese (es: "IT" per Italia)

# Credenziali Telegram
TELEGRAM_TOKEN = "7193847897:AAE7ny5YWjmPyrxIcgeCjvsy8koYM8jQ7pw"  # Token del bot Telegram
TELEGRAM_CHAT_ID = "-1001434969904"  # ID del chat o canale Telegram
FIREBASE_CREDENTIALS = """{
  "type": "service_account",
  "project_id": "telegram-532f0",
  "private_key_id": "f84566ed728edceb42d49d01c3a727e3fcc9d571",
  "private_key": "-----BEGIN PRIVATE KEY-----\\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCTe0Xaw3vbmj6l\\nPoBx4+6lb/K8mj3c4OKLHLgxrXZICPVp4CvLsSTvjuikXWkUKaIT0rrR0igaFxup\\nr27b0+oONKInxKCZ+g2VkYvvBpOivyulbBXfbES5P5pKvFERNqVI5FAWvqck2FcX\\n8I+xVpBzBNf0MrFhiBD7Hoeko3IUJiEyE6bubTwAF0y/Oqd6B7+/FVf48GyBdKwJ\\ntY2pscDmZKBzC6FjRj5YBkBsygZimfsEnuuwWJ29TJbVGl2hPZddDNtoNFKmoGX1\\na9tdQFi+k/Ty5tF0H8wBNppaDKmJUaR8rqoLbDhFDvYcAEOCHko32x7+XHgqF+w2\\nFZhQkzR1AgMBAAECggEABJXhnyKoLYochoYXTPM5o/qDa+pzyp6nYeHmYY0Iz3E6\\niCyIersq8H6GAeOcSnHc8IwtyNZQRDdnDHNARCTQ8y4fGJNxgY1tHLMQzGwXl7N6\\nnO3BDwL5GWAT4Qen5vFxrtQtH/fqOdK21S9imFtI/yUtvbxRwubjIvEDu1JlpUta\\nF2eaXA67e8Iv+TEKEwEOn6PcNY1lXYdkApIDndGgwjxfdensK8f9KHp/zS9C7fgc\\ngq1hu6McLlNiwNft8/fP4G52gIt/LyC+UahS23H1CoGgMi6PxIFKxuZLt1RI87F/\\niCyk/QpBL2U8tH6VG5aqIqoD0yrHFWRyJ6J6v9BtgQKBgQDQY2BdnRDNj7xJJOpY\\n+7YA2HrlDz9Fa+2kBlc9jxmqRalAxkcM08+XrHYiTG7i6jNWA09WizvVLMvn+s3p\\ndG4xcv2jeJlOzmlIcido5jsIJ+ryYBWTEIJM8uhfilU2xZthcNkwRAXPQXflmLUN\\n4Ela+3iOWgqSPmDYwzpxowymVQKBgQC1LXd47w/aNoWDEtY9pyz7U60v8KbG+82c\\nmd/xkH3iTCnthXroBL5aj6Gr1toulLSPocz/WFlR6UvoJ6UtSdxxEKuOqgveSQsr\\nyN8fHWzcHAqfg7Af5MJlshTHkYcV9zUKQkuCXJSoNb+sapdvfGvluuvdASEpnba2\\nzfHXs3M1oQKBgG0e/MFIlBnwYHo02HqMJHxA3+m+mDU0FRbFMz3LB3eATubabS4s\\nZBJafunq+E3esc8ioJMDCevRL11kmhrbmzBNtL+7URxRPhRvom9t0A+vR3pwEhwW\\nkwTUVhZhi8nIpFrcCv8ZP6mN8MjLtFN11TPNZw2z3MFD5NbdNGd5KBCZAoGAKz1b\\nqyAa/3BNsveW7AXvBVh2F9/uXcUQ0FQlD0j10kFtLEPUDnW7XG+1HQbc8YsKANGT\\n1EkooBT2ycRUdpePJejdmOHajUWPhfad0ZY7OdjzbBiIu0PkZVL4BJ0lyUdDgFxM\\nGyOvUunpAeQ6mh/uvFg9HHS9jmoWhlBmbJ1mXKECgYAhx7TwHcI0WyD4BXeEqhH5\\nfkpipkoNVR17cErvMLfZkurB0GTd4mQtRUZKUAV40vg6KU9w2ndyqxeQ4GfMnvF5\\nb+wOcMOjI4P5mPMMhBHVN+MCVQ/M+Afwv6xZzZlSuzpANlWu+v96zfGFRdAHPDlY\\ncPRqI8mlQYyzdJbISiIUXw==\\n-----END PRIVATE KEY-----\\n",
  "client_email": "firebase-adminsdk-fbsvc@telegram-532f0.iam.gserviceaccount.com",
  "client_id": "102583741195441251777",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fbsvc%40telegram-532f0.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}"""

# Credenziali GitHub (per memorizzare gli ASIN inviati)
GITHUB_REPO = "pepperic123/nuovo-telegram"
GITHUB_UPDATE_URL = "https://api.github.com/repos/pepperic123/nuovo-telegram/contents/sent_asins.txt"  # URL API per aggiornare il file
GITHUB_TOKEN = "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"
# Categorie Amazon per la ricerca
AMAZON_CATEGORIES = [
    "Appliances",        # Elettrodomestici
    "ArtsAndCrafts",     # Arti e Mestieri
    "Automotive",        # Automotive
    "Baby",              # Bambini
    "Beauty",            # Bellezza
    "Books",             # Libri
    "Clothing",          # Abbigliamento
    "Electronics",       # Elettronica
    "Grocery",           # Alimentari
    "Health",            # Salute
    "Home",              # Casa
    "Industrial",        # Industria
    "Jewelry",           # Gioielleria
    "KindleStore",       # Kindle Store
    "Kitchen",           # Cucina
    "Luggage",           # Valigie
    "Music",             # Musica
    "OfficeProducts",    # Prodotti per ufficio
    "PersonalCare",      # Cura personale
    "Shoes",             # Scarpe
    "Software",          # Software
    "Sports",            # Sport
    "Tools",             # Attrezzi
    "Toys",              # Giochi
    "VideoGames",        # Videogiochi
    "Watches",           # Orologi
    "Women",             # Donne
    ]
