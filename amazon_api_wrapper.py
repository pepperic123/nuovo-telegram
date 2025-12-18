import time
import random
import requests
from bs4 import BeautifulSoup

from paapi5_python_sdk.api.default_api import DefaultApi
from paapi5_python_sdk.search_items_request import SearchItemsRequest
from paapi5_python_sdk.rest import ApiException

from config import (
    AMAZON_ACCESS_KEY, AMAZON_SECRET_KEY,
    AMAZON_PARTNER_TAG, AMAZON_HOST, AMAZON_RESOURCES
)

EXCLUDED_CATEGORIES = ["Movies", "DVD", "Blu-ray", "Music", "CD", "Vinyl"]


class AmazonApiWrapper:
    def __init__(self):
        try:
            self.api = DefaultApi(
                access_key=AMAZON_ACCESS_KEY,
                secret_key=AMAZON_SECRET_KEY,
                host=AMAZON_HOST,
                region="eu-west-1"
            )
            print("✅ API Amazon inizializzata correttamente.")
        except Exception as e:
            print(f"❌ Errore inizializzazione API: {str(e)}")
            self.api = None

    # ==========================
    # METODO PRINCIPALE
    # ==========================
    def get_offers(self, category):
        # 1️⃣ PROVA PA-API
        if self.api:
            try:
                offers = self._get_offers_paapi(category)
                if offers:
                    return offers
            except Exception as e:
                print(f"⚠️ PA-API fallita: {e}")

        # 2️⃣ FALLBACK SCRAPING
        print("🔄 Uso fallback SCRAPING")
        return self._get_offers_scraping(category)

    # ==========================
    # PA-API
    # ==========================
    def _get_offers_paapi(self, category):
        time.sleep(random.uniform(2, 4))

        request = SearchItemsRequest(
            partner_tag=AMAZON_PARTNER_TAG,
            partner_type="Associates",
            keywords=category,
            resources=AMAZON_RESOURCES,
            item_count=10
        )

        response = self.api.search_items(request)
        offers = []

        if response.search_result and response.search_result.items:
            for item in response.search_result.items:

                product_category = (
                    item.item_info.classifications.binding.display_value
                    if item.item_info.classifications and item.item_info.classifications.binding
                    else "Unknown"
                )

                if product_category in EXCLUDED_CATEGORIES:
                    continue

                price_current = None
                price_original = None

                try:
                    listing = item.offers.listings[0]
                    if listing.price and listing.price.amount:
                        price_current = listing.price.amount
                    if listing.saving_basis and listing.saving_basis.amount:
                        price_original = listing.saving_basis.amount
                except Exception:
                    pass

                offer = {
                    "title": item.item_info.title.display_value,
                    "category": product_category,
                    "price_current": f"{price_current}€" if price_current else "N/A",
                    "price_original": f"{price_original}€" if price_original else "N/A",
                    "discount": "N/A",
                    "savings": "N/A",
                    "image": item.images.primary.large.url if item.images else "N/A",
                    "link": item.detail_page_url,
                    "asin": item.asin
                }
                offers.append(offer)

        return offers

    # ==========================
    # SCRAPING
    # ==========================
def _get_offers_scraping(self, keyword):
    offers = []
    try:
        url = f"https://www.amazon.it/s?k={keyword}"
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept-Language": "it-IT,it;q=0.9"
        }

        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        items = soup.select("div[data-asin]")

        for item in items:
            asin = item.get("data-asin")
            if not asin:
                continue

            title_el = item.select_one("h2 span")
            image_el = item.select_one("img")
            price_el = item.select_one("span.a-price-whole, span.a-offscreen")  # FIX 1

            if not title_el or not image_el:
                continue  # FIX 2: non scartare se manca il prezzo

            price_text = price_el.text.strip() + "€" if price_el else "Offerta su Amazon"  # FIX 2

            offer = {
                "title": title_el.text.strip(),
                "category": keyword,
                "price_current": price_text,
                "price_original": "N/A",
                "discount": "N/A",
                "savings": "N/A",
                "image": image_el.get("src"),
                "link": f"https://www.amazon.it/dp/{asin}",
                "asin": asin
            }

            offers.append(offer)

        return offers

    except Exception as e:
        print(f"❌ Errore scraping: {e}")
        return []