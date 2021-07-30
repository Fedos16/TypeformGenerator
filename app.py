from flask import Flask, render_template, jsonify, request
import pandas as pd
import os
import create_form

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/data', methods=['GET', 'POST'])
def data():
    if request.method == 'POST':
        file = request.files['upload-file']
        if file:
            filename = file.filename
            res = filename.split('.')[-1]
            # do something with file contents
            file.save(os.path.join('uploads', f'file.{res}'))
            return render_template('data.html', status="Файл загружен")
        else:
            return render_template('data.html', status="Файл не загружен")

@app.route('/setform', methods=['POST'])
def setform():
    status_create_form = create_form.setForm()
    return jsonify(ok = status_create_form)

if __name__ == "__main__":
    app.run(debug=True)