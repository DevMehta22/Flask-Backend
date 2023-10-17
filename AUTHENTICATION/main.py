from app import app,mongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify,request
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/register',methods=['POST'])
def register_user():
    _json = request.json
    email = _json['email']
    password = _json['password']
    
    if email and password and request.method=='POST':
        
        if len(password)<8:
            message={
                'status':400,
                'message':"Password should atleast contain 8 characters!"
            }
            resp = jsonify(message)
            resp.status_code = 400
            return resp
        
        if mongo.db.auth.find_one({'email':email})!=None:
            resp = jsonify("email already exist!")
            resp.status_code = 400
            return resp
        else:    
            hashpwd = bcrypt.generate_password_hash(password)
            mongo.db.auth.insert_one({'email':email,'password':hashpwd})
            resp = jsonify("user registration successful!")
            resp.status_code = 200
            return resp
    
@app.route('/login',methods=['POST'])
def login_user():
    _json = request.json
    email = _json['email']
    password = _json['password']
    
    if email and password and request.method=='POST':
        
        if len(password)<8:
            message={
                'status':400,
                'message':"Password should atleast contain 8 characters!"
            }
            resp = jsonify(message)
            resp.status_code = 400
            return resp 
        
        user = mongo.db.auth.find_one({'email':email})
        if user:
            if bcrypt.check_password_hash(user['password'],password):
                resp = jsonify("you are successfully logged in!")
                resp.status_code = 200
                return resp
            else:
                resp = jsonify("password is incorrect!")
                resp.status_code=400
                return resp   
        else:
            resp = jsonify("Email not found")
            resp.status_code=400
            return resp 
                
if __name__=='__main__':
        app.run(debug=True)