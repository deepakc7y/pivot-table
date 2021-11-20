import os
import io
from pivottablejs import pivot_ui
import pandas as pd
import requests
import numpy as np
from flask import Flask, flash, request, redirect, render_template,session
from werkzeug.utils import secure_filename

app=Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['UPLOAD_EXTENSIONS'] = ['.csv']
BASE = "http://127.0.0.1:5000/"

base_dir = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(base_dir,app.config['UPLOAD_FOLDER'])

app.secret_key = "secret key"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

def allowed_file(filename):
    file_ext = os.path.splitext(filename)[1]
    if file_ext in app.config['UPLOAD_EXTENSIONS']:return True


@app.route('/', methods=['GET','POST'])
def upload_file():
    if request.method == 'POST':
        file= request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            flash('File successfully uploaded')
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            global file_name 
            file_name = os.path.join(UPLOAD_FOLDER, filename)
            changedcsv = addColumns(file_name)
            return render_template('index.html',data = changedcsv)
        else:
            flash('Allowed file types are csv only')
            return redirect(request.url)
    else:
        return render_template('index.html', data="")


def addColumns(filename):
    pdf = pd.read_csv(filename,encoding='latin1')
    columns = []
    count = 0
    for i in pdf.iloc[0,:]:
        try:
            i = str(i).replace(",","")
            i = float(str(i).strip())
            columns.append(pdf.columns[count])
        except:
            pass
        count+=1
    thresh_l = []
    cols=[i for i in columns if len(pdf[i].unique())>2 ]
    for i in cols:
        try:
            pdf[i] = [ j.replace(",","") for j in pdf[i]]
            pdf[i] = [ j.replace("-","0") for j in pdf[i]]
        except:
            pass
        pdf[i] = pd.to_numeric(pdf[i],errors = "coerce")
        pdf ["disc_"+str(i)],thresh = pd.qcut(pdf[i],q=3,retbins = True,duplicates="drop")  #[0,0.333,0.666,1]
        thresh_l.append(thresh)
    return pdf.to_csv()

app.run(debug=True)