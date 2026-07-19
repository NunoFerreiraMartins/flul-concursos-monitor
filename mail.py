"""
mail.py

Envia notificações por email quando forem encontrados novos concursos.
"""

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

from config import SMTP_SERVER, SMTP_PORT


def criar_html(concursos):
    """Cria o corpo HTML do email."""

    data = datetime.now().strftime("%d/%m/%Y %H:%M")

    html = f"""
    <html>
    <body style="font-family:Arial,Helvetica,sans-serif">

    <h2>📢 Novos concursos publicados na FLUL</h2>

    <p>
    Foram encontrados <strong>{len(concursos)}</strong>
    novos procedimentos concursais.
    </p>

    <hr>
    """

    for concurso in concursos:

        html += f"""
        <h3>{concurso['titulo']}</h3>

        <p>
        <a href="{concurso['link']}">
        {concurso['link']}
        </a>
        </p>

        """

        if concurso.get("descricao"):

            html += f"""
            <p>{concurso['descricao']}</p>
            """

        html += "<hr>"

    html += f"""

    <p>
    Detetado automaticamente em {data}.
    </p>

    </body>
    </html>
    """

    return html


def enviar_email(concursos):

    email_user = os.environ["EMAIL_USER"]
    email_password = os.environ["EMAIL_PASSWORD"]
    email_to = os.environ["EMAIL_TO"]

    mensagem = MIMEMultipart("alternative")

    mensagem["Subject"] = (
        f"FLUL: {len(concursos)} novo(s) concurso(s)"
    )

    mensagem["From"] = email_user
    mensagem["To"] = email_to

    html = criar_html(concursos)

    mensagem.attach(MIMEText(html, "html"))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:

        smtp.starttls()

        smtp.login(
            email_user,
            email_password,
        )

        smtp.sendmail(
            email_user,
            email_to,
            mensagem.as_string(),
        )
