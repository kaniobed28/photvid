from email import message
from fileinput import filename
from flask import Flask,redirect,url_for,render_template,request,session
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from datetime import datetime
import os 
import secrets
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@127.0.0.1/project'
db = SQLAlchemy(app)
app.secret_key = "this is my secrete key"
########################################MODEL#########################################
class User(db.Model):

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
    PhotOrVidRel = db.relationship("PhotOrVid",backref = 'photvids')



class PhotOrVid(db.Model):

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
    filename = db.Column(
                      db.String(255),
                      unique=False,
                      nullable=True
    )
    user_id  = db.Column(
        db.Integer,
        db.ForeignKey('user.id')
    )
    


    
def upload_saver(input_file):
    filename = secrets.token_urlsafe(10) + input_file.filename
    path = os.path.join(r"flaskPro\static\img" , filename)
    input_file.save(path)
    return filename
##################################ROUTE#####################################
@app.route('/',methods=['GET','POST'])
def index():
  

    return render_template('index.html')

@app.route('/videos', methods=['GET', 'POST'])
def videos():
    return render_template('videos.html')

@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html')
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    return render_template('contact.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if not session.get('email'):
        return redirect('/signup')
    if request.method == 'POST':
        title = request.form.get('title')
        message = request.form.get('message')
        photOrVid =request.files['photOrVid']
        queryEmail= session.get('email')
        query_data = User.query.filter_by(email= queryEmail).first()
        new_photvid = PhotOrVid(title = title,message = message,filename = upload_saver(photOrVid),photvids = query_data)
        db.session.add(new_photvid)
        db.session.commit()

    return render_template('upload.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # session['email'] = request.form.get('email',None)
    if request.method == 'POST':
        username = request.form.get('username',None)
        email = request.form.get('email',None)
        password = request.form.get('password',None)
        session['email'] = request.form.get('email',None)

        new_user = User(username = username,email =email,password =password)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/')
    return render_template('signup.html')

db.create_all()
if __name__ == '__main__':
  #DEBUG is SET to TRUE. CHANGE FOR PROD
  app.run(port=5000,debug=True)