"""
check.py

Programa principal.
"""

import traceback

from parser import extrair_concursos
from storage import atualizar, novos
from mail import enviar_email


def main():

    print("=" * 60)
    print("Monitor FLUL")
    print("=" * 60)

    concursos = extrair_concursos()

    print(f"Foram encontrados {len(concursos)} concursos na página.")

    if not concursos:
        print("Nenhum concurso encontrado.")
        return

    concursos_novos = novos(concursos)

    if concursos_novos:

        print(f"Foram encontrados {len(concursos_novos)} concursos novos.")

        enviar_email(concursos_novos)

    else:

        print("Não existem concursos novos.")

    atualizar(concursos)

    print("Histórico atualizado.")


if __name__ == "__main__":

    try:
        main()

    except Exception:

        print()

        print("=" * 60)
        print("ERRO")
        print("=" * 60)

        traceback.print_exc()

        raise
