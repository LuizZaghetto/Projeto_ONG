from app.extensions import db
class Usuarios(db.Model):
    __tablename__ = 'pessoa'
    
    ID_usuario = db.Column(db.Integer, primary_key=True, nullable=False)
    nome = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    telefone = db.Column(db.String(20), nullable=False)
    data_nasc = db.Column(db.Date, nullable=False)
    CPF = db.Column(db.String(15), nullable=False, unique=True)

    bichos = db.relationship('Bichos', backref='usuario', lazy='select')
    adocoes = db.relationship('Adocao', backref='adocoes_usuario', lazy='select')  # Alterado para 'adocoes_usuario'

class Bichos(db.Model):
    __tablename__ = "bicho"
    
    ID_bicho = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False)
    especie = db.Column(db.String(20), nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    porte = db.Column(db.String(10), nullable=False)
    descricao = db.Column(db.String(500), nullable=True)

    # Relacionamentos
    ID_usuario = db.Column(db.Integer, db.ForeignKey('pessoa.ID_usuario', ondelete='SET NULL'))
    ID_ONG = db.Column(db.Integer, db.ForeignKey('ong.ID_ONG', ondelete='CASCADE'))

    def __repr__(self):
        return f"<Bicho {self.nome}, {self.especie}>"
    
class ONG(db.Model):
    __tablename__ = 'ong'

    ID_ONG = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    telefone = db.Column(db.String(20), nullable=False)
    endereco = db.Column(db.String(100), nullable=False)
    bairro = db.Column(db.String(30), nullable=False)
    cidade = db.Column(db.String(30), nullable=False)
    UF = db.Column(db.String(2), nullable=False)
    CNPJ = db.Column(db.String(15), nullable=False, unique=True)

    # Relacionamento com Bicho
    bichos = db.relationship('Bichos', backref='ong', lazy=True)  # Alterei para 'Bichos' ao invés de 'Bicho'

    def __repr__(self):
        return f"<ONG {self.nome}, {self.CNPJ}>"
        
class Adocao(db.Model):
    __tablename__ = 'adocao'

    ID_adocao = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ID_bicho = db.Column(db.Integer, db.ForeignKey('bicho.ID_bicho'), nullable=False)
    ID_usuario = db.Column(db.Integer, db.ForeignKey('pessoa.ID_usuario'), nullable=False)  
    Data_Adocao = db.Column(db.Date, nullable=False)

    # Relacionamentos
    bicho = db.relationship('Bichos', backref='adocoes_bicho', lazy=True)  # Alterei para 'adocoes_bicho'
    usuario = db.relationship('Usuarios', backref='adocoes_usuario', lazy=True)  # Alterei para 'adocoes_usuario'

    def __repr__(self):
        return f"<Adocao ID={self.ID_adocao}, Bicho={self.ID_bicho}, Usuario={self.ID_usuario}, Data={self.Data_Adocao}>"
