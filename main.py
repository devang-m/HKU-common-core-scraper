
from bs4 import BeautifulSoup
import requests
import re
from urllib.parse import urljoin # For joining next page url with base url
import smtplib
import time
import os

# The notifier function
def notify(title, text):
	os.system("""
	      osascript -e 'display notification "{}" with title "{}" sound name "Glass"'
	      """.format(text, title))

# Calling the function
mail = smtplib.SMTP('smtp.gmail.com',587)
mail.ehlo()
mail.starttls()
#Give your gmail id and password to get email notification when a course is available(senderemail,senderpassword)
mail.login('','')

def scrape():

	available=[]
	#URL of the stats page of courses. May change with time. Update of required.
	url="https://sweb.hku.hk/ccacad/ccc_appl/enrol_stat.html"
	response = requests.get(url)
	soup = BeautifulSoup(response.text, "html.parser")

	#Fill in the course code that you are interested in.
	courses=['CCGL9042','CCGL9020','CCGL9013','CCCH9015','CCCH9032','CCGL9042','CCHU9062','CCHU9021']

	for tr in soup.find_all('tr'):


		tds = tr.find_all('td')
		if (tds[0].get_text() in courses) and (tds[2].get_text() in ['A','B','C','D']):


			if (int(tds[4].get_text())- int(tds[5].get_text())>0):
				print (tds[0].get_text(),tds[4].get_text(),tds[5].get_text())
				available.append(tds[0].get_text()+" "+tds[4].get_text()+"  "+tds[5].get_text())
				notify(title    = 'Course',text  = tds[0].get_text()+" "+tds[4].get_text()+"  "+tds[5].get_text())
				
	if (available !=[]):
		content = str(available)
		# sender email as first agrument(same as filled above). Receiver email as second arguement
		mail.sendmail('senderid','receiver id',content) 
		print("Sent")
	time.sleep(120) #runs every two mins


while True:
	scrape()

mail.close()







