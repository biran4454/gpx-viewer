from flask import Flask, render_template, request
import main

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/map')
def map_view():
    try:
        return render_template('map.html')
    except:
        return render_template('nomap.html')

@app.route('/scan', methods=['POST'])
def scan():
    try:
        main.main()
    except:
        return 'Error', 500
    return 'OK'

@app.route('/regen', methods=['POST'])
def regen():
    try:
        main.clear_cache()
        main.main()
    except:
        return 'Error', 500
    return 'OK'

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        files = request.files.getlist('files')
        for file in files:
            file.save(f'data/GPX/{file.filename}')
        return render_template('success.html')
    return render_template('upload.html')