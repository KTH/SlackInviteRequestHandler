__author__ = 'tinglev@kth.se'

import json
import logging
from flask import Flask, jsonify, request
import requests
app = Flask(__name__)

@app.route('/invite-handler/_monitor', methods=['GET'])
def monitor():
    return 'APPLICATION_STATUS: OK'

@app.route('/invite-handler/event', methods=['POST'])
def challenge():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    req_json = request.get_json()
    logger.debug('Got json: %s', json.dumps(req_json))
    if req_json and req_json.get('challenge'):
        return jsonify({'challenge': req_json.get('challenge')})
    return jsonify({'challenge': ''})
