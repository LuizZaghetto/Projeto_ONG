from flask import Flask, render_template, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123Salsich@#@localhost/ONG'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

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

@app.route("/")
def landing_page():
    return render_template("landing_page/index.html")
    
@app.route("/usuarios/<int:user_id>")
def usuarios(user_id):
    usuarios = carregar_json("usuarios.json")
    # Encontrar usuario pelo id
    usuario_encontrado = next((u for u in usuarios if u['user_id'] == user_id), None)

    if usuario_encontrado is None:
        return abort(404) #retorna um 404 se o usuario nao for encontrado
    
    animais = carregar_json("animais.json")
    
    return render_template("usuarios/index.html", usuario = usuario_encontrado, animais = animais)

@app.route("/perfil_bicho/<nome_bicho>")
def perfil_bicho(nome_bicho):
    return render_template("perfil_bicho/index.html", nome_bicho=nome_bicho)

@app.route("/login")
def login():
    return render_template('login/login.html')

@app.route("/registro")
def registro():
    return render_template('registro/registro.html')

@app.route('/header')
def serve_header():
    return render_template('header/header.html') 

@app.route('/footer')
def serve_footer():
    return render_template('footer/footer.html')

if __name__ == "__main__":
    app.run(debug = True)