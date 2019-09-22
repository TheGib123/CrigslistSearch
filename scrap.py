from selenium import webdriver
import time

# modify searchCity MAKE SURE STRING IS CORRECT
searchCity = ["https://joplin.craigslist.org/search/sso?sort=rel&query=", 
"https://springfield.craigslist.org/search/sso?sort=rel&query=",
"https://kansascity.craigslist.org/search/sso?sort=rel&query=",
"https://fayar.craigslist.org/search/sso?sort=rel&query=",
"https://fortsmith.craigslist.org/search/sso?sort=rel&query=",
"https://littlerock.craigslist.org/search/sso?sort=rel&query=",
"https://stlouis.craigslist.org/search/sso?sort=rel&query=",
"https://tulsa.craigslist.org/search/sso?sort=rel&query=",
"https://oklahomacity.craigslist.org/search/sso?sort=rel&query="]





driver = webdriver.Chrome()		#starts chrome
searchList = []                 #all things you want to search for
listOfAds = []					#all adds
listOfAdsNoDup = []				#adds with removed duplicites
numListOfAds = ""				#show length of listofAdsNoDup


# class for craigslist ad
class AD:
	def __init__(self, name, price, location, link, image):
		self.name = name.text
		self.price = price.text
		self.link = link.get_attribute('href')
		try:
			self.location = location.text
		except:
			try:
				self.location = location.text
			except:
				self.location = location
		try:
			self.image = image.get_attribute('src')
		except:
			self.image = image

# prints ads in console
def PrintAds():
	for i in listOfAdsNoDup:
		print(i.name)
		print(i.price)
		print(i.location)
		print(i.link)
		print(i.image)
		print()

# searches the url for ads
def SearchPage(url):	
	driver.get(url)
	a = driver.find_elements_by_class_name("result-row");
	for i in a:
		name = i.find_element_by_class_name('result-title')
		price = i.find_element_by_class_name('result-price')
		link = i.find_element_by_tag_name('a')
		location = ""
		image = ""
		try:
			location = i.find_element_by_class_name('result-hood')
		except:
			try:
				location = i.find_element_by_class_name('nearby')
			except:
				location = "no location"
		try:
			image = i.find_element_by_tag_name('img')
		except:
			image = "no image"
		if (image != "no image"):
			ad = AD(name, price, location, link, image)
			listOfAds.append(ad)		
	
# sends url with search criteria
def SearchItems(url):
	for i in searchList:
		tempUrl = url.replace("query=", "query=" + i)
		print(tempUrl)
		SearchPage(tempUrl)
		#time.sleep(1)

# sends each city url to SearchItems	
def SearchCitys():
	for i in searchCity:
		SearchItems(i)

# removes duplicites
def DeleteDuplicates():			
	seen_links = set()
	for obj in listOfAds:
		if obj.link not in seen_links:
			listOfAdsNoDup.append(obj)
			seen_links.add(obj.link)
			
# writes all ads to html file	
def WriteHTML():
	f = open("CraigslistAds.html", "w")

	f.write("<html>")
	f.write("<head>")
	f.write("</head>")
	f.write("<body style='text-align: center'>")
	f.write("<h4>" + numListOfAds + " ads found</h4>")
	for i in listOfAdsNoDup:
		f.write("<div>")
		f.write("<a href='" + i.link + "'>")
		f.write("<img alt='' class='' src=" + i.image + ">")
		f.write("</a>")
		f.write("<p>" + i.name + "<br>")
		f.write(i.price + "<br>")
		f.write(i.location + "</p>")
		f.write("</div>")
		
	f.write("</body>")
	f.write("</html>")
		
	f.close()

#get things needed to search and stores them in searchList	
def GetInput():
	print ("Type in each object you want to search for folled by ENTER. Or type done")
	while True:
		item = input()
		if (item != "done"):
			searchList.append(item)
		else:
			break

# start
def Main():	
	global numListOfAds
	GetInput()
	SearchCitys()
	DeleteDuplicates()
	numListOfAds = str(len(listOfAdsNoDup))
	print (numListOfAds + " ads found")
	WriteHTML()
	driver.close()
	
	
	
Main()	
	
	
	
	
	

	
	