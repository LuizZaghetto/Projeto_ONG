from flask import render_template, Blueprint, redirect, url_for, flash, abort, request
from werkzeug.security import generate_password_hash, check_password_hash
import app.forms.forms as forms 
from flask_sqlalchemy import SQLAlchemy
import app.models.models as models
from app.extensions import db
from datetime import datetime
import app.functions as func
from flask_login import login_user, login_required, logout_user, current_user
from app.controllers.auth_routes import auth_routes_bp

routes_bp = Blueprint('routes', __name__)

routes_bp.register_blueprint(auth_routes_bp)



# Página inicial
@routes_bp.route("/", methods=['GET', 'POST'])
def landing_page():
    return render_template("landing_page/index.html")

# Criar interface de usuário
@routes_bp.route("/interface_logado", methods=['GET','POST'])
@login_required
def interface_logado():
    print('test')
    print(request)
    form = forms.bichoForm()
    return render_template("interface_logado/interface_logado.html", form = form)


# Atualizar usuário
@routes_bp.route('/admin/atualizar/<int:ID_usuario>', methods=['GET', 'POST'])
def atualizar(ID_usuario):
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
            flash("Usuário adicionado com sucesso")
            return render_template("atualizar/atualizar.html", 
            form = form,
            atualizacao = atualizacao,
            usuarios = usuarios)
        except:
            flash("Error")
            return render_template("atualizar/atualizar.html", 
            form = form,
            atualizacao = atualizacao,
            usuarios = usuarios)
    else:
        return render_template("atualizar/atualizar.html", 
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



# Lidar com erros
# Invalid URL
@routes_bp.app_errorhandler(404)
def page_not_found(e):
    return render_template("erro/erro.html", erro = 404), 404

#Internal Server Error 
@routes_bp.app_errorhandler(500)
def page_not_found(e):
    return render_template("erro/erro.html", erro = 500), 500
