from app import app,mongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify,request
from passlib.hash import scrypt

@app.route('/create',methods=['POST'])
def create_user():
    _json = request.json
    name = _json['name']
    email = _json['email']
    
    if name and email and request.method=='POST':
        mongo.db.user.insert_one({'name':name,'email':email})
        resp=jsonify("user added successfully")
        resp.status_code=200
        return resp
    else:
        return not_found()
    
@app.route('/users')
def users():
    users=mongo.db.user.find()
    resp=dumps(users)
    return resp

@app.route('/user/<id>')
def user(id):
    user=mongo.db.user.find_one({'_id':ObjectId(id)})
    resp=dumps(user)
    return resp

@app.route('/update/<id>',methods=['PUT'])
def update_user(id):
    _json = request.json
    name = _json['name']
    email = _json['email']
    
    
    if name and email and request.method=='PUT':
        
        mongo.db.user.update_one({'_id':ObjectId(id['$oid']) if '$oid' in id else ObjectId(id)},{'$set':{'name':name,'email':email}})
        resp = jsonify('User updated successfully!')
        resp.status_code=200
        return resp
    else:
        return not_found()

@app.route('/delete/<id>',methods=['DELETE'])
def delete_user(id):
    mongo.db.user.delete_one({'_id':ObjectId(id)})
    resp = jsonify("User deleted successfully!")
    resp.status_code=200
    return resp

@app.errorhandler(404)
def not_found(error=None):
    message={
        'status':404,
        'message':'Not Found'+request.url,
    }
    resp=jsonify(message)
    resp.status_code=404
    
    return resp

if __name__=="__main__":
    app.run(debug=True)
        
    
            