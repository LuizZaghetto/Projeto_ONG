from app.extensions import db
class Usuarios(db.Model):
    __tablename__ = 'pessoa'
    ID_usuario = db.Column(db.Integer, primary_key=True, nullable=False)
    nome = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    telefone = db.Column(db.String(20), nullable=False)
    data_nasc = db.Column(db.Date, nullable=False)
    CPF = db.Column(db.String(15), nullable=False, unique = True)
