from flask import render_template, Blueprint, redirect, url_for, flash, abort, request, session
import logging
from werkzeug.security import generate_password_hash, check_password_hash
import app.forms.forms as forms 
from flask_sqlalchemy import SQLAlchemy
import app.models.models as models
from app.extensions import db
from datetime import datetime
import app.functions as func
from flask_login import login_user, login_required, logout_user, current_user
from app.controllers.auth_routes import auth_routes_bp
from app.controllers.usuario_routes import usuario_routes_bp
from app.controllers.admin_routes import admin_routes_bp
from app.controllers.ong_routes import ong_routes_bp

# Configuração básica de logging
logging.basicConfig(filename="app.log", level=logging.ERROR, 
                    format="%(asctime)s %(levelname)s: %(message)s")


# Configuração do tempo limite de sessão
SESSION_TIMEOUT = 3600  # Tempo em segundos (1 hora)

routes_bp = Blueprint('routes', __name__)

routes_bp.register_blueprint(auth_routes_bp)
routes_bp.register_blueprint(usuario_routes_bp)
routes_bp.register_blueprint(admin_routes_bp)
routes_bp.register_blueprint(ong_routes_bp)


@auth_routes_bp.before_request
def session_timeout():
    session.permanent = True
    auth_routes_bp.permanent_session_lifetime = SESSION_TIMEOUT

# Página inicial
@routes_bp.route("/", methods=['GET', 'POST'])
def landing_page():
    return render_template("landing_page/index.html")

# Acessar o Perfil
@routes_bp.route("/redirecionar-perfil")
@login_required
def perfil():
    print(current_user.tipo)
    if current_user.tipo == 0:
        return redirect(url_for("usuario_routes.perfil_usuario", slug = current_user.slug))
    elif current_user.tipo == 1:
        return redirect(url_for("ong_routes.perfil_ong", slug = current_user.slug))
    else:
        flash("Tipo de usuário desconhecido.", "warning")
        return redirect(url_for("auth_routes_bp.login"))


# Acessar o perfil do bicho
@routes_bp.route("/perfil_bicho/<nome_bicho>")
@login_required
def perfil_bicho(nome_bicho):
    return render_template("perfil_bicho/index.html", nome_bicho=nome_bicho)


@routes_bp.route("/adicionar_bicho", methods=['GET', 'POST'])
@login_required
def adicionar_bicho():
    form = forms.BichoForm()
    
    # Verificar o tipo de usuário
    if current_user.tipo == 1:  # Certifique-se de que o atributo `tipo` está implementado no usuário
        id_ong = current_user.ID_ONG
        id_usuario = None
    else:  # Usuário comum
        id_usuario = current_user.ID_usuario
        id_ong = None

    if form.validate_on_submit():
        bicho = models.Bichos(
            nome=form.nome.data,
            especie=form.especie.data,
            idade=form.idade.data,
            porte=form.porte.data,
            sexo = form.sexo.data,
            descricao=form.descricao.data,
            ID_usuario=id_usuario,
            ID_ONG=id_ong
        )
        db.session.add(bicho)
        db.session.commit()
        flash("Bicho cadastrado com sucesso!", "success")
        return redirect(url_for('routes.perfil'))

    return render_template("perfil_usuario/adicionar_bicho.html", form=form)


# Handler de erro 403 (proibido)
@auth_routes_bp.app_errorhandler(403)
def forbidden_error(error):
    return render_template('errors/403.html'), 403

# Handler de erro 404 (não encontrado)
@auth_routes_bp.app_errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

# Handler de erro 500 (erro interno do servidor)
@auth_routes_bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()  # Garantir rollback caso o erro seja relacionado ao banco
    return render_template('errors/500.html'), 500
