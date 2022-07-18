from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# Instancia principal da aplicacao (app)
app = Flask(__name__)

# Nome do arquivo de banco de dados sqlite
data_base = 'myapp.db'

MAIN_PATH = '/Users/armandosoaressousa/git'
UPLOAD_FOLDER = MAIN_PATH + '/sysuploads/myapp/static/uploads'
UPLOAD_FOLDER_THUMBNAILS = MAIN_PATH + '/sysuploads/myapp/static/uploads/thumbnails'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# Configuracoes da instancia principal da aplicacao
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + data_base
app.config['SECRET_KEY'] = 'ec9439cfc6c796ae2029594d'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_FOLDER_THUNBNAILS'] = UPLOAD_FOLDER_THUMBNAILS
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS
app.config['MAX_CONTENT_LENGTH'] = 5 * 1000 * 1000

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
from myapp import uploads