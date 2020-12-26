import flask
from flask import render_template, flash, redirect, request, url_for, session
from app import app,db
from flask_login import login_required, login_user,current_user,logout_user
from .users import User
from .contact import Contact
from .post import Post
from .comment import Comment
from sqlalchemy import or_, join, func

@app.route('/')
def index():
    posts = db.session.query(Post.id,Post.date,Post.subject,Post.description,Post.title,User.username).join(User).filter(Post.ownerId==User.id).order_by(Post.date).all()
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
            next = request.args.get('next')

            return redirect(next)

        except:
            msg="invalid username or password"
            return render_template('sign.html',msg=msg)

    return render_template('sign.html')

@app.route('/myRecords')
@login_required
def myRecords():
    posts = Post.query.filter_by(ownerId=current_user.get_id()).all()
    return render_template('myRecords.html',posts=posts)

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

@app.route('/delete/<int:id>',methods=['GET','POST'])
def delete(id):
        item_to_delete = Comment.query.get_or_404(id)
        postId=item_to_delete.postId
        db.session.delete(item_to_delete)
        db.session.commit()
        post = Post.query.filter_by(id=postId).first()
        user = User.query.filter_by(id=post.ownerId).first()
        comments = db.session.query(Comment.id, Comment.date, Comment.content, User.username).join(User).filter(
            Comment.postId == post.id).order_by(Comment.date).all()
        return render_template('postDetails.html', post=post, user=user, comments=comments)

@app.route('/deletePosts/<int:id>',methods=['GET','POST'])
def deletePost(id):
        item_to_delete = Post.query.get_or_404(id)
        if (current_user.get_id() == item_to_delete.ownerId):
            db.session.delete(item_to_delete)
            db.session.commit()
            flash("You have successfully deteled the record!")
        return render_template('index.html')

@app.route('/postDetails/<int:id>',methods=['GET','POST'])
@login_required
def postDetails(id):
    if request.method == 'POST':
        message = request.form.get("message",type=str)
        try:
            comment = Comment(content=message,postId=id,ownerId=current_user.get_id())
            db.session.add(comment)
            db.session.commit()
            flash('Comment succeed!!')

        except:
            flash('Sorry, comment failed...')

    post = Post.query.get_or_404(id)
    user = User.query.get_or_404(post.ownerId)
    comments = db.session.query(Comment.id, Comment.date, Comment.content, User.username).join(User).filter(
            Comment.postId == id).order_by(Comment.date).all()

    return render_template('postDetails.html',post=post,user=user,comments=comments)

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
