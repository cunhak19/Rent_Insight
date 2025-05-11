# src/data/olx_api/client.py

import os, time, json
import requests
from src.data.olx_api.auth import OLXAuth

RAW_DIR = os.path.abspath(os.path.join(__file__, "../../../data/raw/olx"))
os.makedirs(RAW_DIR, exist_ok=True)


class OLXClient:
    BASE_URL = "https://www.olx.pt/api/open"
    VERSION_HEADER = {"Version": "2.0"}
    "scope": "read write v2"

    def __init__(self, auth: OLXAuth, per_page=50):
        self.auth = auth
        self.per_page = per_page

    def fetch_rent_adverts(self):
        """Pega todos os anúncios de aluguel, salva JSONs em data/raw/olx/ e retorna lista unida."""
        all_ads = []
        offset = 0

        while True:
            token = self.auth.get_token()
            headers = {**self.VERSION_HEADER, "Authorization": f"Bearer {token}"}
            params = {"category": "rent", "limit": self.per_page, "offset": offset}

            try:
                resp = requests.get(
                    f"{self.BASE_URL}/adverts",
                    headers=headers,
                    params=params,
                    timeout=10,
                )
                # Se token expirou
                if resp.status_code == 401:
                    # força renovação e retry
                    token = self.auth.get_token()
                    headers["Authorization"] = f"Bearer {token}"
                    resp = requests.get(
                        f"{self.BASE_URL}/adverts",
                        headers=headers,
                        params=params,
                        timeout=10,
                    )

                # Se rate‑limit ou erro servidor
                if resp.status_code in (429, 500, 502, 503):
                    wait = 1
                    for i in range(5):
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

                resp.raise_for_status()
                data = resp.json().get("data", [])
            except Exception as e:
                print(f"Erro fetching offset={offset}: {e}")
                break

            # salvar JSON bruto
            fname = f"{time.strftime('%Y%m%d')}_offset{offset}.json"
            with open(os.path.join(RAW_DIR, fname), "w", encoding="utf-8") as f:
                json.dump(resp.json(), f, ensure_ascii=False, indent=2)

            if not data:
                print("Nenhum anúncio retornado — fim da paginação.")
                break

            all_ads.extend(data)
            print(f"Offset {offset}: obtidos {len(data)} anúncios.")
            offset += len(data)

            # pequena pausa para não saturar
            time.sleep(0.2)

        return all_ads


if __name__ == "__main__":
    auth = OLXAuth()
    client = OLXClient(auth)
    ads = client.fetch_rent_adverts()
    print(f"Total anúncios coletados: {len(ads)}")
