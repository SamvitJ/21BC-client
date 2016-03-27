#!/usr/bin/env python3
import sys
from flask import Flask, request, Response
import json

from two1.commands.config import Config
from two1.lib.wallet import Wallet
from two1.lib.bitrequests import BitTransferRequests
from two1.lib.bitrequests import ChannelRequests

# Create app
app = Flask(__name__)

@app.after_request
def enable_cors(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'
    return response

@app.route('/headers-channels', methods=['GET', 'POST'])
def headers_channels():
    wallet = Wallet()
    username = Config().username
    chanrequests = ChannelRequests(wallet, deposit_amount=10000)

    data_dict = request.get_json()
    resp = type('', (object,), {'headers':data_dict.get('headers'), 'url':data_dict.get('url')})()

    req_headers = chanrequests.make_402_payment(resp, 200)
    print(req_headers)

    return json.dumps(req_headers)

@app.route('/headers', methods=['GET', 'POST'])
def headers():
    wallet = Wallet()
    username = Config().username
    bitrequests = BitTransferRequests(wallet, username)

    data_dict = request.get_json()
    resp = type('', (object,), {'headers':data_dict.get('headers'), 'url':data_dict.get('url')})()

    req_headers = bitrequests.make_402_payment(resp, 200)
    print(req_headers)

    return json.dumps(req_headers)
    # return Response(json.dumps(req_headers), status=200, mimetype='application/json')
    # return Response(response=json.dumps(req_headers), status=200, mimetype="application/json")
    # return flask.jsonify(**req_headers)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
