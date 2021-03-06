from myapp import app
from flask import flash, jsonify, redirect, render_template, request, send_from_directory, url_for
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
import os
from os import listdir
from os.path import isfile, join
from PIL import Image
from flask_paginate import Pagination, get_page_args

list_images = []

onlyfiles = [f for f in listdir(app.config['UPLOAD_FOLDER']) if isfile(join(app.config['UPLOAD_FOLDER'], f))]
for each in onlyfiles:
    list_images.append(each)

class MyImage: # This represents your class
  def __init__(self, id, name):
    self.id = id
    self.name = name

def convert_to_list_objects(list_images):
  list_objects_images = []
  for index, each in enumerate(list_images):
    elemento = MyImage(index+1, each)
    list_objects_images.append(elemento)
  return list_objects_images

# Carrega a lista de objetos images
images = convert_to_list_objects(list_images)

# retorna a paginacao da lista de objetos images
def get_images(offset=0, per_page=10, images=images):
    return images[offset: offset + per_page]

def tnails(filename, filename_path, thumbnail_path):
    try:
        filename_complete = filename_path + '/' + filename
        print(filename_complete)
        image = Image.open(filename_complete)
        image.thumbnail((90,90))        
        new_thumbnail = thumbnail_path + '/' + filename
        image.save(new_thumbnail)
        print(f'{new_thumbnail} saved with success!')
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
            uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename_secure))
            tnails(filename_secure, app.config['UPLOAD_FOLDER'], app.config['UPLOAD_FOLDER_THUNBNAILS'])
            list_images.append(filename_secure)
            flash(f'Upload {filename_secure} accomplished with success!', category='success')
        except Exception as e:
            flash(f'Error in Upload - {e}', category='danger')

    return redirect(url_for('list_files_page', images=list_images))

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
        uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename_secure))
        tnails(filename_secure, app.config['UPLOAD_FOLDER'], app.config['UPLOAD_FOLDER_THUNBNAILS'])
        list_images.append(filename_secure)
        flash(f'Upload {filename_secure} accomplished with success!', category='success')
    except Exception as e:
        flash(f'Error in Upload - {e}', category='danger')
        return redirect(url_for('list_files_page', images=list_images))

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
        uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename_secure))
        filenameimage = filename_secure
        tnails(filename_secure, app.config['UPLOAD_FOLDER'], app.config['UPLOAD_FOLDER_THUNBNAILS'])
        list_images.append(filename_secure)
        msg = f'Upload {filename_secure} accomplished with success!'
    except Exception as e:
        #msg = f'Error in Upload - {e}'
        flash(f'Error in Upload - {e}', category='danger')
        return redirect(url_for('list_files_page', images=list_images))

    return jsonify({'htmlresponse': render_template('upload/response.html', msg=msg, filenameimage=filenameimage)})

@app.route('/uploads/<name>')
@login_required
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)

@app.route('/uploads/<int:id>/<filename>')
@login_required
def dowload_private_file(filename):
    return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'], current_user.get_id()), filename)

@app.route('/allimages')
@login_required
def list_files_page():
    images = list_images
    return render_template('upload/list_files.html', images=images)

@app.errorhandler(413)
def too_large(error):
    return "File is too large", 413

@app.route('/images')
@login_required
def pagination_list_files_page():
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    total = len(images)
    pagination_images = get_images(offset=offset, per_page=per_page, images=images)
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')
    return render_template('upload/pagination_list_files.html', images=pagination_images, page=page, per_page=per_page, pagination=pagination)
