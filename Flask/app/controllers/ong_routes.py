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

ong_routes_bp = Blueprint('ong_routes', __name__)

@ong_routes_bp.route("/perfil - ong - <slug>", methods=['GET', 'POST'])
@login_required
def perfil_ong(slug):
    # Buscar a ONG baseado no slug
    ong = models.ONG.query.filter_by(slug=slug).first_or_404()

    # Verificar se o usuário autenticado é o mesmo que está acessando o perfil
    if ong.ID_ONG != current_user.ID_ONG:
        flash("Você não tem permissão para acessar este perfil.", "danger")
        return redirect(url_for('routes.landing_page'))  # Redirecionar para a página inicial ou outra página de sua escolha

    form = forms.bichoForm()
    
    return render_template(
        "perfil_ong/perfil_ong.html", 
        form=form,
        ong = ong
    )

# Atualizar dados da ONG pelo usuário
@ong_routes_bp.route('/atualizar_ONG/<int:ID_ONG>', methods=['GET', 'POST'])
def atualizar_ong(ID_ONG):
    form = forms.AtualizarONGForm()
    ongs = models.ONG.query.order_by(models.ONG.ID_ONG)
    atualizacao = models.ONG.query.get_or_404(ID_ONG)
    print("teste inicial")
    if request.method == "POST":
        print("Reconhecendo o post")
        if form.validate_on_submit():
            senha_atual = request.form['senha_atual']
            if not check_password_hash(atualizacao.senha_hash, senha_atual):
                flash("Senha atual incorreta. Tente novamente.")
                return render_template(
                    "atualizar_ong/atualizar_ong.html",
                    form=form,
                    atualizacao=atualizacao,
                    ongs=ongs
                )
            atualizacao.nome = request.form['nome']
            atualizacao.email = request.form['email']
            atualizacao.telefone = request.form['telefone']
            atualizacao.CEP = request.form['CEP']
            atualizacao.endereco = request.form['endereco']
            atualizacao.cidade = request.form['cidade']
            atualizacao.bairro = request.form['bairro']
            atualizacao.UF = request.form['UF']
            nova_senha = request.form['senha']
            confirmacao_senha = request.form['senha2']
            form.UF.default = atualizacao.UF
            form.process()
            print("teste depois de salvar info")
            if nova_senha and confirmacao_senha:
                if nova_senha == confirmacao_senha:
                    atualizacao.senha_hash = generate_password_hash(nova_senha)
                else:
                    flash("As senhas não coincidem. Tente novamente.")
                    return render_template(
                        "atualizar_ong/atualizar_ong.html",
                        form=form,
                        atualizacao=atualizacao,
                        ongs=ongs                    
                    )
            try:
                db.session.commit()
                flash(f"ONG {atualizacao.nome} atualizada com sucesso")
                return redirect(url_for('ong_routes.perfil_ong', slug = current_user.slug))
            except:
                flash("Erro, tente novamente.")
                return render_template(
                    "atualizar_ong/atualizar_ong.html",
                    form=form,
                    atualizacao=atualizacao,
                    ongs=ongs                
                    )
    return render_template(
        "atualizar_ong/atualizar_ong.html",
        form=form,
        atualizacao=atualizacao,
        ongs=ongs
    )