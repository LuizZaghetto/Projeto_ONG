from flask import render_template, Blueprint, redirect, url_for, flash, abort, request
from werkzeug.security import generate_password_hash, check_password_hash
import app.forms.forms as forms 
from flask_sqlalchemy import SQLAlchemy
import app.models.models as models
from app.extensions import db
from datetime import datetime
import app.functions as func
from flask_login import login_user, login_required, logout_user, current_user

routes_bp = Blueprint('routes', __name__)

# Carregando header e footer
@routes_bp.route('/header')
def serve_header():
    return render_template('header/header.html') 

@routes_bp.route('/footer')
def serve_footer():
    return render_template('footer/footer.html')

# Página inicial
@routes_bp.route("/")
def landing_page():
    return render_template("landing_page/index.html")

# Página de login
@routes_bp.route("/login", methods=['GET', 'POST'])
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
@routes_bp.route("/logout", methods = ["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for('routes.landing_page'))

# Página de registro
@routes_bp.route("/registro", methods=['GET', 'POST'])
def registro():
    form = forms.registroForm()
    if form.validate_on_submit():
        usuario = models.Usuarios.query.filter_by(email = form.email.data).first()
        if usuario is None:
            try: 

                # Formatar CPF e Telefone no backend
                cpf_formatado = func.formatar_cpf(form.CPF.data)
                telefone_formatado = func.formatar_telefone(form.telefone.data)
                # Aplicando hash a senha
                senha_hashed = generate_password_hash(form.senha.data)
                usuario = models.Usuarios(
                    nome = form.nome.data, 
                    email = form.email.data,
                    telefone = form.telefone.data,
                    data_nasc = form.data_nasc.data.strftime('%Y-%m-%d'),                
                    CPF = form.CPF.data,
                    senha_hash = senha_hashed
                )
                db.session.add(usuario)
                db.session.commit()
                form.nome.data = ''
                form.email.data = ''
                form.telefone.data = ''
                form.data_nasc.data = ''
                form.CPF.data = ''
                flash("Registro realizado com sucesso!", "success")
                return redirect(url_for("routes.login"))
            except Exception as e:
                db.session.rollback()
                flash(f"Erro ao registrar o usuário: {e}", "danger")
        else:
            flash("Esse e-mail já está registrado.", "warning")        
    return render_template('registro/registro.html', form=form)

# Criar interface de usuário
@routes_bp.route("/interface_logado")
@login_required
def interface_logado():
    return render_template("interface_logado/interface_logado.html")

# Acessar crud temporário
@routes_bp.route("/admin/crud")
def crud():
    usuarios = models.Usuarios.query.order_by(models.Usuarios.ID_usuario)
    return render_template("crud/crud.html",
    usuarios = usuarios)

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
@routes_bp.route("/admin/excluir/<int:ID_usuario>")
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

# Acessar página de usuário
@routes_bp.route("/usuarios")
def usuarios():
    return render_template("usuarios/index.html")

# Acessar o perfil do bicho
@routes_bp.route("/perfil_bicho/<nome_bicho>")
def perfil_bicho(nome_bicho):
    return render_template("perfil_bicho/index.html", nome_bicho=nome_bicho)


# Lidar com erros
# Invalid URL
@routes_bp.app_errorhandler(404)
def page_not_found(e):
    return render_template("erro/erro.html", erro = 404), 404

#Internal Server Error 
@routes_bp.app_errorhandler(500)
def page_not_found(e):
    return render_template("erro/erro.html", erro = 500), 500

