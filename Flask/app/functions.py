import json
import re
import app.models.models as models
import app.forms.forms as forms 
from app.extensions import db
import requests
import random
from faker import Faker
from werkzeug.security import generate_password_hash
import app.models.models as models
import hashlib
import time


fake = Faker("pt_BR")

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

def criar_usuarios():
    usuarios = []
    for _ in range(100):
        senha = fake.password(length=12, special_chars=True, digits=True, upper_case=True, lower_case=True)
        senha_hash = generate_password_hash(senha)  # Hashea a senha gerada
        usuario = models.Usuarios(
            nome=fake.name(),
            email=fake.email(),
            telefone=fake.phone_number(),
            data_nasc=fake.date_of_birth(minimum_age=18, maximum_age=70),
            CPF=fake.ssn(),
            senha_hash=senha_hash,  # Ajuste o campo de senha no seu modelo
        )
        print(f"Usuário criado: {usuario.nome}, Email: {usuario.email}, Senha: {senha}")
        usuarios.append(usuario)
    return usuarios

def adicionar_usuarios_ao_bd(usuarios):
    try:
        db.session.bulk_save_objects(usuarios)
        db.session.commit()
        print("100 usuários adicionados com sucesso!")
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao adicionar usuários: {e}")

def gerar_hash(filename):
    """Gera um hash único baseado no nome do arquivo e no timestamp atual."""
    timestamp = str(time.time()).encode('utf-8')
    nome_arquivo = filename.encode('utf-8')
    return hashlib.sha256(nome_arquivo + timestamp).hexdigest()[:15]