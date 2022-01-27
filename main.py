from flask import Flask,redirect,url_for,render_template,request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os 
import secrets
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@127.0.0.1/project'
db = SQLAlchemy(app)
########################################MODEL#########################################
class User__his(db.Model):

    id = db.Column(db.Integer,
                   primary_key=True)
    username = db.Column(db.String(255),
                         nullable=False,
                         unique=False)
    email = db.Column(db.String(40),
                      unique=True,
                      nullable=False)
    password = db.Column(db.String(200),
                         primary_key=False,
                         unique=False,
                         nullable=False)

    date = db.Column(db.DateTime,default = datetime.utcnow)

    topic = db.Column(db.String(255),
                      unique=False,
                      nullable=True)
    message = db.Column(db.String(1000000),
                      unique=False,
                      nullable=True)
    filename = db.Column(db.String(255),
                      unique=False,
                      nullable=True)


    
def upload_saver(input_file):
    filename = secrets.token_urlsafe(10) + input_file.filename
    path = os.path.join(r"flaskPro\static\img" , filename)
    input_file.save(path)
##################################ROUTE#####################################
@app.route('/',methods=['GET','POST'])
def index():
  if request.method=='POST':
    # Handle POST Request here
    return render_template('index.html')
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
    return render_template('upload.html')
db.create_all()
if __name__ == '__main__':
  #DEBUG is SET to TRUE. CHANGE FOR PROD
  app.run(port=5000,debug=True)