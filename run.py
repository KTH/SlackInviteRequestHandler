from flask import Flask, jsonify, request
import requests
app = Flask(__name__)

@app.route('/challenge', methods=['POST'])
def challenge():
    req_json = request.get_json()
    if req_json and req_json.get('challenge'):
        return jsonify({'challenge': req_json.get('challenge')})
    return jsonify({'challenge': ''})

@app.route('/invite', methods=['POST'])
def invite():
    pass
