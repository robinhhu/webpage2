import flask
from flask import render_template, flash, redirect, request, jsonify, make_response
from flask_app import app,db
from flask_login import login_required, login_user,current_user,logout_user
from sqlalchemy import or_
from werkzeug.utils import secure_filename
import os, datetime, random
from datetime import timedelta
from .users import User
from .contact import Contact
from .post import Post
from .comment import Comment
from werkzeug.security import generate_password_hash,check_password_hash


#image extensions allowed
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG'])

#create a unique image name for each img using the current time
def create_uuid():
    nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S");
    randomNum = random.randint(0, 100);
    if randomNum <= 10:
        randomNum = str(0) + str(randomNum);
    uniqueNum = str(nowTime) + str(randomNum);
    return uniqueNum;

#qualify file names
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

app.send_file_max_age_default = timedelta(seconds=1)

#The main page is not required to login
#the index page with necessary information is rendered
#all posts posted by all users can be seen in the main page
@app.route('/')
def index():
    posts = db.session.query(Post.id,Post.imgFile,Post.date,Post.subject,Post.description,Post.title,User.username).join(User).filter(Post.ownerId==User.id).order_by(Post.date.desc()).all()

    s = []
    for post in posts:
        s.append(Post.query.get_or_404(post.id))
    temps = []
    for i in range(0,len(s)):
        likes = s[i].like
        collects=s[i].collect
        s[i].num=len(likes)
        s[i].numb=len(collects)
        temps.append(s[i])

    movies = len(Post.query.filter_by(subject="MOVIES").all())
    drama = len(Post.query.filter_by(subject="DRAMA").all())
    books = len(Post.query.filter_by(subject="BOOKS").all())
    exhibition = len(Post.query.filter_by(subject="EXHIBITION").all())
    music = len(Post.query.filter_by(subject="MUSIC").all())

    return render_template('index.html',posts=posts,movies=movies,drama=drama,
                           books=books,exhibition=exhibition,music=music,temp=temps)

#The user sign up page, when the login form is posted
#It compares the user whether exists then the password
#is compared to the hashed password stored in the database
#message will appear when something goes wrong
@app.route('/sign',methods=['GET','POST'])
def sign():
    if request.method == 'POST':
        username = request.form.get("username", type=str)
        password = request.form.get("password", type=str)
        user = User.query.filter_by(username=username).first()
        try:
            if check_password_hash(user.password, password):
                login_user(user)
                app.logger.info('%s logged in successfully', username)
                next = request.args.get('next')

                resp = make_response(redirect(next or flask.url_for('index')))
                resp.set_cookie('username', username)
                resp.set_cookie('password', password)
                return resp

            else:
                msg = "Password incorrect"
                app.logger.info('%s failed to log in', username)
                return render_template('sign.html',msg=msg)

        except:
                msg="Invalid username"
                return render_template('sign.html',msg=msg)

    name = request.cookies.get('username')
    password = request.cookies.get('password')

    return render_template('sign.html',name=name,password=password)

#It is a login required page, all posts posted by the
#current user is rendered in this page
@app.route('/myRecords')
@login_required
def myRecords():
    posts = Post.query.filter_by(ownerId=current_user.get_id()).order_by(Post.date.desc()).all()
    for post in posts:
        post.num = len(post.like)
        post.numb = len(post.collect)

    return render_template('myRecords.html',posts=posts)

#It is a login required page, current user can post
#new record to the website.
#The img should be checked in the right format and uploaded
#to the static folder.
#other information posted with the form should be stored
#and added to the database
@app.route('/addNew',methods=['GET','POST'])
@login_required
def addNew():
    if request.method == 'POST':
        img = request.files.get("photo")
        if not (img and allowed_file(img.filename)):
            return jsonify({"error": 1001, "msg": "Only png, jpg allowed"})

        basepath = os.path.dirname(__file__)

        fname = secure_filename(img.filename)

        ext = fname.rsplit('.', 1)[1]
        new_filename = create_uuid() + '.' + ext
        upload_path = os.path.join(basepath, 'static/images',
                                       new_filename)
        img.save(upload_path)

        subject = request.form.get("subject",type=str)
        title = request.form.get("title",type=str)
        description = request.form.get("description",type=str)
        name = request.cookies.get('username')
        try:
            post = Post(subject=subject,title=title,imgFile=new_filename,description=description,ownerId=current_user.get_id())
            db.session.add(post)
            db.session.commit()
            app.logger.info('%s create a post', name)
            flash("Record created!! Check it in your records!")
        except:
            app.logger.warning('%s failed to create a post', name)
            flash("Sorry, record failed...")

    return render_template('addNew.html')

#The page is not required to login
#Any visitors can send message to the developer
#through filing the form. The code get inforation
#sent by the visitor and add it to the database
#Information indicating whether it is succeed or failed
#will be flashed to the page
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
            app.logger.info('%s sent a message', name)
            flash('Message sent! Thank you!!')
        except:
            app.logger.warning('%s fail to sent a message', name)
            flash('Sorry, message failed...')
            render_template('contact.html')
    return render_template('contact.html')

