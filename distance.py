#!/usr/bin/env python3

# PYTHON_ARGCOMPLETE_OK

import requests
import argparse
import argcomplete
import json

from utils import get_secret

API_KEY = get_secret('google')

def main():
	parser = argparse.ArgumentParser('Calculate distance from one address to multiple addresses')

	parser.add_argument('origin')
	parser.add_argument('destinations', nargs='+')
	parser.add_argument('--mode', default='walking', choices=['driving', 'walking', 'bicycling', 'transit'])
	parser.add_argument('--lang', default='en')
	parser.add_argument('--reverse', action='store_true')

	argcomplete.autocomplete(parser)

	args = parser.parse_args()

	origins = args.origin
	destinations = '|'.join(args.destinations)

	response = requests.request('GET', f'https://maps.googleapis.com/maps/api/distancematrix/json?' +
									   f'units=metric&key={API_KEY}&language={args.lang}' +
									   f'&origins={origins}&destinations={destinations}')

	response.raise_for_status()

	content = json.loads(response.text)

	if content['status'] != "OK":
		print(response.text)
		raise ValueError("Response status invalid")


	results = zip(content['destination_addresses'], content['rows'][0]['elements'])
	
	results = sorted(results, key=lambda x: x[1]['duration']['value'], reverse=args.reverse)

	print('\n'.join([f'{dest} | {result["duration"]["text"]} ({result["distance"]["text"]})' for dest, result in results]))


if __name__ == '__main__':
	main()
