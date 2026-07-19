import json
import requests
from bs4 import BeautifulSoup

URL = "https://www.letras.ulisboa.pt/pt/sobre-a-flul/administracao-e-servicos/recursos-humanos/procedimentos-concursais/ano-de-2026"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def obter_html():
    resposta = requests.get(URL, headers=HEADERS, timeout=30)
    resposta.raise_for_status()
    return resposta.text


def extrair_concursos(html):
    soup = BeautifulSoup(html, "lxml")

    # Vamos implementar esta função no próximo passo
    concursos = []

    return concursos


def main():
    html = obter_html()
    concursos = extrair_concursos(html)

    print(f"Foram encontrados {len(concursos)} concursos.")


if __name__ == "__main__":
    main()
