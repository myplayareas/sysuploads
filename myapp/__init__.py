from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# Instancia principal da aplicacao (app)
app = Flask(__name__)

# Nome do arquivo de banco de dados sqlite
data_base = 'myapp.db'

# Configuracoes da instancia principal da aplicacao
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + data_base
app.config['SECRET_KEY'] = 'ec9439cfc6c796ae2029594d'

# Cria a instancia ORM de banco de dados e associa aplicacao (app)
db = SQLAlchemy(app)

# Cria a instancia de Criptografia da aplicacao (app)
my_bcrypt = Bcrypt(app)

# Cria a instancia de LoginManager para gerenciar a sessao do usuario logado
login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"

# Importa os demais modulos da aplicacao
from myapp.dao import User, Users
from myapp import main
from myapp import authentication
from myapp import users