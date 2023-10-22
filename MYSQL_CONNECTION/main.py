from app import app,mysql
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify,request
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/signup',methods=['POST'])
def signup():
    _json = request.json
    username = _json['username']
    password = _json['password']
    
    if username and password and request.method=='POST':
        
        if len(password)<8:
            message={
                'status':400,
                'message':"Password should atleast contain 8 characters!"
            }
            resp = jsonify(message)
            resp.status_code = 400
            return resp 
        # creating a connection curser
        cursor = mysql.cursor()
        cursor.execute("select * from User where username = %s",(username))
        user = cursor.fetchone()
        cursor.close()
        
        if user:
            resp = jsonify("username is already taken")
            return resp
        else:    
            
            # creating a connection curser
            cursor = mysql.cursor()
            hashpwd = bcrypt.generate_password_hash(password)
            cursor.execute("insert into User (username,password) values (%s,%s)",(username,hashpwd))
            #saving the actions performed on the db
            mysql.commit()
            #closing the cursor
            cursor.close()
            resp = jsonify("user registration successful!")
            resp.status_code = 200
            return resp

@app.route('/login',methods=['POST'])
def login():
    _json = request.json
    username = _json['username']
    password = _json['password']
    
    if username and password and request.method=='POST':
        if len(password)<8:
            message={
                'status':400,
                'message':"Password should atleast contain 8 characters!"
            }
            resp = jsonify(message)
            resp.status_code = 400
            return resp 
        #creating connection server
        cursor = mysql.cursor()
        cursor.execute('select * from User where username = %s',(username))
        user = cursor.fetchone()
        cursor.close()
        
        if user:
            if bcrypt.check_password_hash(user[1],password):
                resp = jsonify("you are successfully logged in")
                resp.status_code = 200
                return resp
            else:
                resp = jsonify("Incorrect password")
                resp.status_code = 400
                return resp
        else:
            resp = jsonify("User not found")
            resp.status_code = 404
            return resp   

if __name__ == '__main__':
    app.run(debug=True)