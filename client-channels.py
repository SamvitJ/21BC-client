#!/usr/bin/env python3
import json
import sys

from two1.lib.wallet import Wallet
from two1.lib.bitrequests import ChannelRequests

def main (argv):
	wallet = Wallet()
	requests = ChannelRequests(wallet)

	url = 'http://10.8.235.166:5000/%s' % (argv[1] if len(argv) > 1 else '')

	# Set up a micropayment channel.
	info = requests.get_402_info(url=url)
	for key, val in info.items():
		print('{}: {}'.format(key, val))

	# Make many requests in the channel and print balance
	queries = ("Bitcoin", "Blockchain", "Satoshi")
	for ii in range(3):
	 	results = requests.post(url=url, data=dict(query=queries[ii]))
	 	print(json.loads(results.text))

	r = requests.get(url=url)
	print(r.text)

if __name__ == "__main__":
	main(sys.argv)
