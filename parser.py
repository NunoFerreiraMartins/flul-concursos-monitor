"""
parser.py

Obtém a página da FLUL e extrai os procedimentos concursais.
"""

import logging
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from config import (
    URL,
    USER_AGENT,
    REQUEST_TIMEOUT,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

HEADERS = {
    "User-Agent": USER_AGENT
}


def obter_html():
    """
    Descarrega a página com até 3 tentativas.
    """

    ultimo_erro = None

    for tentativa in range(3):

        try:

            logging.info(
                "A descarregar página (tentativa %d)...",
                tentativa + 1,
            )

            resposta = requests.get(
                URL,
                headers=HEADERS,
                timeout=REQUEST_TIMEOUT,
            )

            resposta.raise_for_status()

            logging.info("Página descarregada.")

            return resposta.text

        except Exception as erro:

            ultimo_erro = erro

            logging.warning(
                "Tentativa %d falhou.",
                tentativa + 1,
            )

            time.sleep(5)

    raise ultimo_erro


def limpar(texto):
    """
    Remove espaços duplicados.
    """

    return " ".join(texto.split())


def link_relevante(texto, href):
    """
    Decide se uma ligação pode corresponder
    a um procedimento concursal.
    """

    texto = texto.lower()
    href = href.lower()

    palavras = (
        "concurso",
        "procedimento",
        "recrutamento",
        "edital",
        "aviso",
    )

    if any(p in texto for p in palavras):
        return True

    if href.endswith(".pdf"):
        return True

    return False


def extrair_concursos():
    """
    Extrai os concursos da página.

    Resultado:

    [
        {
            "titulo": "...",
            "link": "...",
            "descricao": "..."
        }
    ]
    """

    html = obter_html()

    soup = BeautifulSoup(html, "lxml")

    concursos = []

    vistos = set()

    for a in soup.find_all("a", href=True):

        href = a["href"].strip()

        texto = limpar(
            a.get_text(" ", strip=True)
        )

        if not texto:
            continue

        if not link_relevante(texto, href):
            continue

        link = urljoin(URL, href)

        chave = (
            texto.lower(),
            link.lower(),
        )

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

    concursos.sort(
        key=lambda c: c["titulo"].lower()
    )

    logging.info(
        "%d concursos encontrados.",
        len(concursos),
    )

    return concursos


if __name__ == "__main__":

    concursos = extrair_concursos()

    for concurso in concursos:

        print()

        print(concurso["titulo"])

        print(concurso["link"])
