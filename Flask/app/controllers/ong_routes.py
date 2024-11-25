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

@ong_routes_bp.route("/perfil-<slug>", methods=['GET', 'POST'])
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
        "perfil_usuario/perfil_usuario.html", 
        form=form,
        ong = ong
    )