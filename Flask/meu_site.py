from flask import Flask, render_template, jsonify, abort, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

app = Flask(__name__)

# Integrando com SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123Salsich%40#@localhost/ong'
# Secret Key
app.config['SECRET_KEY'] = "123Salsich@#"
# Inicializando o db
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

# Criar formulario Registro
class registroForm(FlaskForm):
    nomeUsuario = StringField("Nome de usuário", validators=[DataRequired()])
    email = StringField("Email", validators=[Email()])
    senha = StringField("Senha", validators=[DataRequired(), Length(min=8, max=20)])
    enviar = SubmitField("Enviar")

# Define o perfil do Usuario
# class Usuarios(db.model):
#     __tablename__ = 'pessoa'



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

@app.route("/registro", methods=['GET', 'POST'])
def registro():
    form = registroForm()
    if form.validate_on_submit():
        form.nomeUsuario.data = ''
        form.email.data = ''
        form.senha.data = ''
        flash("Form submitted successfully")
    return render_template('registro/registro.html', form=form)


@app.route('/header')
def serve_header():
    return render_template('header/header.html') 

@app.route('/footer')
def serve_footer():
    return render_template('footer/footer.html')

if __name__ == "__main__":
    app.run(debug = True)