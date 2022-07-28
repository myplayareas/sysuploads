from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os

# Instancia principal da aplicacao (app)
app = Flask(__name__)

# Nome do arquivo de banco de dados sqlite
data_base = 'myapp.db'

MAIN_PATH = os.path.abspath(os.getcwd())
UPLOAD_FOLDER = MAIN_PATH + '/myapp/static/uploads'
UPLOAD_FOLDER_THUMBNAILS = MAIN_PATH + '/myapp/static/uploads/thumbnails'
UPLOAD_FOLDER_QRCODES = MAIN_PATH + '/myapp/static/uploads/qrcodes'
PATH_MYAPP = MAIN_PATH + '/myapp'
PATH_STATIC = MAIN_PATH + '/myapp/static'
PATH_IMG = MAIN_PATH + '/myapp/static/img'

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

MY_IP = '172.20.10.3'

# Configuracoes da instancia principal da aplicacao
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + data_base
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'ec9439cfc6c796ae2029594d'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_FOLDER_THUMBNAILS'] = UPLOAD_FOLDER_THUMBNAILS
app.config['UPLOAD_FOLDER_QRCODES'] = UPLOAD_FOLDER_QRCODES
app.config['PATH_MYAPP'] = PATH_MYAPP
app.config['PATH_STATIC'] = PATH_STATIC
app.config['PATH_IMG'] = PATH_IMG

app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS
app.config['MAX_CONTENT_LENGTH'] = 5 * 1000 * 1000

app.config['MY_IP'] = MY_IP

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
from myapp import errors
from myapp import utils

# To run when app starts
#from myapp import tests