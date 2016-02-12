#!/usr/bin/env python3
import sys

from two1.commands.config import Config
from two1.lib.wallet import Wallet
from two1.lib.bitrequests import BitTransferRequests

def main (argv):
	wallet = Wallet()
	username = Config().username
	requests = BitTransferRequests(wallet, username)

	r = requests.get(url='http://10.8.235.166:5000/%s' % (argv[1] if len(argv) > 1 else ''))
	print(r.text)

if __name__ == "__main__":
	main(sys.argv)
