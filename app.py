from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from bson.objectid import ObjectId
from flask_cors import CORS

app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017')

db = client['Flask_API'] # db name

# prevent the cors error
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/users' , methods=['POST','GET'])
def data():

    if request.method == 'POST':
        body = request.json
        firstName = body['firstname']
        lastName = body['lastname']
        emailId = body['emailId']

        db['user'].insert_one({
            "firstname":firstName,
            "lastname":lastName,
            "emailId":emailId
        })

        return jsonify({
            'status':'Data is posted to mngogo db',
            "user":body
        })
    
    if request.method == 'GET':
        allUsers = db['user'].find()
        dataJson = []
        for data in allUsers:
            id = data['_id']
            firstname = data['firstname']
            lastname = data['lastname']
            emailId = data['emailId']

            dataDict = {
                "id":str(id),
                'firstname':firstname,
                'lastname':lastname,
                'emailId':emailId
            }

            dataJson.append(dataDict)

        return jsonify({
            'data':dataJson
        })
    
@app.route('/users/<string:id>' , methods=['PUT','GET','DELETE'])
def onedata(id):

    if request.method == 'GET':
        data = db['user'].find_one({
            "_id":ObjectId(id)
        })

        id = data['_id']
        firstname = data['firstname']
        lastname = data['lastname']
        emailId = data['emailId']

        dataDict = {
            "id":str(id),
            'firstname':firstname,
            'lastname':lastname,
            'emailId':emailId
        }

        return jsonify({
            "data":dataDict
        })
    
    if request.method == 'DELETE':
        data = db['user'].delete_many({
            "_id":ObjectId(id)
        })

        return jsonify({
            'status':"user deleted successfully"
        })
    
    if request.method == 'PUT':
        body = request.json
        firstname = body['firstname']
        lastname = body['lastname']
        emailId = body['emailId']

        dataDict = {
            'firstname':firstname,
            'lastname':lastname,
            'emailId':emailId
        }

        db['user'].update_one({
            "_id":ObjectId(id)
        },{
            '$set': dataDict
        })

        return jsonify({
            'status':"user updated successfully"
        })
    

if __name__ == '__main__':
    app.debug = True
    app.run()