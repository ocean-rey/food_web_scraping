import requests # used to get the webpages and images from url
import re # used to clean price data
import shutil # used to save image file to disk
import csv # used to build csv file

def main():
	titles = []
	images = []
	prices = []
	brands = []
	variant = []
	i = 1
	total_pages = 2
	try:
		print("INFO: Starting scrape of tamimi food products")
		while i < total_pages:
			url = "https://website-api.ecom-dev.tamimimarkets.com/api/product?category=food--beverages&layoutType=GRID&loadMoreType=INFINITE&sorting=NEW_LAST&page="+str(i)
			r = requests.get(url)
			json_data = r.json()
			for value in json_data['data']['product']:
				brand = value['brand']['name']
				print(brand)
				name = value['name']
				print(name)
				for variant in value["variants"]:

			print("INFO [Scraping Data]: {:.2f}% complete".format((i/total_pages)*100))
			i+=1
	except Exception as e:
		print("ERROR: {}".format(e))
	print("INFO: Scraping completed")
	print("INFO: Writing CSV to file...")
	with open('tamimi_food_products.csv', 'w', newline='') as csv_file:
		fieldnames = ['title', 'image', 'price']
		writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
		writer.writeheader()
		index = 0
		while index < len(titles):
			try:
				writer.writerow({'image': images[index], 'title': titles[index], 'price': prices[index]})
				print("INFO [Building CSV]: {:.2f}% complete".format((index/len(titles))*100))
				index += 1
			except Exception as e:
				print("ERROR: {}".format(e))
				print("INFO: ERROR AT INDEX {}".format(index))
				print("titles[{}] = {}".format(index, titles[index]))
				print("images[{}] = {}".format(index, images[index]))
				print("prices[{}] = {}".format(index, prices[index]))


if __name__ == "__main__":
	main()