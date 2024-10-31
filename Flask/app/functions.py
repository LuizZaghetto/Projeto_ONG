import json

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