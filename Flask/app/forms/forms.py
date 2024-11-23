from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, IntegerField, PasswordField
from wtforms.validators import DataRequired, Email, Length, Regexp, EqualTo, Optional

# Criar formulário para Registro
class registroForm(FlaskForm):
    ID_usuario = IntegerField("")
    nome = StringField("Nome de usuário", validators=[DataRequired()])
    email = StringField("Email", validators=[Email(message="Por favor, insira um email válido.")])
    data_nasc = DateField("Data de Nascimento", format='%Y-%m-%d', validators=[DataRequired(), ])
    CPF = StringField("CPF",  validators=[DataRequired(), Regexp(r'^\d{3}\.\d{3}\.\d{3}-\d{2}$', message="O CPF deve estar no formato XXX.XXX.XXX-XX.")])
    telefone = StringField("Número de Telefone", validators=[DataRequired(), Regexp(r'^\(\d{2}\)\s\d{5}-\d{4}$', message="Telefone deve estar no formato (XX) XXXXX-XXXX.")])
    senha = PasswordField("Digite sua senha", validators=[DataRequired(), EqualTo('senha2', message = "As senhas devem ser iguais")])
    senha2 = PasswordField("Confirme a senha", validators=[DataRequired()])
    enviar = SubmitField("Enviar")


# Criar formulário para Login
class loginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])   
    senha = PasswordField("Senha", validators=[DataRequired()])
    enviar = SubmitField("Enviar")   

class registroONGForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    telefone = StringField('Telefone', validators=[DataRequired()])
    CEP = StringField('CEP', validators=[DataRequired()])
    endereco = StringField('Endereço', validators=[DataRequired()])
    bairro = StringField('Bairro', validators=[DataRequired()])
    cidade = StringField('Cidade', validators=[DataRequired()])
    UF = StringField('UF', validators=[DataRequired()])
    CNPJ = StringField('CNPJ', validators=[DataRequired()])
    senha = PasswordField("Digite sua senha", validators=[DataRequired(), EqualTo('senha2', message = "As senhas devem ser iguais")])
    senha2 = PasswordField("Confirme a senha", validators=[DataRequired()])
    enviar = SubmitField('Registrar')

# Criar formulário para adicionar Bicho
class bichoForm(FlaskForm):
    nome = StringField("Nome do Bicho", validators=[DataRequired()])
    porte = StringField("Porte do Bicho", validators=[DataRequired()])
    enviar = SubmitField("Enviar")

# Criar formulário para atualizar usuário
class AtualizarUsuarioForm(FlaskForm):
    nome = StringField("Nome de usuário", validators=[DataRequired()])
    email = StringField("Email", validators=[Email(message="Por favor, insira um email válido.")])
    data_nasc = DateField("Data de Nascimento", format='%Y-%m-%d', validators=[DataRequired()])
    CPF = StringField("CPF", validators=[DataRequired(), Regexp(r'^\d{3}\.\d{3}\.\d{3}-\d{2}$', message="O CPF deve estar no formato XXX.XXX.XXX-XX.")])
    telefone = StringField("Número de Telefone", validators=[DataRequired(), Regexp(r'^\(\d{2}\)\s\d{5}-\d{4}$', message="Telefone deve estar no formato (XX) XXXXX-XXXX.")])
    senha_atual = PasswordField("Senha Atual", validators=[DataRequired()])  # Sempre obrigatório
    senha = PasswordField("Nova senha", validators=[Optional(), EqualTo('senha2', message="As senhas devem ser iguais")])
    senha2 = PasswordField("Confirme a nova senha", validators=[Optional()])
    enviar = SubmitField("Atualizar")
