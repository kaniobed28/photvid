from flask import Flask,redirect,url_for,render_template,request,session
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_login import login_user,logout_user,current_user,UserMixin,LoginManager,login_required
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bcrypt import Bcrypt
from datetime import datetime
import os 
import secrets
import glob
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
db = SQLAlchemy(app)
app.secret_key = "this is my secrete key"

bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
@login_manager.user_loader

def user_loader(user_id):
    #TODO change here
    return User.query.get(user_id)
########################################MODEL#########################################
class User(db.Model,UserMixin):

    id = db.Column(db.Integer,
                   primary_key=True)
    username = db.Column(db.String(255),
                         nullable=False,
                         unique=False)
    email = db.Column(db.String(40),
                      unique=True,
                      nullable=False)
    password = db.Column(
                      db.String(255),
                      unique=False,
                      nullable=False
    )
    PhotosRel = db.relationship("Photos",backref = 'photos_backref')
    VideosRel = db.relationship("Videos",backref = 'videos_backref')



class Photos(db.Model,UserMixin):

    id = db.Column(db.Integer,
                   primary_key=True)
    title = db.Column(
                      db.String(255),
                      unique=False,
                      nullable=True
    )
    message = db.Column(
                      db.String(40),
                      unique=False,
                      nullable=True
    )
    img_filename = db.Column(
                      db.String(255),
                      unique=False,
                      nullable=True
    )

    

    user_id  = db.Column(
        db.Integer,
        db.ForeignKey('user.id')
    )
class Videos(db.Model,UserMixin):

    id = db.Column(db.Integer,
                   primary_key=True)
    title = db.Column(
                      db.String(255),
                      unique=False,
                      nullable=True
    )
    message = db.Column(
                      db.String(40),
                      unique=False,
                      nullable=True
    )


    vid_filename = db.Column(
                      db.String(255),
                      unique=False,
                      nullable=True
    )

    user_id  = db.Column(
        db.Integer,
        db.ForeignKey('user.id')
    )
    


    
def img_saver(input_file):
    filename = secrets.token_urlsafe(10) + input_file.filename
    path = os.path.join(r"flaskPro\static\img" , filename)
    input_file.save(path)
    return filename

def vid_saver(input_file):
    filename = secrets.token_urlsafe(10) + input_file.filename
    path = os.path.join(r"flaskPro\static\video" , filename)
    input_file.save(path)
    return filename
##################################ROUTE#####################################
@app.route('/',methods=['GET','POST'])
def index():
    imgData = Photos.query.order_by(Photos.id).all()
    return render_template('index.html',imgData = imgData)

@app.route('/videos', methods=['GET', 'POST'])
def videos():
    vidData = Videos.query.order_by(Videos.id).all()
    return render_template('videos.html',vidData = vidData)

@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html')
# @app.route('/contact', methods=['GET', 'POST'])
# def contact():
#     return render_template('contact.html')


@app.route('/upload_image', methods=['GET', 'POST'])
def upload_image():
    # if not session.get('email'):
    #     return redirect('/signup')
    if not current_user.is_authenticated:
        return redirect('/signup')
    if request.method == 'POST':
        title = request.form.get('title')
        message = request.form.get('message')
        photOrVid =request.files['photOrVid']
        queryEmail= current_user.email #session.get('email')
        query_data = User.query.filter_by(email= queryEmail).first()
        new_photvid = Photos(title = title,message = message,img_filename = img_saver(photOrVid),photos_backref = query_data)
        db.session.add(new_photvid)
        db.session.commit()

        return redirect("/")

    return render_template('upload_image.html')

@app.route('/upload_video', methods=['GET', 'POST'])
def upload_video():
    # if not session.get('email'):
    #     return redirect('/signup')
    if not current_user.is_authenticated:
        return redirect('/signup')
    if request.method == 'POST':
        title = request.form.get('title')
        message = request.form.get('message')
        photOrVid =request.files['photOrVid']
        queryEmail= current_user.email #session.get('email')
        query_data = User.query.filter_by(email= queryEmail).first()
        new_photvid = Videos(title = title,message = message,vid_filename = vid_saver(photOrVid),videos_backref = query_data)
        db.session.add(new_photvid)
        db.session.commit()

        return redirect("/videos")

    return render_template('upload_video.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # session['email'] = request.form.get('email',None)
    if request.method == 'POST':
        username = request.form.get('username',None)
        email = request.form.get('email',None)
        password = request.form.get('password',None)
        # session['email'] = request.form.get('email',None)

        new_user = User(username = username,email =email,password =password)
        db.session.add(new_user)
        db.session.commit()
        data = User.query.filter_by(email = email).first()
        login_user(data,remember=True)
        return redirect('/')
    return render_template('signup.html')

db.create_all()
if __name__ == '__main__':
  #DEBUG is SET to TRUE. CHANGE FOR PROD
  app.run(port=5000,debug=True)