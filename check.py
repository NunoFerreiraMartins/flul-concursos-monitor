import os
import traceback

from parser import extrair_concursos
from storage import atualizar, novos
from mail import enviar_email
from config import DATABASE_FILE


def main():

    concursos = extrair_concursos()

    print(f"{len(concursos)} concursos encontrados.")

    if not os.path.exists(DATABASE_FILE):

        print("Primeira execução.")

        atualizar(concursos)

        print("Histórico criado. Não será enviado qualquer email.")

        return

    concursos_novos = novos(concursos)

    if concursos_novos:

        enviar_email(concursos_novos)

        print(f"{len(concursos_novos)} novos concursos enviados.")

    else:

        print("Sem novidades.")

    atualizar(concursos)


if __name__ == "__main__":

    try:
        main()

    except Exception:
        traceback.print_exc()
        raise
