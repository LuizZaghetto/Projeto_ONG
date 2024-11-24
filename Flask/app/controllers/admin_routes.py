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


# Atualizar usuário usando admin
@admin_routes_bp.route('/admin/atualizar_admin/<int:ID_usuario>', methods=['GET', 'POST'])
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
    
# # Deletar Usuário Admin
@admin_routes_bp.route("/admin/excluir/<int:ID_usuario>", methods=['POST'])
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