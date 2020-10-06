import requests
from bs4 import BeautifulSoup
import re
# collect image, title, price as per yusras request

def main():
	titles = []
	images = []
	prices = []
	i = 1
	try:
		while i < 18:
			url = "http://www.panda.com.sa/stores/riyadh/food-products.html?p="+str(i)
			print(url)
			r = requests.get(url)
			soup = BeautifulSoup(r.text, 'html.parser')
			for product in soup.find_all("div", class_="product-block"):
				# get image from the thingy
				image = product.find_all("a", class_="product-zoom")[0].get('href')
				print(image)
				images.append(image)
				#get title from the thingy
				title = product.find_all("h3", class_="product-name")[0].a.contents[0]
				print(title)
				titles.append(title)
				# get price from the thingy 
				price = product.find_all("span", class_="price")[0].contents[0]
				match = re.match('([0-9]*.[0-9])')
				print (match.group(1))
				print(price)
				prices.append(price)
			i+=1
	except Exception as e:
		print("ERROR: {}".format(e))
	data = [titles, images, prices]
	print(data)

if __name__ == "__main__":
	main()