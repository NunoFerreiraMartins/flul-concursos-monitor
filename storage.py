"""
storage.py

Guarda e lê o histórico dos concursos encontrados.
"""

import json
import os

from config import DATABASE_FILE


def carregar():
    """
    Lê o ficheiro concursos.json.

    Se não existir devolve uma lista vazia.
    """

    if not os.path.exists(DATABASE_FILE):
        return []

    try:
        with open(DATABASE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    except (json.JSONDecodeError, OSError):
        return []


def guardar(concursos):
    """
    Guarda a lista de concursos.
    """

    with open(DATABASE_FILE, "w", encoding="utf-8") as f:
        json.dump(
            concursos,
            f,
            indent=4,
            ensure_ascii=False,
        )


def _id(concurso):
    """
    Identificador único de um concurso.
    """

    return (
        concurso["titulo"].strip().lower(),
        concurso["link"].strip().lower(),
    )


def novos(concursos_atuais):
    """
    Compara os concursos atuais com o histórico.

    Devolve apenas os concursos novos.
    """

    antigos = carregar()

    ids_antigos = {_id(c) for c in antigos}

    novos_concursos = []

    for concurso in concursos_atuais:

        if _id(concurso) not in ids_antigos:
            novos_concursos.append(concurso)

    return novos_concursos


def atualizar(concursos_atuais):
    """
    Atualiza o ficheiro local.
    """

    guardar(concursos_atuais)
