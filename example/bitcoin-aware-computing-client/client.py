import json
import time
import subprocess

import two1.commands.status
from two1.lib.server import rest_client
from two1.commands.config import TWO1_HOST
from two1.commands.config import Config
from two1.lib.wallet import Wallet
from two1.lib.bitrequests import BitTransferRequests

# set up wallet proxy
wallet = Wallet()

# read local user account data
config = Config()
username = Config().username

# initialize rest client to communicate with 21.co API
client = rest_client.TwentyOneRestClient(TWO1_HOST, config.machine_auth, config.username)

# set up bitrequests client using BitTransfer payment method for managing 402 requests
requests = BitTransferRequests(wallet, username)

# check the spot price for our API call
response = requests.get_402_info(url='http://localhost:5000/fastfind')
endpoint_info = dict(response)
price = int(endpoint_info['price'])
print(endpoint_info)

# sample data
data1 = [
	{'height': 4},
	{'height': 3},
	{'height': 6},
	{'height': 4},
	{'height': 3},
	{'height': 6},
	{'height': 4},
	{'height': 3},
	{'height': 6},
	{'height': 10},
]

# slow local method
t0 = time.time()
a = get_element(data1, 'height', 10)
t1 = time.time()

# print results of local call
print(a)
print("Execution time: " + str(t1-t0))

# accelerated method

# get user's 21.co balance
bal = client.get_earnings()
twentyone_balance = bal["total_earnings"]

t0 = time.time()
if twentyone_balance > price:
	a = fast_get_element(data1, 'height', 10)
else:
	a = get_element(data1, 'height', 10)

t1 = time.time()
print(a)
print("Execution time: " + str(t1-t0))

# slow local method
def get_element(arr, prop, val):
	for elem in arr:
		if elem[prop] == val:
			return elem
		time.sleep(1)

# fast bitcoin-aware api Nox
def fast_get_element(arr, prop, val):
	body = {
		'array': json.dumps(arr),
		'property': prop,
		'value': val
	}
	res = requests.post(url='http://localhost:5000/fastfind', data=body)
	return json.loads(res.text)['elem']
