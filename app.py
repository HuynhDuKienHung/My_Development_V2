from flask import Flask , render_template, request, url_for, redirect, session, flash
from datetime import timedelta
from flask import Flask
from flask import current_app as app
from os import path
import pandas as pd
import random

import firebase_admin
from firebase_admin import db, credentials
import json
obj_create =firebase_admin.credentials.Certificate('static/js/serviceAccountKey.json')
default_app = firebase_admin.initialize_app(obj_create,{
    'databaseURL':'https://real-time-database-02023-default-rtdb.firebaseio.com/'
    })
#import model
app = Flask(__name__)
app.config['SECRET_KEY'] = ''.join((random.choice('abcdxyzpqr') for i in range(12)))
app.permanent_session_lifetime = timedelta(minutes=30)

ref_user = db.reference('/user')

@app.route("/")
def Load():
    return render_template("index.html");

@app.route("/Login", methods =['POST','GET'])
def login():
    if request.method == 'POST':
        user_name = request.form['ten']
        password = request.form['matkhau']
        if not(check_account_exists(user_name)):
            flash("Account doesn't exist", "info")
            return redirect(url_for('signup'))
        else:
            session['user'] =user_name
            ref = db.reference(f"/user/{user_name}")
            data_send = {
                'name': user_name,
                'password': password
            }
            ref.update(data_send)
            return redirect(url_for('user',name = user_name))
    return render_template("login.html")

@app.route("/Register", methods = ['POST', 'GET'])
def signup():
    if request.method == 'POST':
        user_name = request.form['ten']
        password = request.form['matkhau']
        if (check_account_exists(user_name)):
            flash("Account already exists", "info")
            return redirect(url_for('login'))
        else:
            session['user'] =user_name
            ref = db.reference(f"/user/{user_name}")
            data_send = {
                'name': user_name,
                'password': password
            }
            ref.update(data_send)
            return redirect(url_for('user',name = user_name))
    return render_template("signup.html")
@app.route("/Logout")
def Logout():
    if "user" in session:
        session.pop('user',None)
        return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))



@app.route("/home")
def homePage():
    if "user" in session:
        name = session['user']
        return render_template("home.html");
    else:
        return redirect(url_for('login'))
    
@app.route("/UserGuide")
def user_guide():
    if "user" in session:
        name = session['user']
        return render_template("UserGuide.html");
    else:
        return redirect(url_for('login'))



@app.route("/user")
def user():
    if "user" in session:
        name = session['user']
        return render_template("user.html");
    else:
        return redirect(url_for('login'))

@app.route("/About")
def About():
    if "user" in session:
        name = session['user']
        return render_template("About.html");
    else:
        return redirect(url_for('login'))

def check_account_exists(username):
    user_ref = ref_user.child(username)
    user_data = user_ref.get()
    return user_data is not None

if __name__ == "__main__":
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
