from flask import render_template, Blueprint, redirect, url_for, flash, abort, request
from werkzeug.security import generate_password_hash, check_password_hash
import app.forms.forms as forms
import app.models.models as models
from app.extensions import db
from datetime import datetime
import app.functions as func
from flask_login import login_user, login_required, logout_user, current_user

usuario_routes_bp = Blueprint('usuario_routes', __name__)

@usuario_routes_bp.route("/perfil-<slug>", methods=['GET', 'POST'])
@login_required
def perfil_usuario(slug):
    # Buscar o usuário baseado no slug
    usuario = models.Usuarios.query.filter_by(slug=slug).first_or_404()

    # Verificar se o usuário autenticado é o mesmo que está acessando o perfil
    if usuario.ID_usuario != current_user.ID_usuario:
        flash("Você não tem permissão para acessar este perfil.", "danger")
        return redirect(url_for('routes.landing_page'))  # Redirecionar para a página inicial

    form = forms.BichoForm()
    
    return render_template(
        "perfil_usuario/perfil_usuario.html", 
        form=form,
        usuario=usuario
    )


@usuario_routes_bp.route('/atualizar_usuario/<int:ID_usuario>', methods=['GET', 'POST'])
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
            nome_anterior = atualizacao.nome  
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
            if nome_anterior != atualizacao.nome:
                slug_nome = (atualizacao.nome)
                atualizacao.slug = f"{slug_nome}-{atualizacao.ID_usuario}"

            try:
                db.session.commit()
                flash(f"Usuário {atualizacao.nome} atualizado com sucesso")
                return redirect(url_for('usuario_routes.perfil_usuario', slug = current_user.slug))
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