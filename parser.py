"""
parser.py

Obtém a página da FLUL e extrai a lista de concursos.
"""

from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from config import REQUEST_TIMEOUT, URL, USER_AGENT

HEADERS = {
    "User-Agent": USER_AGENT
}


def obter_html():
    """Descarrega a página."""
    resposta = requests.get(
        URL,
        headers=HEADERS,
        timeout=REQUEST_TIMEOUT,
    )

    resposta.raise_for_status()
    return resposta.text


def limpar(texto):
    """Remove espaços repetidos."""
    return " ".join(texto.split())


def extrair_concursos():
    """
    Devolve uma lista de concursos.

    Cada concurso tem a forma:

    {
        "titulo": "...",
        "link": "...",
        "descricao": "..."
    }
    """

    html = obter_html()

    soup = BeautifulSoup(html, "lxml")

    concursos = []

    vistos = set()

    # Procuramos todas as ligações da página.
    # A página da FLUL costuma publicar cada concurso como um PDF ou uma página.

    for a in soup.find_all("a", href=True):

        href = a["href"].strip()

        texto = limpar(a.get_text(" ", strip=True))

        if not texto:
            continue

        href_lower = href.lower()

        texto_lower = texto.lower()

        # Filtrar apenas ligações relevantes
        if not (
            ".pdf" in href_lower
            or "concurso" in texto_lower
            or "procedimento" in texto_lower
            or "recrutamento" in texto_lower
            or "edital" in texto_lower
        ):
            continue

        link = urljoin(URL, href)

        chave = (texto, link)

        if chave in vistos:
            continue

        vistos.add(chave)

        concursos.append(
            {
                "titulo": texto,
                "link": link,
                "descricao": texto,
            }
        )

    concursos.sort(key=lambda x: x["titulo"])

    return concursos


if __name__ == "__main__":

    for concurso in extrair_concursos():
        print(concurso["titulo"])
        print(concurso["link"])
        print("-" * 60)
