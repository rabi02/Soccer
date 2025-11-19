import requests
from bs4 import BeautifulSoup
import argparse
import mysql.connector
import certifi
import urllib3
import json
http = urllib3.PoolManager( cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
def ScrapData(url,HtmlElement,exemptField,scrap_type,HtmlElementType):
	final_result = []
	results =[]
	if scrap_type == 'API':
		response = requests.get(url)
		final_result = json.dumps(json.loads(response.text), indent=3)
	else:
		page = requests.get(url)
		soup = BeautifulSoup(page.content, "html.parser")
		if HtmlElementType == 'class':
			results = soup.find('table', class_=HtmlElement)
		if HtmlElementType == 'id':
			results = soup.find('table', id=HtmlElement)
		# print(url)
		print(HtmlElement)
		# print(exemptField)
		if results:
			final_result = GetScrapData(results,exemptField)
		else:
			headers = {
				'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
			}
			page = requests.get(url,headers=headers)
			soup = BeautifulSoup(page.content, "html.parser")
			results = soup.find('table', class_=HtmlElement)
			final_result = GetScrapData(results,exemptField)
		print(results)
	return final_result
def GetScrapData(results,exemptField):
	listarr =[]
	alldata =[]
	thDetail=[]
	if results:

		tr_results = results.find_all("tr")

		all_th =[]
		i =0
		ev_tr =tr_results[0]
		# for ev_tr in tr_results:
		if ev_tr.find_all("td") and i == 0:
			th_result = ev_tr
			thDetail = th_result.find_all("td")
			tr_results.remove(ev_tr)
			# print(thDetail)
			# for j in thDetail:
				
				#all_th.append(thDetail[j].text)

			pass
		elif ev_tr.find_all("th"):
			th_result = ev_tr
			all_th = th_result.find_all("th")
			tr_results.remove(ev_tr)
		else:
			tr_results.remove(ev_tr)
		i=i+1
		if len(thDetail)>0:
			all_th = thDetail
		lastMatch = len(tr_results)
		firstMatch = 1
		i = 0
		for i in range(firstMatch-1,lastMatch):
			all_td = tr_results[i].find_all("td")
			# print(all_td)
			eachrecord =[]
			for j in range(0,len(all_th)):
				eachcell =[]
				if j <=8:
					# print("++++++++++++++++++++++")
					# print(j)
					# print("****************************")
					# print(all_td[j])
					# print("-----------------------------")
					# text = all_td[j].text
					cellval={}
					allthName = all_th[j].text
					allthName =allthName.strip()
					try:
						
						# images = all_td[j].find('img')['src']
						# href_info = all_td[j].find("a")['href']
						# text = all_td[j].text
						# print(images,href_info,text)

						if all_td[j].find("img"):
							images = all_td[j].find('img')['src']
							# print(images)
							cellval['image']={'field_name':allthName,'value':images}
							# eachcell.append({'field_name':allthName,'value_type':'src','value':images})

						if all_td[j].find("a"):
							href_info = all_td[j].find("a")['href']
							text = all_td[j].text
							cellval['href']={'field_name':allthName,'value':href_info}
							# eachcell.append({'field_name':allthName,'value_type':'href','value':href_info,'text':text})
						
						if all_td[j].text:
							text = all_td[j].text.strip()
							# print(allthName+'-'+text.strip())
							cellval['text']={'field_name':allthName,'value':text}
							# eachcell.append({'field_name':allthName,'value':text.strip()})
						eachcell.append(cellval)	
						eachrecord.append(eachcell)
					except NameError:
						print(NameError)
					except:
						print('error')

			alldata.append(eachrecord)
	return alldata	
def ScrapDatasoccerstats(url,HtmlElement,exemptField,scrap_type,HtmlElementType):
	final_result = []
	results =[]
	new_result =[]
	page = requests.get(url)
	soup = BeautifulSoup(page.content, "html.parser")
	
	if HtmlElementType == 'class':
		results = soup.find('div', class_=HtmlElement)
		if results:
			new_result = results.find_all("table")
	if HtmlElementType == 'id':
		results = soup.find('table', id=HtmlElement,cellpadding='2')
		if results:
			new_result = results.find("table")
		
		
		# print(offers)
		# results =results.find("span").renderContents()
			
			
		# print("----------------------------------------")
		# print(results)
		# print("/////////////////////////////////////////")

	
	# print(HtmlElement)
	# print(exemptField)
	# print(results)
	if new_result:
		final_result = GetScrapData(results,exemptField)
		

	else:
		headers = {
			'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
		}
		page = requests.get(url,headers=headers)
		soup = BeautifulSoup(page.content, "html.parser")
		results = soup.find('table', class_=HtmlElement)
		final_result = GetScrapData(results,exemptField)
	# print(final_result)
	return final_result
def ScrapStatisticDatasoccerstats(url):
	keyname=['Goals scored','Goals conceded','Goals conceded per match']
	cssHtmlElement=['trow2','trow3']
	final_result = []
	results =[]
	new_result =[]
	page = requests.get(url)
	soup = BeautifulSoup(page.content, "html.parser")
	results = soup.find('table',cellpadding='0')
	if results:
		eachrecord =[]
		for jk in range(0,len(cssHtmlElement)):
			for row in soup.find_all('tr', class_=cssHtmlElement[jk]):
				for k in range(0,len(keyname)):
					
					if keyname[k] in row.text:
						# print(row)
						all_td = row.find_all("td")
						# print(all_td)
						cellval={}
						for j in range(0,len(all_td)):
							# print(keyname[k])
							if j == 0:
								cellval['scoring'] =all_td[j].text.strip()
							if j == 1:
								cellval['home'] =all_td[j].text.strip()
							if j == 2:
								cellval['away'] =all_td[j].text.strip()
							if j == 2:
								cellval['all'] =all_td[j].text.strip()
						eachrecord.append(cellval)
			
	return eachrecord
def ScrapFootballdataCoUk(url):
	import csv
	import urllib2
	page = requests.get(url)
	soup = BeautifulSoup(page.content, "html.parser")
	results = soup.find('table')
	if results:
		tr_results = results.find_all("tr")
		lastMatch = len(tr_results)
		firstMatch = 1
		i = 0
		eachrecord =[]
		for i in range(firstMatch-1,lastMatch):
			all_td = tr_results[i].find_all("td")
			print(all_td[0].text)
			href_info = all_td[1].find("a")['href']
			print(href_info)
			print(all_td[1].text)


			url = 'https://www.football-data.co.uk/'+href_info
			response = urllib2.urlopen(url)
			cr = csv.reader(response)

			for row in cr:
				print (row)
	return 1

def ScrapFromOddsPortal(url):
	import csv
	import urllib2
	page = requests.get(url)
	soup = BeautifulSoup(page.content, "html.parser")
	results = soup.find('table')
	if results:
		tr_results = results.find_all("tr")
		lastMatch = len(tr_results)
		firstMatch = 1
		i = 0
		eachrecord =[]
		for i in range(firstMatch-1,lastMatch):
			all_td = tr_results[i].find_all("td")
			print(all_td[0].text)
			href_info = all_td[1].find("a")['href']
			print(href_info)
			print(all_td[1].text)
			for row in cr:
				print (row)
	return 1

def ScrapFromOddsPortalPagination(url):
	final_result = []
	results =[]
	new_result =[]
	page = requests.get(url)
	print(url)
	soup = BeautifulSoup(page.content, "html.parser")
	results = soup.find('div')
	# final_result = GetScrapData(results,exemptField)
	print(results)
	return results

