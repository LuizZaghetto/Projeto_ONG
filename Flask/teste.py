import os
from dotenv import load_dotenv

# Carregar as variáveis do .env
load_dotenv(".gitignore/.env")

# Acessar a senha do banco de dados
database_password = os.getenv("DATABASE_PASSWORD")

print(f"{database_password}")
print("Ola")