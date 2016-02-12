#!/usr/bin/env python3
from two1.commands.config import Config
from two1.lib.wallet import Wallet
from two1.lib.bitrequests import BitTransferRequests

EXAMPLE_SERVER = "http://127.0.0.1:5000"
PROXY = "http://127.0.0.1:9000"

proxies = {"http": PROXY}

wallet = Wallet()
username = Config().username
requests = BitTransferRequests(wallet, username)

print("Call the example server directly")
print("The goal here is to confirm that the example server is \
reachable and can distinguish between a proxied and non-proxied \
connection.")
r = requests.get(url=EXAMPLE_SERVER + "/AmIBehindProxy")
print(r.text)

print("Call the example debug server though the proxy, paying 1000 satoshis per request")
print("The goal here is to confirm that the example server was hit through a proxy.")
r = requests.get(url=EXAMPLE_SERVER + "/AmIBehindProxy", proxies=proxies)
print(r.text)

print("Now call a real server at princeton.edu by paying the proxy some bitcoin")
r = requests.get(url="https://www.princeton.edu", proxies=proxies)
# print(r.text)

# write output to file
with open('princeton.html', 'w') as f:
	f.write(r.text)
