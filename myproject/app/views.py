from flask import render_template, flash, redirect, request
from app import app,db
from flask_login import login_required, login_user,current_user,logout_user
from .users import User
from .contact import Contact

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sign',methods=['GET','POST'])
def sign():
    if request.method == 'POST':
        username = request.form.get("username", type=str)
        password = request.form.get("password", type=str)
        print(username,password)
        user = User.query.filter_by(username=username,password=password).first()
        try:
            login_user(user)
            return render_template('index.html')

        except:
            msg="invalid username or password"
            return render_template('sign.html',msg=msg)

    return render_template('sign.html')

@app.route('/myRecords')
@login_required
def myRecords():
    return render_template('myRecords.html')

@app.route('/addNew')
@login_required
def addNew():
    return render_template('addNew.html')

@app.route('/contact',methods=['GET','POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get("name",type=str)
        email = request.form.get("email",type=str)
        subject = request.form.get("subject",type=str)
        message = request.form.get("message",type = str)
        try:
            contact = Contact(name=name,email=email,subject=subject,message=message)
            db.session.add(contact)
            db.session.commit()
            flash('Message sent! Thank you!!')
        except:
            flash('Sorry, message failed...')
            render_template('contact.html')
    return render_template('contact.html')

@app.route('/create',methods=['GET','POST'])
def create():
    if request.method == 'POST':
        email = request.form.get("email", type=str)
        username = request.form.get("username", type=str)
        password = request.form.get("password", type=str)
        print(email,username,password)
        user = User.query.filter_by(email=email).all()
        if (len(user) != 0):
            msg = "You already have an account"
            return render_template('create.html', msg=msg)
        u = User.query.filter_by(username=username).all()
        if (len(u) != 0):
            msg = "invalid username"
            return render_template('create.html', msg=msg)
        try:
            user = User(email=email,username=username,password=password)
            db.session.add(user)
            db.session.commit()
            msg="Successfully create account, please log in"
            return render_template('sign.html',msg=msg)
        except:
            msg="Please try again"
            render_template('create.html', msg=msg)
    return render_template('create.html')

@app.route('/password',methods=['GET','POST'])
def password():
    if request.method == 'POST':
        email = request.form.get("email",type=str)
        username = request.form.get("username", type=str)
        password = request.form.get("password", type=str)
        print(email,username,password)
        user = User.query.filter_by(username=username,email=email).all()
        if (len(user) == 0):
            msg = "account not found"
            return render_template('password.html', msg=msg)
        try:
            user = User.query.filter_by(username=username, email=email).first()
            user.password = password
            db.session.commit()
            msg="password changed"
            return render_template('sign.html',msg=msg)

        except:
            msg="please try again"
            return render_template('password.html',msg=msg)
    return render_template('password.html')

@app.route('/postDetails')
def postDetails():
    return render_template('postDetails.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('index.html')