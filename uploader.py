import os
from flask import Flask, flash, request, redirect, url_for, render_template
import werkzeug
from werkzeug.utils import secure_filename
from geo.Geoserver import Geoserver
import glob
from decouple import config

geo = Geoserver(config('GS_HOST'), username=config('GS_USERNAME'),
                password=config('GS_PASSWORD'))

UPLOAD_FOLDER = './rasters'
ALLOWED_EXTENSIONS = {'tif'}

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def store_exists(store_name, workspace = None):
    coverages_list = []
    response = False
    coverage_stores = geo.get_coveragestores(workspace)
    
    if type(coverage_stores) == 'str':
        return response

    if coverage_stores['coverageStores']:
        coverages_list = coverage_stores['coverageStores']['coverageStore']        
    if store_name in [coverage['name'] for coverage in coverages_list]:
        response = True
    
    return response

@app.route('/', methods=['GET'])
def form():
    workspaces = geo.get_workspaces()['workspaces']['workspace']
    ws = [workspace['name'] for workspace in  workspaces]
    return render_template("index.html", workspaces=ws)

@app.route('/', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('Erro ao receber o arquivo')
        return redirect(request.url)

    file = request.files['file']
    workspace_name = secure_filename(request.form["workspace"])

    if file.filename == '':
        flash('Nenhum arquivo selecionado!')
        return redirect(request.url)

    if file and not allowed_file(file.filename):
        flash('Arquivo inválido!')
        return redirect(request.url)

    store_name= secure_filename(file.filename)[:-4]
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    path = '/'.join([app.config['UPLOAD_FOLDER'],filename])
    
    if file and allowed_file(file.filename) and not store_exists(store_name, workspace_name):
        resultado = geo.create_coveragestore(
            path=path,
            workspace=workspace_name,
            layer_name=store_name,
            file_type="GeoTIFF",
            content_type="image/tiff",
        )
        print(path)
        os.remove(path)

        flash(f'O store "{store_name}" foi criado com sucesso no workspace "{workspace_name}"!')

        return render_template("success.html")

    flash(f'O store "{store_name}" já existe no workspace "{workspace_name}"!','warning')
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
