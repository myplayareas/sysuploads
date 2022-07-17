from myapp import db, login_manager
from myapp import my_bcrypt
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = my_bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return my_bcrypt.check_password_hash(self.password_hash, attempted_password)

class Users:
    def insert_user(self, user):
        try:
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            print(f'Error during insert user - {e}')

    def query_user_by_username(self, p_username):
        user = User.query.filter_by(username=p_username).first()
        return user
    def query_user_by_id(self, p_id):
        user = User.query.filter_by(id=p_id).first()
        return user
    
    def list_all_users(self):
        return User.query.all()

    def update_user(self, id, username, email):
        try:
            user_to_update = self.query_user_by_id(id)
            user_to_update.username = username
            user_to_update.email_address = email
            db.session.commit()
        except Exception as e:
            raise Exception(f'Error during update user - {e}')