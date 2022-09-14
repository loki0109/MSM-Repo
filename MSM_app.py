from ast import Pass
from asyncio.windows_events import NULL
from flask import Flask,render_template,request,Response,json,flash, redirect,url_for,session
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['MONGO_URI'] = "mongodb://localhost:27017/msm_db"
mongo = PyMongo(app)
bcrypt = Bcrypt(app)

db = mongo.db.users

app.secret_key = "loki-1238sanmxg-dcj1248o"
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
    
@app.route("/login", methods = ["GET"])
def login():
    
    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug = True)