#Create account page.
#when the form is submitted, the password should be checked
#to be longer than 6 characters
#Then each email address should be guaranteed to
#create one account. Username should not be the same
#So alert will appear when those conditions are met
#Or else email, username and the hashed password will be
#stored in the database
@app.route('/create',methods=['GET','POST'])
def create():
    if request.method == 'POST':
        email = request.form.get("email", type=str)
        username = request.form.get("username", type=str)
        password = request.form.get("password", type=str)
        if(len(password) < 6):
            msg="password should at least contain 6 characters"
            return render_template('create.html',msg=msg)
        user = User.query.filter_by(email=email).all()
        if (len(user) != 0):
            msg="You already have an account"
            return render_template('create.html',msg=msg)
        u = User.query.filter_by(username=username).all()
        if (len(u) != 0):
            msg="invalid username"
            return render_template('create.html',msg=msg)
        try:
            user = User(email=email,username=username,password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            app.logger.info('%s create account', username)
            msg="Successfully create account, please log in"
            return render_template('sign.html',msg=msg)
        except:
            app.logger.warning("%s fail to create",username)
            msg="Please try again"
            return render_template('create.html',msg=msg)
    return render_template('create.html')

#Reset password page
#when the form is submitted, the password should be checked
#to be longer than 6 characters
#Then the user length is compared to guarantee the account exist
#So alert will appear when those conditions are met
#Or else the hashed password will be stored in the database
@app.route('/password',methods=['GET','POST'])
def password():
    if request.method == 'POST':
        email = request.form.get("email",type=str)
        username = request.form.get("username", type=str)
        password = request.form.get("password", type=str)
        if(len(password) < 6):
            msg="password should at least contain 6 characters"
            return render_template('password.html',msg=msg)
        user = User.query.filter_by(username=username,email=email).all()
        if (len(user) == 0):
            msg="account not found"
            return render_template('password.html',msg=msg)
        try:
            user = User.query.filter_by(username=username, email=email).first()
            user.password = generate_password_hash(password)
            db.session.commit()
            app.logger.info('%s reset password', username)
            msg="password changed"
            return render_template('sign.html',msg=msg)

        except:
            app.logger.warning("%s fail to reset",username)
            msg="please try again"
            return render_template('password.html',msg=msg)
    return render_template('password.html')

#Login required page
#only the owner of the comment can delete the comment
@app.route('/delete/<int:id>',methods=['GET','POST'])
@login_required
def delete(id):
        item_to_delete = Comment.query.get_or_404(id)
        postId = item_to_delete.postId
        if (int(current_user.get_id()) == int(item_to_delete.ownerId)):
            db.session.delete(item_to_delete)
            db.session.commit()
        post = Post.query.filter_by(id=postId).first()
        user = User.query.filter_by(id=post.ownerId).first()
        comments = db.session.query(Comment.id, Comment.date, Comment.content, User.username).join(User).filter(
            Comment.postId == post.id).order_by(Comment.date).all()

        a = "far"
        b = "far"
        likes = post.like
        collects = post.collect

        for like in likes:
            if int(like.id) == int(current_user.get_id()):
                a = "fas"

        for collect in collects:
            if int(collect.id) == int(current_user.get_id()):
                b = "fas"

        return render_template('postDetails.html', post=post, user=user, comments=comments, a=a,b=b)

#login required page
#only the owner of the post can delete the post
#all comments should be deleted before the post
#to be deleted to avoid any violents
@app.route('/deletePosts/<int:id>',methods=['GET','POST'])
@login_required
def deletePost(id):
        item_to_delete = Post.query.get_or_404(id)
        comments = Comment.query.filter_by(postId=id).all()
        if (int(current_user.get_id()) == int(item_to_delete.ownerId)):
            for comment in comments:
                db.session.delete(comment)
            db.session.delete(item_to_delete)
            db.session.commit()
            app.logger.info('%s post deleted', item_to_delete.postId)
            flash("You have successfully deteled the record!")
        else:
            app.logger.warning("%s no access to delete",item_to_delete.postId)
            flash("You do not have access to delete the post..")
        return redirect('/')

#login required page
#If form is submitted then comment is added to the database
#else render the page
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
            app.logger.warning("comment failed")
            flash('Sorry, comment failed...')

    a = "far"
    b = "far"
    post = Post.query.get_or_404(id)
    user = User.query.get_or_404(post.ownerId)
    comments = db.session.query(Comment.id, Comment.date, Comment.content, User.username).join(User).filter(
            Comment.postId == id).order_by(Comment.date).all()
    likes = post.like
    collects = post.collect

    for like in likes:
        if int(like.id) == int(current_user.get_id()):
            a = "fas"

    for collect in collects:
        if int(collect.id) == int(current_user.get_id()):
            b = "fas"

    return render_template('postDetails.html',post=post,user=user,comments=comments,a=a,b=b)

#login required page
#Query the search content in the database and render the search page
@app.route('/search',methods=['GET','POST'])
@login_required
def search():
    if request.method == 'POST':
        content = request.form.get("search", type=str)
        posts = Post.query.filter(or_(Post.title.contains(content), Post.description.contains(content))).all()

        for post in posts:
            collects = post.collect
            likes = post.like
            post.b="far"
            post.a="far"
            for like in likes:
                if int(like.id) == int(current_user.get_id()):
                    post.a = "fas"
            for collect in collects:
                if int(collect.id) == int(current_user.get_id()):
                    post.b = "fas"

    return render_template('search.html', posts=posts)

#login required page
#Query the search content in the database and render the search page
@app.route('/search/<subject>',methods=['GET','POST'])
@login_required
def searchs(subject):
    posts=Post.query.filter_by(subject=subject).all()

    for post in posts:
        likes = post.like
        collects=post.collect
        post.a = "far"
        post.b = "far"
        for like in likes:
            if int(like.id) == int(current_user.get_id()):
                post.a = "fas"
        for collect in collects:
            if int(collect.id) == int(current_user.get_id()):
                post.b = "fas"
    return render_template('search.html',posts=posts,subject=subject)

#login required
#logout user
@app.route('/logout')
@login_required
def logout():
    app.logger.info('%s logout', current_user)
    logout_user()
    return redirect('/')

#login required
#like posts, if already liked, then unlike
#else like
@app.route('/likes/<int:id>',methods=['POST','GET'])
@login_required
def like(id):
    if request.method == 'POST':
        user = current_user.get_id()
        post = Post.query.get_or_404(id)
        likes = post.like
        for like in likes:
            if int(like.id) == int(user):
                post.like.remove(current_user)
                db.session.commit()
                return redirect('/postDetails/' + str(id))

        post.like.append(current_user)
        db.session.commit()
    return redirect('/postDetails/'+str(id))

#login required
#collect posts, if already collected, then uncollected
#else collect
@app.route('/collects/<int:id>',methods=['POST','GET'])
@login_required
def collect(id):
    if request.method == 'POST':
        user = current_user.get_id()
        post = Post.query.get_or_404(id)
        collects = post.collect
        for collect in collects:
            if int(collect.id) == int(user):
                post.collect.remove(current_user)
                db.session.commit()
                return redirect('/postDetails/' + str(id))

        post.collect.append(current_user)
        db.session.commit()
    return redirect('/postDetails/'+str(id))

#login required
#query all mylike posts
@app.route('/myLike',methods=['POST','GET'])
@login_required
def myLike():
    temps = db.session.query(Post.id, Post.imgFile, Post.date, Post.subject, Post.description, Post.title,
                             User.username).join(User).filter(Post.ownerId == User.id).order_by(Post.date.desc()).all()
    s = [];
    for temp in temps:
        s.append(Post.query.get_or_404(temp.id))
    posts = []
    for ss in s:
        likes = ss.like
        ss.a="far"
        for like in likes:
            if int(like.id) == int(current_user.get_id()):
                ss.a="fas"
                posts.append(ss)

    movies = len(Post.query.filter_by(subject="MOVIES").all())
    drama = len(Post.query.filter_by(subject="DRAMA").all())
    books = len(Post.query.filter_by(subject="BOOKS").all())
    exhibition = len(Post.query.filter_by(subject="EXHIBITION").all())
    music = len(Post.query.filter_by(subject="MUSIC").all())

    return render_template('myLike.html', posts=posts, movies=movies, drama=drama,
                           books=books, exhibition=exhibition, music=music,temps=temps)

#login required
#query all mycollection posts
@app.route('/mysc',methods=['POST','GET'])
@login_required
def mysc():
    temps = db.session.query(Post.id, Post.imgFile, Post.date, Post.subject, Post.description, Post.title,
                             User.username).join(User).filter(Post.ownerId == User.id).order_by(Post.date.desc()).all()
    s = [];
    for temp in temps:
        s.append(Post.query.get_or_404(temp.id))
    posts = []
    for ss in s:
        collects = ss.collect
        ss.a="far"
        for collect in collects:
            if int(collect.id) == int(current_user.get_id()):
                ss.a="fas"
                posts.append(ss)

    movies = len(Post.query.filter_by(subject="MOVIES").all())
    drama = len(Post.query.filter_by(subject="DRAMA").all())
    books = len(Post.query.filter_by(subject="BOOKS").all())
    exhibition = len(Post.query.filter_by(subject="EXHIBITION").all())
    music = len(Post.query.filter_by(subject="MUSIC").all())

    return render_template('mysc.html', posts=posts, movies=movies, drama=drama,
                           books=books, exhibition=exhibition, music=music,temps=temps)

