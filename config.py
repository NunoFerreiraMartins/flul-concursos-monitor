"""
Configuração do monitor FLUL
"""

# Página a monitorizar
URL = (
    "https://www.letras.ulisboa.pt/pt/sobre-a-flul/"
    "administracao-e-servicos/recursos-humanos/"
    "procedimentos-concursais/ano-de-2026"
)

# Ficheiro onde será guardado o histórico
DATABASE_FILE = "concursos.json"

# Nome do site
SITE_NAME = "Faculdade de Letras da Universidade de Lisboa"

# Timeout das ligações
REQUEST_TIMEOUT = 30

# User Agent
USER_AGENT = (
    "Mozilla/5.0 "
    "(X11; Linux x86_64) "
    "AppleWebKit/537.36 "
    "(KHTML, like Gecko) "
    "Chrome/137.0 Safari/537.36"
)

# Endereço de email do remetente
EMAIL_FROM = "EMAIL_USER"

# Endereço do destinatário
EMAIL_TO = "EMAIL_TO"

# Servidor SMTP (Gmail)
SMTP_SERVER = "smtp.gmail.com"

SMTP_PORT = 587
