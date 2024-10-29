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
    nome = StringField("Nome de usuário", validators=[DataRequired()])
    email = StringField("Email", validators=[Email()])
    data_nasc = StringField("Data de Nascimento", validators=[DataRequired()])
    CPF = StringField("CPF", validators=[DataRequired()])
    telefone = StringField("Número de Telefone", validators=[DataRequired()])
    # senha = StringField("Senha", validators=[DataRequired(), Length(min=8, max=20)])
    enviar = SubmitField("Enviar")

# Define o perfil do Usuario
class Usuarios(db.Model):
    __tablename__ = 'pessoa'
    ID_usuario = db.Column(db.Integer, primary_key=True, nullable=False)
    nome = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    telefone = db.Column(db.String(20), nullable=False)
    data_nasc = db.Column(db.Date, nullable=False)
    CPF = db.Column(db.String(15), nullable=False, unique = True)

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
        usuario = Usuarios.query.filter_by(email = form.email.data).first()
        if usuario is None:
            try: 
                usuario = Usuarios(
                    nome = form.nome.data, 
                    email = form.email.data,
                    telefone = form.telefone.data,
                    data_nasc = datetime.strptime(form.data_nasc.data, '%Y-%m-%d'),
                    CPF = form.CPF.data
                )
                db.session.add(usuario)
                db.session.commit()
                form.nome.data = ''
                form.email.data = ''
                form.telefone.data = ''
                form.data_nasc.data = ''
                form.CPF.data = ''
                flash("Registro realizado com sucesso!", "success")
            except Exception as e:
                db.session.rollback()
                flash("Erro ao registrar o usuário: {e}", "danger")
        else:
            flash("Esse e-mail já está registrado.", "warning")        
    return render_template('registro/registro.html', form=form)

@app.route('/header')
def serve_header():
    return render_template('header/header.html') 

@app.route('/footer')
def serve_footer():
    return render_template('footer/footer.html')

#Invalid URL

@app.errorhandler(404)
def page_not_found(e):
    return render_template("erro/erro.html", erro = 404), 404

#Internal Server Error 

@app.errorhandler(500)
def page_not_found(e):
    return render_template("erro/erro.html", erro = 500), 500

if __name__ == "__main__":
    app.run(debug = True)