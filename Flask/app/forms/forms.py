from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, IntegerField, PasswordField, SelectField, TextAreaField, FileField
from wtforms.validators import DataRequired, Email, Length, Regexp, EqualTo, Optional, NumberRange
from flask_wtf.file import FileAllowed
from .estados import ESTADOS_BRASIL

# Formulários para registro
# Registro de usuário
class registroForm(FlaskForm):
    ID_usuario = IntegerField("ID de usuário")
    nome = StringField("Nome de usuário", validators=[DataRequired()])
    email = StringField("Email", validators=[Email(message="Por favor, insira um email válido.")])
    data_nasc = DateField("Data de Nascimento", format='%Y-%m-%d', validators=[DataRequired(), ])
    CPF = StringField("CPF",  validators=[DataRequired(), Regexp(r'^\d{3}\.\d{3}\.\d{3}-\d{2}$', message="O CPF deve estar no formato XXX.XXX.XXX-XX.")])
    telefone = StringField("Número de Telefone", validators=[DataRequired(), Regexp(r'^\(\d{2}\)\s\d{5}-\d{4}$', message="Telefone deve estar no formato (XX) XXXXX-XXXX.")])
    senha = PasswordField("Digite sua senha", validators=[DataRequired(), EqualTo('senha2', message = "As senhas devem ser iguais")])
    senha2 = PasswordField("Confirme a senha", validators=[DataRequired()])
    avatar = FileField("Avatar", validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'], message="Somente imagens são permitidas."), DataRequired(message="O avatar é obrigatório.")])
    enviar = SubmitField("Registrar")

# Registro de ONG
class ONGregistroForm(FlaskForm):
    ID_ONG = IntegerField("ID de ONG")
    nome = StringField('Nome', validators=[DataRequired()])
    email = StringField("Email", validators=[Email(message="Por favor, insira um email válido.")])
    telefone = StringField("Número de Telefone", validators=[DataRequired(), Regexp(r'^\(\d{2}\)\s\d{5}-\d{4}$', message="Telefone deve estar no formato (XX) XXXXX-XXXX.")])
    CEP = StringField('CEP', validators=[DataRequired(), Regexp(r'^\d{5}-\d{3}$', message="CEP deve estar no formato XXXXX-XXX.")])
    endereco = StringField('Endereço', validators=[DataRequired()])
    bairro = StringField('Bairro', validators=[DataRequired()])
    cidade = StringField('Cidade', validators=[DataRequired()])
    UF = SelectField(
        'UF', 
        choices=ESTADOS_BRASIL, 
        validators=[DataRequired()],
        default=''
    )
    CNPJ = StringField('CNPJ', validators=[DataRequired(), Regexp(r'^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$', message="CNPJ deve estar no formato XX.XXX.XXX/XXXX-XX.")])
    senha = PasswordField("Digite sua senha", validators=[DataRequired(), EqualTo('senha2', message = "As senhas devem ser iguais")])
    senha2 = PasswordField("Confirme a senha", validators=[DataRequired()])
    enviar = SubmitField('Registrar')

# Formulários para login
# Login de Usuário
class loginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])   
    senha = PasswordField("Senha", validators=[DataRequired()])
    enviar = SubmitField("Enviar")   

# Login de ONG
class ONGloginForm(FlaskForm):
    email = StringField("Email", validators=([DataRequired()]))
    senha = PasswordField("Senha", validators=([DataRequired()]))
    enviar = SubmitField("Enviar")


# Criar formulário para adicionar Bicho
class BichoForm(FlaskForm):
    nome = StringField("Nome", validators=[DataRequired(), Length(max=50, message="O nome deve ter no máximo 50 caracteres.")])
    especie = SelectField("Espécie", choices=[('Cachorro', 'Cachorro'), ('Gato', 'Gato')], validators=[DataRequired()])
    idade = IntegerField("Idade", validators=[DataRequired(),  NumberRange(min=0, max=50, message="A idade deve estar entre 0 e 50.")])
    sexo = SelectField("Sexo", choices=[('Feminino', 'Feminino'), ('Masculino', 'Masculino')], validators = [DataRequired()])
    porte = SelectField("Porte", choices=[('Pequeno', 'Pequeno'), ('Médio', 'Médio'), ('Grande', 'Grande')], validators=[DataRequired()])
    descricao = TextAreaField("Descrição", validators=[Optional(), Length(max=500, message="A descrição deve ter no máximo 500 caracteres.")])
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

# Criar formulário para atualizar ONG
class AtualizarONGForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    email = StringField("Email", validators=[Email(message="Por favor, insira um email válido.")])
    telefone = StringField("Número de Telefone", validators=[DataRequired(), Regexp(r'^\(\d{2}\)\s\d{5}-\d{4}$', message="Telefone deve estar no formato (XX) XXXXX-XXXX.")])
    CEP = StringField('CEP', validators=[DataRequired(), Regexp(r'^\d{5}-\d{3}$', message="CEP deve estar no formato XXXXX-XXX.")])
    endereco = StringField('Endereço', validators=[DataRequired()])
    bairro = StringField('Bairro', validators=[DataRequired()])
    cidade = StringField('Cidade', validators=[DataRequired()])
    UF = SelectField(
        'UF', 
        choices=ESTADOS_BRASIL, 
        validators=[DataRequired()],
        default=''
    )
    senha_atual = PasswordField("Senha Atual", validators=[DataRequired()])  
    senha = PasswordField("Nova senha", validators=[Optional(), EqualTo('senha2', message="As senhas devem ser iguais")])
    senha2 = PasswordField("Confirme a nova senha", validators=[Optional()])
    enviar = SubmitField('Atualizar')
