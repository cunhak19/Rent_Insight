import os
import time
import json
import requests
from src.data.olx_api.auth import OLXAuth

# Diretório onde serão salvos os JSONs brutos
data_dir = os.path.abspath(os.path.join(__file__, "../../../data/raw/olx"))
os.makedirs(data_dir, exist_ok=True)


class OLXClient:
    """
    Cliente para coletar anúncios de aluguel via OLX Open API.
    """

    BASE_URL = "https://www.olx.pt/api/open"

    def __init__(self, auth: OLXAuth, per_page: int = 50, location_id: str = "100001"):
        self.auth = auth
        self.per_page = per_page
        self.location_id = location_id  # ID fixo para Lisboa (exemplo: "100001")

    def fetch_rent_adverts(self):
        all_ads = []
        page = 1

        while True:
            headers = {
                "Accept": "application/json",
            }
            params = {
                "location_id": self.location_id,
                "operation": "rent",
                "limit": self.per_page,
                "page": page,
            }
            resp = requests.get(
                f"{self.BASE_URL}/adverts", headers=headers, params=params, timeout=10
            )

            if resp.status_code in (429, 500, 502, 503):
                wait = 1
                for _ in range(5):
                    time.sleep(wait)
                    resp = requests.get(
                        f"{self.BASE_URL}/adverts",
                        headers=headers,
                        params=params,
                        timeout=10,
                    )
                    if resp.status_code == 200:
                        break
                    wait *= 2

            try:
                resp.raise_for_status()
            except requests.HTTPError as e:
                print(f"Erro na página {page}: {e}")
                break

            page_ads = resp.json().get("adverts", [])

            fname = f"{time.strftime('%Y%m%d')}_page{page}.json"
            with open(os.path.join(data_dir, fname), "w", encoding="utf-8") as f:
                json.dump(resp.json(), f, ensure_ascii=False, indent=2)

            if not page_ads:
                print("Fim da paginação: nenhum novo anúncio.")
                break

            all_ads.extend(page_ads)
            print(f"Página {page}: {len(page_ads)} anúncios obtidos.")
            page += 1
            time.sleep(0.2)

        return all_ads


if __name__ == "__main__":
    auth = OLXAuth()
    # Substitua "100001" pelo location_id real de Lisboa se necessário
    client = OLXClient(auth, per_page=50, location_id="100001")
    adverts = client.fetch_rent_adverts()
    print(f"Total de anúncios coletados: {len(adverts)}")
