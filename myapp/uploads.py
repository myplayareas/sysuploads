from crypt import methods
from myapp import app
from flask import flash, redirect, render_template, request, send_from_directory, url_for
from flask_login import login_required
from werkzeug.utils import secure_filename
import os
from os import listdir
from os.path import isfile, join

from PIL import Image

list_images = []

onlyfiles = [f for f in listdir(app.config['UPLOAD_FOLDER']) if isfile(join(app.config['UPLOAD_FOLDER'], f))]
for each in onlyfiles:
    list_images.append(each)

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

@app.route('/uploads/<name>')
@login_required
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)

@app.route('/images')
@login_required
def list_files_page():
    images = list_images
    return render_template('upload/list_files.html', images=images)


