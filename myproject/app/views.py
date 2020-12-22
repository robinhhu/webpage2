from flask import render_template
from app import app

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sign')
def sign():
    return render_template('sign.html')

@app.route('/myRecords')
def myRecords():
    return render_template('myRecords.html')

@app.route('/addNew')
def addNew():
    return render_template('addNew.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/create')
def create():
    return render_template('create.html')

@app.route('/password')
def password():
    return render_template('password.html')

@app.route('/postDetails')
def postDetails():
    return render_template('postDetails.html')