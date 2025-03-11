from paapi5_python_sdk.api.default_api import DefaultApi
from paapi5_python_sdk.search_items_request import SearchItemsRequest
from paapi5_python_sdk.rest import ApiException
from config import (
    AMAZON_ACCESS_KEY, AMAZON_SECRET_KEY,
    AMAZON_PARTNER_TAG, AMAZON_HOST, AMAZON_RESOURCES
)

# Categorie da escludere
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

    def get_offers(self, category):
        if not self.api:
            return []

        try:
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
                    # Controlla la categoria del prodotto
                    product_category = item.item_info.classifications.binding.display_value if item.item_info.classifications and item.item_info.classifications.binding else "Unknown"
                    
                    # Escludi film e musica
                    if product_category in EXCLUDED_CATEGORIES:
                        continue  

                    # Ottieni il prezzo attuale in modo sicuro
                    price_current = None
                    try:
                        if item.offers and item.offers.listings:
                            first_listing = item.offers.listings[0]
                            if hasattr(first_listing, "price") and hasattr(first_listing.price, "amount"):
                                price_current = first_listing.price.amount
                    except Exception:
                        pass  # Se non trova il prezzo, continua

                    # Ottieni il prezzo originale in modo sicuro
                    price_original = None
                    try:
                        if item.offers and item.offers.listings:
                            first_listing = item.offers.listings[0]
                            if hasattr(first_listing, "saving_basis") and hasattr(first_listing.saving_basis, "amount"):
                                price_original = first_listing.saving_basis.amount
                    except Exception:
                        pass  # Se non trova il prezzo originale, continua

                    # Calcola sconto e risparmio
                    discount = 0
                    savings = 0
                    if price_original and price_current:
                        discount = round((1 - (price_current / price_original)) * 100) if price_original > price_current else 0
                        savings = round(price_original - price_current, 2) if price_original > price_current else 0

                    offer = {
                        "title": item.item_info.title.display_value,
                        "category": product_category,
                        "price_current": f"{price_current}€" if price_current else "N/A",
                        "price_original": f"{price_original}€" if price_original else "N/A",
                        "discount": f"{discount}%" if discount > 0 else "N/A",
                        "savings": f"{savings}€" if savings > 0 else "N/A",
                        "image": item.images.primary.large.url if item.images else "N/A",
                        "link": item.detail_page_url,
                        "asin": item.asin
                    }
                    offers.append(offer)
            return offers

        except ApiException as e:
            print(f"❌ Errore PAAPI 5.0: {e.body}")
            return []