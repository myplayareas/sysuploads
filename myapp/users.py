from myapp import app
from flask import redirect, render_template, request, url_for, flash
from flask_login import login_required
from myapp.dao import Users, User
from flask_paginate import Pagination, get_page_args
import pandas as pd
from myapp.forms import UserForm
from myapp.uploads import update_list_images

usersCollection = Users()
users = usersCollection.list_all_users()

def get_users(offset=0, per_page=10, users=users):
    return users[offset: offset + per_page]

@app.route('/users')
@login_required
def pagination_page():
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    usersCollection = Users()
    users = usersCollection.list_all_users()
    total = len(users)
    pagination_users = get_users(offset=offset, per_page=per_page, users=users)
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')
    return render_template('user/pagination.html', users=pagination_users, page=page, per_page=per_page, pagination=pagination)

@app.route('/edituser/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_user(id):
    form = UserForm()
    usuario_old = usersCollection.query_user_by_id(id)
    
    if request.method == 'GET':
        # Carrega form com os dados originais do usuario selecionado
        form.load_content(usuario_old.username, usuario_old.email_address)
        return render_template('user/edita_user.html', user=usuario_old, form=form)        
    
    if form.validate_on_submit():
        try:
            usersCollection.update_user(id, form.username.data, form.email_address.data)
            flash(f'User {form.username.data} updated with success!', category='success')
        except Exception as e:
            flash(f"Erro: {e}", category='danger')
        return redirect(url_for('pagination_page'))
    
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error to edit user: {err_msg}', category='danger')
    
    return render_template('user/edita_user.html', user=usuario_old, form=form)

@app.route('/loadusers')
@login_required
def load_users():
    users = usersCollection.list_all_users()
    try: 
        if (len(users) <= 1): 
            df_users = pd.read_csv('users.csv')
            for index, row in df_users.iterrows():
                user_to_create = User(username=row['username'], email_address=row['email_address'], password=row['password'])
                usersCollection.insert_user(user_to_create)
    except Exception as e:
        print(f'Erro popula_usuarios: {e}')
    return redirect(url_for('pagination_page'))

@app.route('/dashboard')
@login_required
def dashboard_page():
    usersCollection = Users()
    users = usersCollection.list_all_users()
    total_users = len(users)
    total_images = len(update_list_images())
    return render_template('user/dashboard.html', qtd_images=total_images)

@app.route('/dashboard/admin')
@login_required
def dashboard_admin_page():
    usersCollection = Users()
    users = usersCollection.list_all_users()
    total_users = len(users)
    total_images = len(update_list_images())
    return render_template('user/dashboard_admin.html', qtd_users=total_users, qtd_images=total_images)
