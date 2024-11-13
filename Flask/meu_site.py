from flask import Flask
from app.controllers.routes import routes_bp
from app.extensions import db
from os import getenv
from dotenv import load_dotenv

# Carregar as variáveis do .env
load_dotenv()

# Acessar a chave secreta
secret_key = getenv("SECRET_KEY")

# Acessar os dados do banco de dados
# Banco Principal
database_user = getenv("DATABASE_USER")
database_host = getenv("DATABASE_HOST")
database_password = getenv("DATABASE_PASSWORD")
database_name = getenv("DATABASE_NAME")
# Banco Secundário
database2_user = getenv("DATABASE2_USER")
database2_host = getenv("DATABASE2_HOST")
database2_password = getenv("DATABASE2_PASSWORD")
database2_name = getenv("DATABASE2_NAME")

err = {
    'OperationalError': 'Erro ao conectar ao banco de dados.',
    'KeyError': 'Variável de ambiente ausente.',
    'FileNotFoundError': 'Arquivo de configuração não encontrado.',
    'ValueError': 'Valor inválido fornecido.',
    'RuntimeError': 'Erro de contexto de aplicação.',
}

def create_app():
    try:
        app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
        
        # Configuração da chave secreta e do banco de dados
        app.config['SECRET_KEY'] = secret_key
        app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{database_user}:{database_password}@{database_host}/{database_name}"
        #app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{database2_user}:{database2_password}@{database2_host}/{database2_name}"
        
        # Inicializar o SQLAlchemy com o app
        db.init_app(app)

        with app.app_context():
            db.create_all()
        
        # Registrar blueprints
        app.register_blueprint(routes_bp)
            
        return app
    except Exception as e:
        error_name = e.__class__.__name__
        if error_name in err.keys():
            print(err[error_name])



app = create_app()
if __name__ == "__main__": 
    app.run(debug = True)