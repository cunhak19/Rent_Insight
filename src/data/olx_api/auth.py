import os
import time
import requests
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()


class OLXAuth:
    """
    Gerencia o fluxo OAuth2 client_credentials para a OLX Partner API.
    """

    # Endpoint correto para Portugal conforme documentação
    TOKEN_URL = "https://www.olx.pt/api/open/oauth/token"

    def __init__(self):
        # Lê credenciais do .env
        self.client_id = os.getenv("OLX_CLIENT_ID")
        self.client_secret = os.getenv("OLX_CLIENT_SECRET")
        self.token = None
        self.expires_at = 0

    def get_token(self) -> str:
        """
        Retorna um access token válido. Renova automaticamente se estiver expirado ou prestes a expirar.
        """
        # Renova se não tiver token ou faltar menos de 60s para expirar
        if not self.token or time.time() >= self.expires_at - 60:
            # Payload em JSON conforme especificação
            payload = {
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "scope": "read write v2",
            }
            headers = {"Accept": "application/json", "Content-Type": "application/json"}
            # Requisição de token
            resp = requests.post(
                self.TOKEN_URL, json=payload, headers=headers, timeout=10
            )
            resp.raise_for_status()

            # Debug inicial (pode remover depois)
            print("TOKEN STATUS", resp.status_code, "BODY:", resp.text[:200])

            data = resp.json()
            # Armazena token e calcula expiração
            self.token = data["access_token"]
            expires_in = data.get("expires_in", 3600)
            self.expires_at = time.time() + expires_in

        return self.token


if __name__ == "__main__":
    auth = OLXAuth()
    token = auth.get_token()
    # Exibe apenas os primeiros caracteres para segurança
    print("Access token:", token[:10] + "…")
