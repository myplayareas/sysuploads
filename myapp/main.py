from myapp import app
from flask import render_template
from flask_login import login_required
from myapp.dao import Users

@app.route('/myapp')
@login_required
def myapp_page():
    usersCollection = Users()
    users = usersCollection.list_all_users()
    return render_template('user/myapp.html', users=users)