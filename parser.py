"""
parser.py
Extrai concursos da página da FLUL.
"""

import logging
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from config import URL, REQUEST_TIMEOUT, USER_AGENT

logging.basicConfig(level=logging.INFO)

HEADERS = {"User-Agent": USER_AGENT}


def obter_html(url):
    r = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
    r.raise_for_status()
    return r.text


def limpar(txt):
    return " ".join((txt or "").split())


def extrair_concursos():
    """
    Devolve uma lista de dicionários:
    {
        "titulo": "...",
        "link": "...",
        "descricao": "..."
    }
    """
    html = obter_html(URL)
    soup = BeautifulSoup(html, "lxml")

    concursos = []
    vistos = set()

    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        texto = limpar(a.get_text(" ", strip=True))
        if not texto:
            continue

        link = urljoin(URL, href)

        # Mantém apenas ligações relevantes para documentos/concursos
        h = link.lower()
        if not (
            h.endswith(".pdf")
            or "/document/" in h
            or "/doc_download/" in h
            or "concurso" in texto.lower()
        ):
            continue

        chave = (texto.lower(), link.lower())
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

    concursos.sort(key=lambda c: c["titulo"].lower())
    logging.info("%d concursos encontrados", len(concursos))
    return concursos


if __name__ == "__main__":
    for c in extrair_concursos():
        print(c["titulo"])
        print(c["link"])
        print()
