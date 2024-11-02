from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length


# Criar formulário para Registro
class registroForm(FlaskForm):
    nome = StringField("Nome de usuário", validators=[DataRequired()])
    email = StringField("Email", validators=[Email()])
    data_nasc = StringField("Data de Nascimento", validators=[DataRequired()])
    CPF = StringField("CPF", validators=[DataRequired()])
    telefone = StringField("Número de Telefone", validators=[DataRequired()])
    # senha = StringField("Senha", validators=[DataRequired(), Length(min=8, max=20)])
    ID_usuario = StringField("ID do usuário")
    enviar = SubmitField("Enviar")

# Criar formulário para Login
class loginForm(FlaskForm):
    nome = StringField("Nome de usuário", validators=[DataRequired()])   
    enviar = SubmitField("Enviar")   