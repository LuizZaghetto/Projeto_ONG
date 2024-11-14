from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, IntegerField, PasswordField
from wtforms.validators import DataRequired, Email, Length, Regexp, EqualTo

# Criar formulário para Registro
class registroForm(FlaskForm):
    ID_usuario = IntegerField("")
    nome = StringField("Nome de usuário", validators=[DataRequired()])
    email = StringField("Email", validators=[Email(message="Por favor, insira um email válido.")])
    data_nasc = DateField("Data de Nascimento", format='%Y-%m-%d', validators=[DataRequired(), ])
    CPF = StringField("CPF",  validators=[DataRequired(), Regexp(r'^\d{3}\.\d{3}\.\d{3}-\d{2}$', message="O CPF deve estar no formato XXX.XXX.XXX-XX.")])
    telefone = StringField("Número de Telefone", validators=[DataRequired(), Regexp(r'^\(\d{2}\)\s\d{5}-\d{4}$', message="Telefone deve estar no formato (XX) XXXXX-XXXX.")])
    senha_hash = PasswordField("Digite sua senha", validators=[DataRequired(), EqualTo('senha_hash2', message = "As senhas devem ser iguais")])
    senha_hash2 = PasswordField("Confirme a senha", validators=[DataRequired()])
    enviar = SubmitField("Enviar")


# Criar formulário para Login
class loginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])   
    senha_hash = PasswordField("Senha", validators=[DataRequired()])
    enviar = SubmitField("Enviar")   