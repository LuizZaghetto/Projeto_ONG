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


# Configuração básica de logging
logging.basicConfig(filename="app.log", level=logging.ERROR, 
                    format="%(asctime)s %(levelname)s: %(message)s")


# Configuração do tempo limite de sessão
SESSION_TIMEOUT = 3600  # Tempo em segundos (1 hora)

routes_bp = Blueprint('routes', __name__)

routes_bp.register_blueprint(auth_routes_bp)

@auth_routes_bp.before_request
def session_timeout():
    session.permanent = True
    auth_routes_bp.permanent_session_lifetime = SESSION_TIMEOUT

# Página inicial
@routes_bp.route("/", methods=['GET', 'POST'])
def landing_page():
    return render_template("landing_page/index.html")

@routes_bp.route("/perfil", methods=['GET', 'POST'])
@login_required
def interface_logado():
    form = forms.bichoForm()
    return render_template(
        "interface_logado/interface_logado.html", 
        form=form
    )

@routes_bp.route('/atualizar_usuario/<int:ID_usuario>', methods=['GET', 'POST'])
def atualizar_usuario(ID_usuario):
    form = forms.AtualizarUsuarioForm()
    usuarios = models.Usuarios.query.order_by(models.Usuarios.ID_usuario)
    atualizacao = models.Usuarios.query.get_or_404(ID_usuario)
    if request.method == "POST":
        if form.validate_on_submit():
            senha_atual = request.form['senha_atual']
            if not check_password_hash(atualizacao.senha_hash, senha_atual):
                flash("Senha atual incorreta. Tente novamente.")
                return render_template(
                    "atualizar_usuario/atualizar_usuario.html",
                    form=form,
                    atualizacao=atualizacao,
                    usuarios=usuarios
                )
            atualizacao.nome = request.form['nome']
            atualizacao.email = request.form['email']
            atualizacao.telefone = request.form['telefone']
            atualizacao.data_nasc = request.form['data_nasc']
            atualizacao.CPF = request.form['CPF']
            nova_senha = request.form['senha']
            confirmacao_senha = request.form['senha2']
            if nova_senha and confirmacao_senha:
                if nova_senha == confirmacao_senha:
                    atualizacao.senha_hash = generate_password_hash(nova_senha)
                else:
                    flash("As senhas não coincidem. Tente novamente.")
                    return render_template(
                        "atualizar_usuario/atualizar_usuario.html",
                        form=form,
                        atualizacao=atualizacao,
                        usuarios=usuarios
                    )
            try:
                db.session.commit()
                flash(f"Usuário {atualizacao.nome} atualizado com sucesso")
                return redirect(url_for('routes.interface_logado'))
            except:
                flash("Erro, tente novamente.")
                return render_template(
                    "atualizar_usuario/atualizar_usuario.html",
                    form=form,
                    atualizacao=atualizacao,
                    usuarios=usuarios
                )
    return render_template(
        "atualizar_usuario/atualizar_usuario.html",
        form=form,
        atualizacao=atualizacao,
        usuarios=usuarios
    )


# Atualizar usuário usando admin
@routes_bp.route('/admin/atualizar_admin/<int:ID_usuario>', methods=['GET', 'POST'])
def atualizar_admin(ID_usuario):
    form = forms.registroForm()
    usuarios = models.Usuarios.query.order_by(models.Usuarios.ID_usuario)
    atualizacao = models.Usuarios.query.get_or_404(ID_usuario)
    if request.method == "POST":
        atualizacao.nome = request.form['nome']
        atualizacao.email = request.form['email']
        atualizacao.telefone = request.form['telefone']
        atualizacao.data_nasc = request.form['data_nasc']
        atualizacao.CPF = request.form['CPF']
        atualizacao.ID_usuario = request.form['ID_usuario']
        try:
            db.session.commit()
            flash(f"Usuário {ID_usuario} atualizado com sucesso")
            return render_template("atualizar_admin/atualizar_admin.html", 
            form = form,
            atualizacao = atualizacao,
            usuarios = usuarios)
        except:
            flash("Error")
            return render_template("atualizar_admin/atualizar_admin.html", 
            form = form,
            atualizacao = atualizacao,
            usuarios = usuarios)
    else:
        return render_template("atualizar_admin/atualizar_admin.html", 
        form = form,
        atualizacao = atualizacao,
        usuarios = usuarios)
    
# # Deletar Usuário
@routes_bp.route("/admin/excluir/<int:ID_usuario>", methods=['POST'])
@login_required
def excluir(ID_usuario):
    exclusao = models.Usuarios.query.get_or_404(ID_usuario)
    usuarios = models.Usuarios.query.order_by(models.Usuarios.ID_usuario)
    try:
        db.session.delete(exclusao)
        db.session.commit()
        flash(f"Usuario {exclusao.nome} deletado com sucesso")

        return redirect(url_for("routes.crud"))
    except:
        flash("Houve um problema ao deletar o usuário")
        return redirect(url_for("routes.crud"))

# Acessar o perfil do bicho
@routes_bp.route("/perfil_bicho/<nome_bicho>")
@login_required
def perfil_bicho(nome_bicho):
    return render_template("perfil_bicho/index.html", nome_bicho=nome_bicho)


@routes_bp.route("/adicionar_Bicho")
@login_required
def adicionar_bicho():
    form = forms.bichoForm()
    if form.validate_on_submit():
        bicho = models.Bichos(
            nome = form.nome.data,
            porte = form.porte.data
        )
        db.session.add(bicho)
        db.session.commit()
        return redirect(url_for('routes.interface_logado'))
    return render_template("adicionar_bicho")

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
