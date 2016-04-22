#!/usr/bin/env python3
import sys
from flask import Flask, request, Response
import json
import subprocess

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

@app.route('/', methods=['GET', 'POST'])
def root():
    return """Welcome to your 21 Bitcoin Computer, a.k.a. your payment headers generator!<br/>
           <br/>Get the status of your bitcoin wallet by making a GET request to /status.
           <br/>Get payment headers by making a POST request to /headers, with instruction headers from the payable service included in the body of your request."""

@app.route('/status')
def status():
    p = subprocess.Popen(['21', 'status'], stdout=subprocess.PIPE)
    out = p.communicate()
    print("\nGot status!")
    return out

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True, ssl_context=(
        '/home/twenty-client/scripted/root-CA/server.crt',
        '/home/twenty-client/scripted/root-CA/server.key'
    ))
