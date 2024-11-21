from flask import render_template, Blueprint, redirect, url_for, flash, abort, request
from werkzeug.security import generate_password_hash, check_password_hash
import app.forms.forms as forms 
from flask_sqlalchemy import SQLAlchemy
import app.models.models as models
from app.extensions import db
from datetime import datetime
import app.functions as func
from flask_login import login_user, login_required, logout_user, current_user

auth_routes_bp = Blueprint('auth_routes', __name__)

# Página de login
@auth_routes_bp.route("/login", methods=['GET', 'POST'])
def login():
    form = forms.loginForm()
    if form.validate_on_submit():
        usuario = models.Usuarios.query.filter_by(email=form.email.data).first()
        if usuario and check_password_hash(usuario.senha_hash, form.senha.data):
            login_user(usuario)
            flash("Login bem sucedido")
            return redirect(url_for('routes.interface_logado'))  # Roteamento do dashboard ou página protegida
        flash("Invalid username or password!")
    return render_template('login/login.html', form=form)

# Função de logout
@auth_routes_bp.route("/logout", methods = ["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for('routes.landing_page'))

# Página de registro
@auth_routes_bp.route("/registro", methods=['GET', 'POST'])
def registro():
    usuarioForm = forms.registroForm()
    ONGForm = forms.registroONGForm()

    tipo_conta = request.form.get('tipo_conta')

    if request.method == 'POST':
        if tipo_conta == 'usuario' and usuarioForm.validate_on_submit():
            adicionar = models.Usuarios.query.filter_by(email = usuarioForm.email.data).first()
            if adicionar is None:
                    # Formatar campos no backend
                    cpf_formatado = func.formatar_cpf(usuarioForm.CPF.data)
                    telefone_formatado = func.formatar_telefone(usuarioForm.telefone.data)
                    # Aplicando hash a senha
                    senha_hashed = generate_password_hash(usuarioForm.senha.data)
                    adicionar = models.Usuarios(
                        nome = usuarioForm.nome.data, 
                        email = usuarioForm.email.data,
                        telefone = telefone_formatado,
                        data_nasc = usuarioForm.data_nasc.data.strftime('%Y-%m-%d'),                
                        CPF = cpf_formatado,
                        senha_hash = senha_hashed
                    )
        elif tipo_conta == 'ONG' and ONGForm.validate_on_submit():
            adicionar = models.ONG.query.filter_by(email = ONGForm.email.data).first()
            if adicionar is None:
                # Formatar campos no backend
                    telefone_formatado = func.formatar_telefone(usuarioForm.telefone.data)
                # Aplicando hash a senha
                    senha_hashed = generate_password_hash(ONGForm.senha.data)
                    adicionar = models.ONG(
                    nome = ONGForm.nome.data,
                    email = ONGForm.email.data, 
                    telefone = ONGForm.telefone.data, 
                    CEP = ONGForm.CEP.data,
                    endereco = ONGForm.endereco.data,
                    bairro = ONGForm.bairro.data,
                    cidade = ONGForm.cidade.data,
                    UF = ONGForm.UF.data, 
                    CPNJ = ONGForm.CPNJ.data,
                    senha_hash = senha_hashed
                )
        if adicionar:
            db.session.add(adicionar)
            db.session.commit()
            return redirect(url_for("auth_routes.login"))
    return render_template('registro/registro.html', form=usuarioForm, formONG = ONGForm)


