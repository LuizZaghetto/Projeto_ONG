from flask import render_template, Blueprint, redirect, url_for, flash, abort, request
from werkzeug.security import generate_password_hash, check_password_hash
import app.forms.forms as forms
import app.models.models as models
from app.extensions import db
from datetime import datetime
import app.functions as func
from flask_login import login_user, login_required, logout_user, current_user
from slugify import slugify


auth_routes_bp = Blueprint('auth_routes', __name__)


@auth_routes_bp.route("/login", methods=['GET', 'POST'])
def login():
    usuarioform = forms.loginForm()
    ONGform = forms.ONGloginForm()

    # Se o usuário já está autenticado, redirecionar para seu perfil
    if current_user.is_authenticated:
        return redirect(url_for("routes.perfil"))

    if request.method == "POST":
        form_type = request.form.get('form_type')
        if form_type == 'usuario' and usuarioform.validate_on_submit():
            usuario = models.Usuarios.query.filter_by(
                email=usuarioform.email.data).first()
            if usuario and check_password_hash(usuario.senha_hash, usuarioform.senha.data):
                login_user(usuario)
                flash("Login bem-sucedido!", "success")
                return redirect(url_for("routes.perfil"))
            else:
                flash("Credenciais inválidas.", "danger")
        elif form_type == 'ong' and ONGform.validate_on_submit():
            ong = models.ONG.query.filter_by(email=ONGform.email.data).first()
            if ong and check_password_hash(ong.senha_hash, ONGform.senha.data):
                login_user(ong)
                flash("Login bem-sucedido!", "success")
                return redirect(url_for("routes.perfil"))
            else:
                flash("Credenciais inválidas.", "danger")
        else:
            flash("Por favor, preencha o formulário corretamente.", "warning")

    return render_template("login/login.html", usuarioform=usuarioform, ONGform=ONGform)


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
    usuarioform = forms.registroForm()
    ONGform = forms.ONGregistroForm()
    if current_user.is_authenticated:
        return redirect(url_for("routes.perfil"))
    # Verificar qual formulário foi enviado
    if request.method == 'POST':
        form_type = request.form.get('form_type')

        if form_type == 'usuario' and usuarioform.validate_on_submit():
            # Lógica para o formulário de usuário
            usuario = models.Usuarios.query.filter_by(
                email=usuarioform.email.data).first()
            if usuario is None:
                try:
                    # Formatar CPF e Telefone no backend
                    cpf_formatado = func.formatar_cpf(usuarioform.CPF.data)
                    telefone_formatado = func.formatar_telefone(
                        usuarioform.telefone.data)

                    # Aplicando hash à senha
                    senha_hashed = generate_password_hash(
                        usuarioform.senha.data)

                    slug_usuario = slugify(usuarioform.nome.data)

                    usuario = models.Usuarios(
                        nome=usuarioform.nome.data,
                        email=usuarioform.email.data,
                        telefone=telefone_formatado,
                        data_nasc=usuarioform.data_nasc.data.strftime(
                            '%Y-%m-%d'),
                        CPF=cpf_formatado,
                        senha_hash=senha_hashed,
                        slug=slug_usuario
                    )

                    # Adicionando e commitando no banco de dados
                    db.session.add(usuario)
                    db.session.commit()
                    # Concatenando o id no slug
                    usuario.slug = f"{slug_usuario}-{usuario.ID_usuario}"

                    db.session.commit()  # Commit a atualização do slug com ID

                    flash("Registro de usuário realizado com sucesso!", "success")
                    return redirect(url_for("auth_routes.login"))
                except Exception as e:
                    db.session.rollback()  # Reverter mudanças no banco em caso de erro
                    flash(f"Erro ao registrar o usuário: {e}", "danger")
            else:
                flash("Esse e-mail já está registrado.", "warning")
        elif form_type == 'ong' and ONGform.validate_on_submit():
            # Lógica para o formulário de ONG
            ong = models.ONG.query.filter_by(email=ONGform.email.data).first()
            if ong is None:
                try:
                    # Aplicando hash à senha
                    senha_hashed = generate_password_hash(ONGform.senha.data)

                    slug_ong = slugify(ONGform.nome.data)

                    ong = models.ONG(
                        nome=ONGform.nome.data,
                        email=ONGform.email.data,
                        telefone=ONGform.telefone.data,
                        CEP=ONGform.CEP.data,
                        endereco=ONGform.endereco.data,
                        bairro=ONGform.bairro.data,
                        cidade=ONGform.cidade.data,
                        UF=ONGform.UF.data,
                        CNPJ=ONGform.CNPJ.data,
                        senha_hash=senha_hashed,
                        slug=slug_ong
                    )

                    # Adicionando e commitando no banco de dados
                    db.session.add(ong)
                    db.session.commit()
                    # Concatenando o id no slug
                    ong.slug = f"{slug_ong}-{ong.ID_ONG}"

                    db.session.commit()  # Commit a atualização do slug com ID

                    flash("Registro de ONG realizado com sucesso!", "success")
                    return redirect(url_for("auth_routes.login"))
                except Exception as e:
                    db.session.rollback()  # Reverter mudanças no banco em caso de erro
                    flash(f"Erro ao registrar a ONG: {e}", "danger")
            else:
                flash("Esse e-mail já está registrado.", "warning")
        else:
            flash("Erro no formulário, corrija os campos destacados.", "warning")
    return render_template('registro/registro.html', usuarioform=usuarioform, ONGform=ONGform)
