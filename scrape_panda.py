import requests # used to get the webpages and images from url
import re # used to clean price data
import shutil # used to save image file to disk
import csv # used to build csv file
from bs4 import BeautifulSoup # used to scrape site

def main():
	titles = []
	images = []
	prices = []
	i = 1
	total_pages = 20
	try:
		print("[INFO]: Starting scrape of Panda food products")
		while i < total_pages:
			url = "http://www.panda.com.sa/stores/riyadh/food-products.html?p="+str(i)
			r = requests.get(url)
			soup = BeautifulSoup(r.text, 'html.parser')
			for product in soup.find_all("div", class_="product-block"):
				# get image from the thingy
				image = product.find_all("a", class_="product-zoom")[0].get('href')
				filename = "images/"+image.split("/")[-1]
				img_r = requests.get(image)
				with open(filename, 'wb') as f:
					for chunk in img_r:
						f.write(chunk)
				images.append(filename)
				#get title from the thingy
				title = str(product.find_all("h3", class_="product-name")[0].a.contents[0])
				titles.append(title)
				# get price from the thingy 
				price = product.find_all("span", class_="price")[0].contents[0]
				pattern = r"(\d+\.\d{1,2})"
				price = re.findall(pattern, price)[0]
				prices.append(price)
			i+=1
	except Exception as e:
		print("ERROR: {}".format(e))
	print("[INFO]: Scraping completed")
	print("[INFO]: Writing CSV to file...")
	with open('panda_food_products.csv', 'w', newline='') as csv_file:
		fieldnames = ['title', 'image', 'price']
		writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
		writer.writeheader()
		index = 0
		while index < len(titles):
			try:
				writer.writerow({'image': images[index], 'title': titles[index], 'price': prices[index]})
				index += 1
			except Exception as e:
				print("ERROR: {}".format(e))
				print("INFO: ERROR AT INDEX {}".format(index))
	print("[INFO] Done.")

if __name__ == "__main__":
	main()