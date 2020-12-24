from flask import render_template, flash, redirect, request
from app import app,db
from flask_login import login_required, login_user,current_user,logout_user
from .users import User
from .contact import Contact
from .post import Post
from sqlalchemy import or_

@app.route('/')
def index():
    posts = Post.query.all().order_by(Post.date)
    movies = len(Post.query.filter_by(subject="MOVIES").all())
    drama = len(Post.query.filter_by(subject="DRAMA").all())
    books = len(Post.query.filter_by(subject="BOOKS").all())
    exhibition = len(Post.query.filter_by(subject="EXHIBITION").all())
    music = len(Post.query.filter_by(subject="MUSIC").all())
    return render_template('index.html',posts=posts,movies=movies,drama=drama,
                           books=books,exhibition=exhibition,music=music)

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
        if(len(password) < 6):
            msg = "password should at least contain 6 characters"
            return render_template('create.html',msg=msg)
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
        if(len(password) < 6):
            msg = "password should at least contain 6 characters"
            return render_template('password.html',msg=msg)
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

@app.route('/search',methods=['GET','POST'])
def search():
    if request.method == 'POST':
        content = request.form.get("search", type=str)
        posts = Post.query.filter(or_(Post.title.contains(content), Post.description.contains(content))).all()

    return render_template('search.html', posts=posts)

@app.route('/search/<subject>',methods=['GET','POST'])
def searchs(subject):
    posts=Post.query.filter_by(subject=subject).all()
    return render_template('search.html',posts=posts,subject=subject)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('index.html')
