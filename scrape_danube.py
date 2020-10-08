import shutil
import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import requests
import time
import re

browser = webdriver.Chrome()

def main():
	departments = []
	images = []
	titles = []
	prices = []
	base_url = "https://danube.sa"
	departments_url = "https://danube.sa/en/departments/"
	r = requests.get(departments_url)
	soup = BeautifulSoup(r.text, 'html.parser')
	for dept in soup.find_all('div', class_="department-box"):
		dept_name = dept.find('div', class_='department-box__title').text
		all_link = base_url + dept.find('a', class_="department-box__all-link").get("href")
		page = 1
		while(page < 100 and page != -1):
			browser.get(all_link+"?page="+str(page))
			try:
				WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'product-box')))
			except TimeoutException as ex:
				page = -1
				break
			all_soup = BeautifulSoup(browser.page_source, 'html.parser')
			for product in all_soup.find_all('div', class_="product-box"):
				departments.append(dept_name)
				product_tile = product.find('div', class_='product-box__name').text
				titles.append(product_tile)
				product_price = product.find('div', class_='product-price__current-price').text
				product_price = re.findall(r"(\d+\.\d{1,2})", product_price)[0]
				prices.append(product_price)
				image_url = re.findall(r'\(.*?\)', product.find('div', class_="product-box__image__element").get('style'))[0]
				image_url = image_url[1: len(image_url)-1]
				filename = "images/"+image_url.split("/")[-1]
				img_r = requests.get(image_url, stream = True)
				img_r.raw.decode_content = True
				with open(filename, 'wb') as f:
					shutil.copyfileobj(r.raw, f)
				images.append(filename)
			page+=1

	with open('danube_products.csv', 'w', newline='') as csv_file:
		fieldnames = ['department', 'image', 'title', 'price']
		writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
		writer.writeheader()
		index = 0
		while index < len(titles):
			try:
				writer.writerow({'department': departments[index], 'image': images[index], 'title': titles[index], 'price':prices[index]})
				print("INFO [Building CSV]: {:.2f}% complete".format((index/len(titles))*100))
				index += 1
			except Exception as e:
				print("ERROR: {}".format(e))
				print("INFO: ERROR AT INDEX {}".format(index))
	browser.close()
if __name__ == "__main__":
	main()