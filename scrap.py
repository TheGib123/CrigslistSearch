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
		self.name = name
		self.price = price
		self.link = link
		self.location = location
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
		#rewrite 
		name = ""
		price = ""
		link = ""
		location = ""
		image = ""
		
		try:
			name = str(i.find_element_by_class_name('result-title').text)
		except:
			name = "no name"
		try:
			price = str(i.find_element_by_class_name('result-price').text)
		except:
			price = "no price"
		try:
			link = i.find_element_by_tag_name('a')
			link = str(link.get_attribute('href'))
		except:
			link = "no link"
		try:
			image = i.find_element_by_tag_name('img')
			image = str(image.get_attribute('src'))
		except:
			image = "no image"			
		try:
			location = str(i.find_element_by_class_name('result-hood').text)
		except:
			try:
				location = str(i.find_element_by_class_name('nearby').text)
			except:
				location = "no location"
				
		if (image != "no image"):
			ad = AD(name, price, location, link, image)
			listOfAds.append(ad)	
				
				
		
# sends url with search criteria
def SearchItems(url):
	for i in searchList:
		if (i != '' and i != ' ' ):
			tempUrl = url.replace("query=", "query=" + i)
			tempUrl = tempUrl.replace(" ", "+")
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
		try:
			f.write("<div>")
			f.write("<a href='" + i.link + "'>")
			f.write("<img alt='' class='' src=" + i.image + ">")
			f.write("</a>")
			f.write("<p>" + i.name + "<br>")
			f.write(i.price + "<br>")
			f.write(i.location + "</p>")
			f.write("</div>")
		except:
			print ("1 ad failed")
		
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
	#PrintAds()
	numListOfAds = str(len(listOfAdsNoDup))
	print (numListOfAds + " ads found")
	WriteHTML()
	driver.close()
	
	
	
Main()	
	
	
	
	
	

	
	
