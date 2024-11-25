from flask import Flask
from flask_migrate import Migrate
from app.controllers.routes import routes_bp, auth_routes_bp, usuario_routes_bp, admin_routes_bp, ong_routes_bp
from app.extensions import db
import os
from dotenv import load_dotenv
import app.functions as func
from flask_login import LoginManager 
import app.models.models as models


# Carregar as variáveis do .env
load_dotenv()

# Acessar a chave secretaos.
secret_key = os.getenv("SECRET_KEY")

# Acessar os dados do banco de dados
# Banco Principal
database_user = os.getenv("DATABASE_USER")
database_host = os.getenv("DATABASE_HOST")
database_password = os.getenv("DATABASE_PASSWORD")
database_name = os.getenv("DATABASE_NAME")
# Banco Secundário
database2_user =os. getenv("DATABASE2_USER")
database2_host = os.getenv("DATABASE2_HOST")
database2_password = os.getenv("DATABASE2_PASSWORD")
database2_name = os.getenv("DATABASE2_NAME")

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

        # Pasta de migrações personalizada
        app.config['MIGRATION_DIR'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app', 'migrations')
        
        # Inicializar o SQLAlchemy com o app
        db.init_app(app)

        #Inicializar o Migrate com o app e db
        migrate = Migrate(app, db, directory=app.config['MIGRATION_DIR'])

        with app.app_context():
            db.create_all()
            # func.atualizar_dados_formatados()

        login_manager = LoginManager()
        login_manager.init_app(app)
        login_manager.login_view = 'auth_routes.login'
        
        @login_manager.user_loader
        def load_user(user_id):
            # Identifique o prefixo para determinar o tipo
            if user_id.startswith("usuario-"):
                user_id = user_id.replace("usuario-", "")
                usuario = models.Usuarios.query.get(int(user_id))
                if usuario:
                        print(f"Usuário carregado: {usuario.nome}, Tipo: {usuario.tipo}")
                return usuario
            elif user_id.startswith("ong-"):
                    user_id = user_id.replace("ong-", "")
                    ong = models.ONG.query.get(int(user_id))
                    if ong:
                        print(f"ONG carregada: {ong.nome}, Tipo: {ong.tipo}")
                        return ong
            print("Usuário não encontrado")
            return None



        # Registrar blueprints
        app.register_blueprint(routes_bp)
        app.register_blueprint(auth_routes_bp) 
        app.register_blueprint(usuario_routes_bp) 
        app.register_blueprint(admin_routes_bp)
        app.register_blueprint(ong_routes_bp) 

            
        return app
    except Exception as e:
        error_name = e.__class__.__name__
        if error_name in err.keys():
            print(err[error_name])



app = create_app()
if __name__ == "__main__":
    app = create_app()
    with app.app_context():  # Garante que estamos no contexto do app
        try:
            # Geração de usuários
            usuarios = func.criar_usuarios()
            func.adicionar_usuarios_ao_bd(usuarios)
            print("Usuários criados e adicionados com sucesso ao banco de dados.")
        except Exception as e:
            print(f"Erro ao criar usuários: {e}")

    # Inicia o servidor Flask
    app.run(debug=True)