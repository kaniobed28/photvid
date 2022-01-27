from flask import Flask,redirect,url_for,render_template,request
from flask_sqlalchemy import SQLAlchemy
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@127.0.0.1/project'
db = SQLAlchemy(app)

class User(db.Model):
    

    id = db.Column(db.Integer,
                   primary_key=True)
    username = db.Column(db.String(50),
                         nullable=False,
                         unique=False)
   
    password = db.Column(db.String(200),
                         primary_key=False,
                         unique=False,
                         nullable=False)
    vid = db.relationship('Video',backref = 'myvideo')
class Video(db.Model):
    

    id = db.Column(db.Integer,
                   primary_key=True)
    video = db.Column(db.String(50),
                         nullable=False,
                         unique=False)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('user.id')
                       
                                )


   
db.create_all()

obed = User(username = "Kani Obed",password = "1234pass") 
db.session.add(obed)
# db.session.commit() the commit should be one in any function of class
data = User.query.filter_by(password ='1234pass').first()
obvid = Video(video = 'cap america',myvideo = data)
db.session.add(obvid)
db.session.commit()














@app.route('/',methods=['GET','POST'])
def home():
    if request.method=='POST':
        # Handle POST Request here
        return render_template('index.html')
    return render_template('index.html')

if __name__ == '__main__':
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run(port=5000,debug=True)