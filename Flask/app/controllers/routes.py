from flask import render_template, Blueprint, redirect, url_for, flash, abort
import app.forms.forms as forms 
from flask_sqlalchemy import SQLAlchemy
import app.models.models as models
from app.extensions import db
from datetime import datetime
import app.functions as func

routes_bp = Blueprint('routes', __name__)

@routes_bp.route("/")
def landing_page():
    return render_template("landing_page/index.html")

@routes_bp.route("/login")
def login():
    form = forms.loginForm()
    if form.validate_on_submit():
        usuario = models.Usuarios.query.filter_by(email = form.email.data).first()
        if usuario is None:
            try: 
                usuario = forms.Usuarios(
                    nome = form.nome.data, 
                )
                db.session.add(usuario)
                db.session.commit()
                form.nome.data = ''
                flash("Registro realizado com sucesso!", "success")
            except Exception as e:
                db.session.rollback()
                flash("Erro ao registrar o usuário: {e}", "danger")
        else:
            flash("Esse e-mail já está registrado.", "warning")        
    return render_template('login/login.html', form=form)

@routes_bp.route("/registro", methods=['GET', 'POST'])
def registro():
    form = forms.registroForm()
    if form.validate_on_submit():
        usuario = models.Usuarios.query.filter_by(email = form.email.data).first()
        if usuario is None:
            try: 
                usuario = models.Usuarios(
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
                flash(f"Erro ao registrar o usuário: {e}", "danger")
        else:
            flash("Esse e-mail já está registrado.", "warning")        
    return render_template('registro/registro.html', form=form)


@routes_bp.route('/header')
def serve_header():
    return render_template('header/header.html') 

@routes_bp.route('/footer')
def serve_footer():
    return render_template('footer/footer.html')

@routes_bp.route("/perfil_bicho/<nome_bicho>")
def perfil_bicho(nome_bicho):
    return render_template("perfil_bicho/index.html", nome_bicho=nome_bicho)

# Invalid URL

@routes_bp.errorhandler(404)
def page_not_found(e):
    return render_template("erro/erro.html", erro = 404), 404

#Internal Server Error 

@routes_bp.errorhandler(500)
def page_not_found(e):
    return render_template("erro/erro.html", erro = 500), 500

@routes_bp.route("/usuarios")
def usuarios():
    return render_template("usuarios/index.html")