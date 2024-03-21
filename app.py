from flask import Flask, render_template, request
import main
import os

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
async def scan():
    await main.main()
    return 'OK'

@app.route('/regen', methods=['POST'])
async def regen():
    main.delete_map()
    main.clear_cache()
    await main.main()
    return 'OK'

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        files = request.files.getlist('files')
        for file in files:
            if not os.path.exists('data/GPX'):
                os.makedirs('data/GPX')
            file.save(f'data/GPX/{file.filename}')
        return render_template('success.html')
    return render_template('upload.html')