from ast import Pass
import os
from asyncio.windows_events import NULL
from re import template
from flask import Flask,render_template,request,Response,json,flash,redirect,url_for,session
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_session import Session

app = Flask(__name__)
app.config['MONGO_URI'] = "mongodb://localhost:27017/msm_db"
mongo = PyMongo(app)
bcrypt = Bcrypt(app)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

db = mongo.db.users

app.secret_key = "loki-1238sanmxg-dcj1248o"
sessionvb = Session(app)

@app.route("/signup",methods = ["POST", "GET"])
def signup():  
    if request.method == "POST":
        Full_name = request.form['Full_name']
        Email = request.form['Email']
        User_name = request.form['User_name']
        Password = request.form['Password']
        hashed_password = bcrypt.generate_password_hash(Password).decode('utf-8')
        if((db.count_documents({'email':Email}))!=0):
            flash(f'Email Id already exists!!!','danger')
            
        else:
            new_user = {
                'name': Full_name,
                'email':Email,
                'User_name':User_name,
                'Password': hashed_password
            }
            db.insert_one(new_user)
            flash(f'User {Full_name} is successfully created','success')
            return redirect(url_for('login'))
    return render_template('signup.html')
    
@app.route("/login", methods = ["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form["Email"]
        password = request.form["Password"]
        name_pass = db.find_one({'email':email},{'_id':0,'Password':1})
        if bcrypt.check_password_hash(name_pass['Password'],password):
            session["email"] = email
            flash(f'User logged in successfully','success')
            return redirect(url_for('feed'))
        else:
            flash(f'Invalid credentials','danger')
    return render_template("login.html")

@app.route("/feed",methods = ["POST","GET"])
def feed():
    emailvar = session["email"]
    sess_name = db.users.find({'email':emailvar})
    usern=[]
    for i in sess_name:
        usern.append(i)
        print(i)
    return render_template("feed.html",usern=usern)

@app.route("/homepage",methods = ["POST","GET"])
def homepage():
    return render_template("homepage.html")

@app.route("/logout")
def logout():
    session["email"] = None
    return redirect("/homepage")
    
@app.route("/image_upload",methods = ["POST","GET"])
def image_upload():
    return render_template("image_upload.html")

if __name__ == "__main__":
    app.run(debug = True)
