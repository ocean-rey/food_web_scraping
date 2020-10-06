import requests # used to get the webpages and images from url
import re # used to clean price data
import shutil # used to save image file to disk
import csv # used to build csv file

def main():
	titles = []
	images = []
	prices = []
	brands = []
	variant_names = []
	i = 1
	total_pages = 100
	try:
		print("INFO: Starting scrape of tamimi food products")
		while i < total_pages:
			url = "https://website-api.ecom-dev.tamimimarkets.com/api/product?category=food--beverages&layoutType=GRID&loadMoreType=INFINITE&sorting=NEW_LAST&page="+str(i)
			r = requests.get(url)
			json_data = r.json()
			for value in json_data['data']['product']:
				brand = value['brand']['name'].strip()
				name = value['name'].strip()
				for variant in value["variants"]:
					brands.append(brand)
					titles.append(name)
					variant_name = variant["name"].strip()
					variant_names.append(variant_name)
					price = variant["storeSpecificData"][0]['mrp']
					prices.append(price)
					if variant['images'] is not None :
						image_url = variant['images'][0]
						filename = "images/"+image_url.split('/')[-1]
						img_r = requests.get(image_url, stream = True)
						img_r.raw.decode_content = True
						with open(filename, 'wb') as f:
							shutil.copyfileobj(r.raw, f)
						images.append(filename)
					else:
						## if this variant has no image, assume that the same image as
						## the previous variant is used. we don't bother redownloading it,
						## only maintatning the reference
						images.append(filename)
			print("INFO [Scraping Data]: {:.2f}% complete".format((i/total_pages)*100))
			i+=1
	except Exception as e:
		print("ERROR: {}".format(e))
	print("INFO: Scraping completed")
	print("INFO: Writing CSV to file...")
	with open('tamimi_food_products.csv', 'w', newline='') as csv_file:
		fieldnames = ['brand', 'variant', 'title', 'image', 'price']
		writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
		writer.writeheader()
		index = 0
		while index < len(titles):
			try:
				writer.writerow({'brand': brands[index], 'variant': variant_names[index],
					'image': images[index], 'title': titles[index], 'price': prices[index]})
				print("INFO [Building CSV]: {:.2f}% complete".format((index/len(titles))*100))
				index += 1
			except Exception as e:
				print("ERROR: {}".format(e))
				print("INFO: ERROR AT INDEX {}".format(index))


if __name__ == "__main__":
	main()