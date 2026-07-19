import logging
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from config import URL, USER_AGENT, REQUEST_TIMEOUT

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

HEADERS = {
    "User-Agent": USER_AGENT
}


def obter_html(url):
    """
    Descarrega uma página com até 3 tentativas.
    """

    ultimo_erro = None

    for tentativa in range(3):

        try:

            logging.info("A abrir %s", url)

            resposta = requests.get(
                url,
                headers=HEADERS,
                timeout=REQUEST_TIMEOUT
            )

            resposta.raise_for_status()

            return resposta.text

        except Exception as erro:

            ultimo_erro = erro

            logging.warning(
                "Tentativa %d falhou.",
                tentativa + 1
            )

            time.sleep(5)

    raise ultimo_erro


def limpar(texto):

    return " ".join(texto.split())


def obter_categorias():

    """
    Procura automaticamente as categorias
    de concursos existentes na página principal.

    Devolve uma lista:

    [
        {
            "categoria": "...",
            "link": "..."
        }
    ]
    """

    html = obter_html(URL)

    soup = BeautifulSoup(html, "lxml")

    categorias = []

    vistos = set()

    for a in soup.find_all("a", href=True):

        texto = limpar(a.get_text())

        href = a["href"].strip()

        if not texto:
            continue

        texto_lower = texto.lower()

        if any(x in texto_lower for x in (
            "docentes",
            "investigadores",
            "técnicos",
            "tecnicos",
            "dl 57",
            "projetos",
            "projectos"
        )):

            link = urljoin(URL, href)

            if link in vistos:
                continue

            vistos.add(link)

            categorias.append({

                "categoria": texto,

                "link": link

            })

    logging.info(
        "Encontradas %d categorias.",
        len(categorias)
    )

    return categorias


def extrair_concursos_categoria(categoria):

    """
    Recebe uma categoria e devolve todos
    os concursos dessa categoria.

    Esta função será completada
    na segunda parte.
    """

    html = obter_html(categoria["link"])

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

        link = urljoin(categoria["link"], href)

        chave = (
            texto.lower(),
            link.lower()
        )

        if chave in vistos:
            continue

        vistos.add(chave)

        if (
            link.lower().endswith(".pdf")
            or "/document/" in link.lower()
            or "/doc_download/" in link.lower()
        ):

            concursos.append(
                {
                    "categoria": categoria["categoria"],
                    "titulo": texto,
                    "descricao": texto,
                    "link": link
                }
            )

    return concursos


def extrair_concursos():

    """
    Extrai todos os concursos
    de todas as categorias.
    """

    categorias = obter_categorias()

    concursos = []

    vistos = set()

    for categoria in categorias:

        logging.info(
            "A analisar %s...",
            categoria["categoria"]
        )

        try:

            lista = extrair_concursos_categoria(
                categoria
            )

            for concurso in lista:

                chave = (
                    concurso["titulo"].lower(),
                    concurso["link"].lower()
                )

                if chave in vistos:
                    continue

                vistos.add(chave)

                concursos.append(concurso)

        except Exception as erro:

            logging.exception(
                "Erro ao analisar %s",
                categoria["categoria"]
            )

    concursos.sort(
        key=lambda x: (
            x["categoria"].lower(),
            x["titulo"].lower()
        )
    )

    logging.info(
        "%d concursos encontrados.",
        len(concursos)
    )

    return concursos


if __name__ == "__main__":

    concursos = extrair_concursos()

    for concurso in concursos:

        print()

        print(
            f"[{concurso['categoria']}]"
        )

        print(concurso["titulo"])

        print(concurso["link"])
