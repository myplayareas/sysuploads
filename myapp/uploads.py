from myapp import app
from flask import flash, jsonify, redirect, render_template, request, send_from_directory, url_for
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
import os
from os import listdir
from os.path import isfile, join
from PIL import Image
from flask_paginate import Pagination, get_page_args
from myapp.dao import User, File, Users, Files

usersCollection = Users()
filesCollection = Files()

class MyImage: # This represents your class
  def __init__(self, id, name):
    self.id = id
    self.name = name

def user_directory(path_temp, user_id):
    user_path = path_temp + '/' + str(user_id)

    if os.path.exists(user_path):
        return user_path
    else: 
        os.makedirs(user_path)
    return user_path 

# Carrega uma lista atualzada com os nomes dos arquivos da pasta UPLOAD_FOLDER
def update_list_images():
    path_user_images = user_directory(app.config['UPLOAD_FOLDER'], current_user.get_id())
    list_images = []
    onlyfiles = [f for f in listdir(path_user_images) if isfile(join(path_user_images, f))]
    for each in onlyfiles:
        list_images.append(each)
    return list_images

# Converte lista de nomes de arquivos em lista de objetos MyImage
def convert_to_list_objects(list_images):
  list_objects_images = []
  for index, each in enumerate(list_images):
    elemento = MyImage(index+1, each)
    list_objects_images.append(elemento)
  return list_objects_images

# retorna a paginacao da lista de objetos images
def get_images(offset=0, per_page=10, images=None):
    return images[offset: offset + per_page]

# dado um arquivo cria o thumbnail correspondente e salva na pasta de thumbnails
def tnails(filename, filename_path, thumbnail_path):
    try:
        filename_complete = filename_path + '/' + filename
        image = Image.open(filename_complete)
        image.thumbnail((90,90))        
        new_thumbnail = thumbnail_path + '/' + filename
        image.save(new_thumbnail)
    except IOError as io:
        raise Exception(f'Erro - {io}')

@app.route('/uploads', methods=['GET', 'POST'])
@login_required
def upload_page():
    # Carrega o form de upload
    if request.method == 'GET':
        return render_template('upload/upload.html')
    
    # Faz o upload do arquivo
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        try: 
            filename_secure = secure_filename(uploaded_file.filename)
            path_to_save_image = user_directory(app.config['UPLOAD_FOLDER'], current_user.get_id())
            uploaded_file.save(os.path.join(path_to_save_image, filename_secure))
            file_to_save = File(name=filename_secure)
            filesCollection.insert_file(file_to_save)
            path_to_save_image_thumbnail = user_directory(app.config['UPLOAD_FOLDER_THUMBNAILS'], current_user.get_id())
            tnails(filename_secure, path_to_save_image, path_to_save_image_thumbnail)
            usersCollection.link_to_file(user_id=current_user.get_id(), file=file_to_save)
            flash(f'Upload {filename_secure} accomplished with success!', category='success')
        except Exception as e:
            flash(f'Error in Upload - {e}', category='danger')

    return redirect(url_for('list_files_page'))

@app.route('/uploadsprogress', methods=['GET'])
@login_required
def load_upload_progress_page():
    return render_template('upload/upload_progress.html')

@app.route('/uploadsprogress', methods=['POST'])
@login_required
def upload_progress():    
    # Faz o upload do arquivo
    uploaded_file = request.files['file']
    try: 
        filename_secure = secure_filename(uploaded_file.filename)
        path_to_save_image = user_directory(app.config['UPLOAD_FOLDER'], current_user.get_id())
        uploaded_file.save(os.path.join(path_to_save_image, filename_secure))
        file_to_save = File(name=filename_secure)
        filesCollection.insert_file(file_to_save)
        path_to_save_image_thumbnail = user_directory(app.config['UPLOAD_FOLDER_THUMBNAILS'], current_user.get_id())
        tnails(filename_secure, path_to_save_image, path_to_save_image_thumbnail)
        usersCollection.link_to_file(user_id=current_user.get_id(), file=file_to_save)
        flash(f'Upload {filename_secure} accomplished with success!', category='success')
    except Exception as e:
        flash(f'Error in Upload - {e}', category='danger')
        return redirect(url_for('list_files_page'))

    return '', 204

@app.route('/uploadsclassicprogress', methods=['GET'])
@login_required
def load_upload_classic_progress_page():
    return render_template('upload/upload_classic_progress.html')

@app.route('/uploadsclassicprogress', methods=['POST'])
@login_required
def upload_classic_progress():    
    # Faz o upload do arquivo
    uploaded_file = request.files['uploadFile']
    try: 
        filename_secure = secure_filename(uploaded_file.filename)
        path_to_save_image = user_directory(app.config['UPLOAD_FOLDER'], current_user.get_id())
        uploaded_file.save(os.path.join(path_to_save_image, filename_secure))
        filenameimage = filename_secure
        file_to_save = File(name=filename_secure)
        filesCollection.insert_file(file_to_save)
        path_to_save_image_thumbnail = user_directory(app.config['UPLOAD_FOLDER_THUMBNAILS'], current_user.get_id())
        tnails(filename_secure, path_to_save_image, path_to_save_image_thumbnail)
        usersCollection.link_to_file(user_id=current_user.get_id(), file=file_to_save)
        msg = f'Upload {filename_secure} accomplished with success!'
    except Exception as e:
        flash(f'Error in Upload - {e}', category='danger')
        return redirect(url_for('list_files_page'))

    return jsonify({'htmlresponse': render_template('upload/response.html', msg=msg, filenameimage=filenameimage)})

@app.route('/uploads/<int:id>/<name>')
@login_required
def download_file(id, name):
    path_to_save_image = user_directory(app.config['UPLOAD_FOLDER'], str(id))
    return send_from_directory(path_to_save_image, name)

@app.route('/uploads/<int:id>/<filename>')
@login_required
def dowload_private_file(filename):
    return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'], current_user.get_id()), filename)

@app.route('/allimages')
@login_required
def list_files_page():
    # Carrega a lista de objetos images
    images = convert_to_list_objects(update_list_images())
    return render_template('upload/list_files.html', images=images)

@app.errorhandler(413)
def too_large(error):
    return "File is too large", 413

@app.route('/images')
@login_required
def pagination_list_files_page():
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    # Carrega a lista de objetos images
    images = convert_to_list_objects(update_list_images())

    total = len(images)
    pagination_images = get_images(offset=offset, per_page=per_page, images=images)
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')
    return render_template('upload/pagination_list_files.html', images=pagination_images, page=page, per_page=per_page, pagination=pagination)

@app.route("/deleteimage/<int:id>/<name>")
@login_required
def delete_image(id, name):

    path_saved_image = user_directory(app.config['UPLOAD_FOLDER'], id)
    path_saved_image_thumbnail = user_directory(app.config['UPLOAD_FOLDER_THUMBNAILS'], id)
    
    image_name_uploads = path_saved_image +  '/' + name
    image_name_thubnails = path_saved_image_thumbnail + '/' + name

    if os.path.exists(image_name_uploads):
        try:
            os.remove(image_name_uploads)
            os.remove(image_name_thubnails)
            file_to_delete = filesCollection.query_file_by_name(name)
            usersCollection.unlink_file(user_id=current_user.get_id(), file=file_to_delete)
            filesCollection.delete_file(file_to_delete)
            flash(f'{name} deleted successfully!', category='success')
        except Exception as e:
            flash(f'Error {e} during deletion of {name}!', category='danger')
    else:
        flash(f'The file {name} does not exist!', category='danger')        
    return redirect(url_for('pagination_list_files_page'))