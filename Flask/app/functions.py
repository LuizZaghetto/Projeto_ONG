import json
import re
import app.models.models as models
import app.forms.forms as forms 
from app.extensions import db


def carregar_json(filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
                return json.load(file)
    except FileNotFoundError:
        print(f"Erro: O arquivo '{filename}' não foi encontrado.")
        return []
    except json.JSONDecodeError:
        print(f"Erro: O arquivo '{filename}' não é um JSON válido.")
        return []
    
import re

def formatar_cpf(cpf):
    # Remove qualquer caractere que não seja número
    cpf = re.sub(r'\D', '', cpf)
    
    # Aplica o formato XXX.XXX.XXX-XX
    if len(cpf) == 11:
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
    return cpf

def formatar_telefone(telefone):
    # Remove qualquer caractere que não seja número
    telefone = re.sub(r'\D', '', telefone)
    
    # Aplica a formatação (99) 99999-9999
    if len(telefone) == 11:
        return f"({telefone[:2]}) {telefone[2:7]}-{telefone[7:]}"
    elif len(telefone) == 10:
        return f"({telefone[:2]}) {telefone[2:6]}-{telefone[6:]}"
    return telefone

def atualizar_dados_formatados():
    usuarios = models.Usuarios.query.all()  # Obtem todos os usuários do banco de dados
    for usuario in usuarios:
        # Formatar CPF e Telefone se necessário
        usuario.CPF = formatar_cpf(usuario.CPF)
        usuario.telefone = formatar_telefone(usuario.telefone)
        
        # Salvar no banco de dados
        db.session.commit()  # Salva as alterações no banco

    print("Dados atualizados com sucesso!")
