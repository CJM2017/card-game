import os
import boto3

from flask import Flask, jsonify, request
app = Flask(__name__)

USERS_TABLE = os.environ['USERS_TABLE']
IS_OFFLINE = os.environ.get('IS_OFFLINE')
 
if IS_OFFLINE:
    client = boto3.client(
        'dynamodb',
        region_name='localhost',
        endpoint_url='http://localhost:8000'
    )
else:
    client = boto3.client('dynamodb')
 
@app.route("/users/<string:userId>")
def getUser(userId):
    resp = client.get_item(
        TableName=USERS_TABLE,
        Key={
            'userId': { 'S': userId }
        }
    )
    item = resp.get('Item')
    if not item:
        return jsonify({'error': 'User does not exist'}), 404
 
    return jsonify({
        'userId': item.get('userId').get('S'),
        'name': item.get('name').get('S')
    })
 
 
@app.route("/users", methods=["POST"])
def createUser():
    userId = request.json.get('userId')
    name = request.json.get('name')
    if not userId or not name:
        return jsonify({'error': 'Please provide userId and name'}), 400
 
    _ = client.put_item(
        TableName=USERS_TABLE,
        Item={
            'userId': {'S': userId },
            'name': {'S': name }
        }
    )
 
    return jsonify({
        'userId': userId,
        'name': name
    })