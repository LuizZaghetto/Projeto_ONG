import json
import re

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
    
def formatar_CPF(cpf):
    # Remove qualquer caractere não numérico
    cpf = re.sub(r'\D', '', cpf)
    
    # Verifica se o CPF tem exatamente 11 dígitos
    if len(cpf) == 11:
        return f'{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}'
    else:
        raise ValueError("CPF inválido. Deve conter exatamente 11 dígitos.")