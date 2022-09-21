from flask import Flask,render_template,request,Response,json,flash,redirect,url_for,session
from flask_pymongo import PyMongo,ObjectId
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
            flash(f'Log in successful','success')
            return redirect(url_for('feed'))
        else:
            flash(f'Invalid credentials','danger')
    return render_template("login.html")

@app.route("/homepage",methods = ["POST","GET"])
def homepage():
        return render_template("homepage.html")

@app.route("/logout")
def logout():
    session["email"] = None
    return redirect("/homepage")
    
@app.route("/image_upload",methods = ["GET","POST"])
def image_upload():
    if "uploaded_image" in request.files:
        uploaded_image = request.files['uploaded_image']
        mongo.save_file(uploaded_image.filename, uploaded_image)
        mongo.db.photos.insert_one(
            {'Image_name': request.form.get('Image_name'), 'uploaded_image_name': uploaded_image.filename,'like_counter':0})
        mongo.db.fs.files.insert_one({'like_counter':0})
        return redirect(url_for('feed'))
    return render_template("image_upload.html")

@app.route("/feed",methods = ["POST","GET"])
def feed():
    retrive_img = list(mongo.db.fs.files.find({}))    
    emailvar = session["email"]
    sess_name = db.users.find({'email':emailvar})
    usern=[]
    for i in sess_name:
        usern.append(i)
        print(i)
    return render_template("feed.html",usern=usern,retrive_img=retrive_img)

@app.route("/update",methods=["POST","GET"])
def update():
    if request.method == "POST":
        old_name = request.form['old_name']
        new_name = request.form['new_name']
        update_find_all = list(mongo.db.photos.find({'Image_name':old_name},{'uploaded_image_name':0, '_id':0}))
        if old_name == update_find_all[0]['Image_name']:
            mongo.db.photos.update_one({'Image_name': old_name },{'$set':{'Image_name':new_name}})
            flash(f'Updated Successfully','info')
            return redirect(url_for('feed'))
        else:
            flash(f'Enter correct name','danger')
    return render_template('update.html')
        
@app.route("/like_button/<id>",methods=["POST","GET"])
def like_button(id):
    print("========================")
    data= request.args.get('like1')
    print(data)
    print("========================")
    print(data) 
    return redirect('/feed')

@app.route("/delete/<id>",methods = ["POST","GET"])
def delete(id):
    print(id)
    mongo.db.fs.files.delete_one({'_id':ObjectId(id)})
    flash(f'Post Deleted Successfully','info')
    return redirect('/feed')

if __name__ == "__main__":
    app.run(debug = True)
