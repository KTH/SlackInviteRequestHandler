from flask import Flask, jsonify, request
import requests
app = Flask(__name__)

@app.route('/invite-handler/_monitor', methods=['GET'])
def monitor():
    return 'APPLICATION_STATUS: OK'

@app.route('/invite-handler/challenge', methods=['POST'])
def challenge():
    req_json = request.get_json()
    if req_json and req_json.get('challenge'):
        return jsonify({'challenge': req_json.get('challenge')})
    return jsonify({'challenge': ''})

@app.route('/invite-handler/', methods=['POST'])
def invite():
    req_json = request.get_json()
    print(f'Recieved {req_json}')
