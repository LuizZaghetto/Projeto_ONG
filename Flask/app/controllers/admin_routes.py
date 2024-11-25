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

admin_routes_bp = Blueprint('admin_routes', __name__)

# Acessar crud temporário
@admin_routes_bp.route("/admin/crud")
def crud():
    usuarios = models.Usuarios.query.order_by(models.Usuarios.ID_usuario)
    ongs = models.ONG.query.order_by(models.ONG.ID_ONG)
    return render_template("crud/crud.html",
    usuarios = usuarios, ongs = ongs)

# Atualizar usuário pelo admin
@admin_routes_bp.route('/admin/atualizar_usuario_admin/<int:ID_usuario>', methods=['GET', 'POST'])
def atualizar_usuario_admin(ID_usuario):
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
            return render_template("atualizar_usuario_admin/atualizar_usuario_admin.html", 
            form = form,
            atualizacao = atualizacao,
            usuarios = usuarios)
        except:
            flash("Error")
            return render_template("atualizar_usuario_admin/atualizar_usuario_admin.html", 
            form = form,
            atualizacao = atualizacao,
            usuarios = usuarios)
    else:
        return render_template("atualizar_usuario_admin/atualizar_usuario_admin.html", 
        form = form,
        atualizacao = atualizacao,
        usuarios = usuarios)
    
 # Atualizar ONG pelo admin   
@admin_routes_bp.route('/admin/atualizar_ONG_admin/<int:ID_ONG>', methods=['GET', 'POST'])
def atualizar_ONG_admin(ID_ONG):
    form = forms.ONGregistroForm()
    ongs = models.ONG.query.order_by(models.ONG.ID_ONG)
    atualizacao = models.ONG.query.get_or_404(ID_ONG)
    if request.method == "POST":
        atualizacao.nome = request.form['nome']
        atualizacao.email = request.form['email']
        atualizacao.telefone = request.form['telefone']
        atualizacao.CEP = request.form['CEP']
        atualizacao.endereco = request.form['endereco']
        atualizacao.bairro = request.form['bairro']
        atualizacao.cidade = request.form['cidade']
        atualizacao.UF = request.form['UF']
        atualizacao.CNPJ = request.form['CNPJ']
        atualizacao.ID_ONG = request.form['ID_ONG']
        try:
            db.session.commit()
            flash(f"ONG {ID_ONG} atualizada com sucesso")
            return render_template("atualizar_ong_admin/atualizar_ong_admin.html", 
            form = form,
            atualizacao = atualizacao,
            ongs = ongs)
        except:
            flash("Error")
            return render_template("atualizar_ong_admin/atualizar_ong_admin.html", 
            form = form,
            atualizacao = atualizacao,
            ongs = ongs)
    else:
        return render_template("atualizar_ong_admin/atualizar_ong_admin.html", 
        form = form,
        atualizacao = atualizacao,
        ongs = ongs)
    
# Deletar Usuário Admin
@admin_routes_bp.route("/admin/excluir_usuário/<int:ID_usuario>", methods=['POST'])
def excluir_usuario_admin(ID_usuario):
    exclusao = models.Usuarios.query.get_or_404(ID_usuario)
    usuarios = models.Usuarios.query.order_by(models.Usuarios.ID_usuario)
    try:
        db.session.delete(exclusao)
        db.session.commit()
        flash(f"Usuario {exclusao.nome} deletado com sucesso")

        return redirect(url_for("admin_routes.crud"))
    except:
        flash("Houve um problema ao deletar o usuário")
        return redirect(url_for("admin_routes.crud"))
    
# Deletar ONG pelo Admin
@admin_routes_bp.route("/admin/excluirONG/<int:ID_ONG>", methods=['POST'])
def excluir_ONG_admin(ID_ONG):
    exclusao = models.ONG.query.get_or_404(ID_ONG)
    ongs = models.ONG.query.order_by(models.ONG.ID_ONG)
    try:
        db.session.delete(exclusao)
        db.session.commit()
        flash(f"Usuario {exclusao.nome} deletado com sucesso")

        return redirect(url_for("admin_routes.crud"))
    except:
        flash("Houve um problema ao deletar o usuário")
        return redirect(url_for("admin_routes.crud"))