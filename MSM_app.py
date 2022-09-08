from flask import Flask,render_template,request,Response,json
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_URI'] = "mongodb://localhost:27017/try1"
mongo = PyMongo(app)

db = mongo.db.users

@app.route("/signup", methods = ["GET","POST"])
def signup():  
    id = db.insert_one({
        'First_name' : request.json['First_name'],
        'Last_name' : request.json['Last_name'],
        'Email' : request.json['Email'],
        'User_name' : request.json['User_name'],
        'Password' : request.json['Password'],
    })
    print(id.inserted_id)

    return Response(
    mimetype="application/json",
    status=201,
    response=json.dumps({"message": "User created successfully", "id":str(id.inserted_id)})
    )
    

@app.route("/login", methods = ["GET"])
def login():
    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug = True)
