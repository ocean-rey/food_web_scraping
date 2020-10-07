import json
from algoliasearch.search_client import SearchClient

client = SearchClient.create('1D2IEWLQAD', '7e7fbc46b3453e0de73714946f7209f7')
index = client.init_index('spree_products')

def main():
	hits = []
	res = index.search('',{'hitsPerPage': 1000, 'page': 0})
	for hit in res['hits']:
		hits.append(hit)
	with open('danube.json', 'w') as f:
		json.dump(hits, f)
	


if __name__ == "__main__":
	main()