from flask import Flask , render_template, request, url_for, redirect, session, flash
from datetime import timedelta
from flask import Flask
from flask import current_app as app
from flask_sqlalchemy import SQLAlchemy
from os import path
import pandas as pd
import random

#import model
app = Flask(__name__)
app.config['SECRET_KEY'] = ''.join((random.choice('abcdxyzpqr') for i in range(12)))
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///user.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(minutes=30)

db = SQLAlchemy(app)
app.app_context().push()
class User(db.Model):
    user_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    password = db.Column(db.String(100))
    def  __init__(self, name, password):
        self.name = name
        self.password = password

@app.route("/")
def Load():
    return render_template("index.html");

@app.route("/About")
def About():
    if "user" in session:
        name = session['user']
        return render_template("About.html");
    else:
        flash("You haven't login yet", "info")
        return redirect(url_for('loginPage'))

@app.route("/UserGuide")
def user_guide():
    if "user" in session:
        name = session['user']
        return render_template("UserGuide.html");
    else:
        flash("You haven't login yet", "info")
        return redirect(url_for('loginPage'))

@app.route("/home")
def homePage():
    if "user" in session:
        name = session['user']
        return render_template("home.html");
    else:
        flash("You haven't login yet", "info")
        return redirect(url_for('loginPage'))

@app.route("/Login", methods =['POST','GET'])
def loginPage():
   if request.method == 'POST':
        user_name = request.form['ten']
        password = request.form['matkhau']
        session.permanent = True
        flash("You logged in successfully", "info")
        if user_name:
            session['user'] =user_name
            user = User(user_name,password)
            db.session.add(user)
            db.session.commit()
            flash("Created in DB successfully", "info")
            A = True
        return redirect(url_for('user',name = user_name))
   return render_template("login.html")

@app.route("/user")
def user():
    if "user" in session:
        name = session['user']
        return render_template("user.html");
    else:
        flash("You haven't login yet", "info")
        return redirect(url_for('loginPage'))

@app.route("/Logout")
def Logout():
    if "user" in session:
        session.pop('user',None)
        flash("You logged out ", "info")
        return redirect(url_for('loginPage'))
    else:
        flash("You haven't login yet", "info")
        return redirect(url_for('loginPage'))

if __name__ == "__main__":
    if not path.exists("user.db"):
        db.create_all()
        print("Created Database")
    app.run(debug = True)





'''
@app.route("/", methods = ['GET','POST'])
def submit():
    #html -> .py
    if request.method =="POST": 
        Arg1 = request.form["arg_1"]
        Arg2 = request.form["arg_2"]
        Arg3 = request.form["arg_3"]
        Arg4 = request.form["arg_4"]
        Arg5 = request.form["arg_5"]
        Arg6 = request.form["arg_6"]
        Arg7 = request.form["arg_7"]
        Arg8 = request.form["arg_8"]
        Arg9 = request.form["arg_9"]
        Arg10 = request.form["arg_10"]

    new_data = pd.DataFrame([[Arg1,Arg2,Arg3,Arg4,Arg5,Arg6,Arg7,Arg8,Arg9,Arg10]],
        columns=['gender','age','hypertension','heart_disease','ever_married','work_type','Residence_type','avg_glucose_level','bmi','smoking_status' ])
    
    Result = model.dtree.predict(new_data)
    print(Result)
    #.py -> html
    return render_template("index.html", predict = Result)


@app.route("/" , methods = ['GET'])
def User():
    return render_template("tab2.html")

'''
