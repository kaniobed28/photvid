from flask import Flask,redirect,url_for,render_template,request,session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy


app=Flask(__name__)
app.secret_key = "thisis "
app.config['SESSION_TYPE'] = 'sqlalchemy'

db = SQLAlchemy(app)
app.config['SESSION_SQLALCHEMY'] = db
db.create_all()



@app.route('/',methods=['GET','POST'])
def home():
    if request.method=='POST':
        
        session['uname'] = request.form.get('uname',None)
        session['pwd'] = request.form.get('pwd',None) 
        return render_template('page.html')
    if not session.get('uname'):
        return redirect(url_for('login'))
    return render_template('page.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    
    return render_template('login.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('uname',None)
    return render_template('logout.html')

if __name__ == '__main__':
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run(port=5000,debug=True)