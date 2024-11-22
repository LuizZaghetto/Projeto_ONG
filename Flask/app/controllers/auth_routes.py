from flask import render_template, Blueprint, redirect, url_for, flash, abort, request
from werkzeug.security import generate_password_hash, check_password_hash
import app.forms.forms as forms
import app.models.models as models
from app.extensions import db
from datetime import datetime
import app.functions as func
from flask_login import login_user, login_required, logout_user, current_user

auth_routes_bp = Blueprint('auth_routes', __name__)

# Página de login
@auth_routes_bp.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        form = forms.bichoForm()
        flash('Usuário já autenticado', 'warning')
        return render_template('interface_logado/interface_logado.html', form=form)
    else:
        form = forms.loginForm()
        if form.validate_on_submit():
            usuario = models.Usuarios.query.filter_by(email=form.email.data).first()
            if usuario and check_password_hash(usuario.senha_hash, form.senha.data):
                login_user(usuario)
                flash("Login bem-sucedido!", "success")
                return redirect(url_for('routes.interface_logado'))
            else:
                flash("Credenciais inválidas.", "danger")
        elif request.method == 'POST':
            flash("Erro no formulário, corrija os campos destacados.", "warning")
        return render_template('login/login.html', form=form)


# Função de logout
@auth_routes_bp.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    flash("Logout realizado com sucesso!", "info")
    return redirect(url_for('routes.landing_page'))

# Página de registro
@auth_routes_bp.route("/registro", methods=['GET', 'POST'])
def registro():
    form = forms.registroForm()
    if form.validate_on_submit():
        usuario = models.Usuarios.query.filter_by(email=form.email.data).first()
        if usuario is None:
            try:
                # Formatar CPF e Telefone no backend
                cpf_formatado = func.formatar_cpf(form.CPF.data)
                telefone_formatado = func.formatar_telefone(form.telefone.data)

                # Aplicando hash à senha
                senha_hashed = generate_password_hash(form.senha.data)
                usuario = models.Usuarios(
                    nome=form.nome.data,
                    email=form.email.data,
                    telefone=telefone_formatado,
                    data_nasc=form.data_nasc.data.strftime('%Y-%m-%d'),
                    CPF=cpf_formatado,
                    senha_hash=senha_hashed
                )

                # Adicionando e commitando no banco de dados
                db.session.add(usuario)
                db.session.commit()

                flash("Registro realizado com sucesso!", "success")
                return redirect(url_for("auth_routes.login"))
            except Exception as e:
                db.session.rollback()  # Reverter mudanças no banco em caso de erro
                flash(f"Erro ao registrar o usuário: {e}", "danger")
        else:
            flash("Esse e-mail já está registrado.", "warning")
    elif request.method == 'POST':
        flash("Erro no formulário, corrija os campos destacados.", "warning")
    return render_template('registro/registro.html', form=form)

