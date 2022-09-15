# -*- coding: utf-8 -*-
from BeautifulSoup import BeautifulSoup
import codecs
import sqlite3
from os import listdir
from os.path import isfile, join

filename='input\index.html'

connnection = sqlite3.connect('test.db')
print "Opened database successfully";
conn = connnection.cursor()
conn.execute('''CREATE TABLE ILAC
       (ID INTEGER PRIMARY KEY     AUTOINCREMENT,
       ADI           CHAR(50)    NOT NULL,
       HAL            CHAR(50)     NOT NULL,
	   KULLANIM         TEXT		NOT NULL,
	   ENDIKASYON         TEXT		NOT NULL,
	   KONTRENDIKASYON         TEXT		NOT NULL,
	   UYARI      		TEXT		NOT NULL,
	   ETKILESIM         TEXT		NOT NULL);''')
	   
conn.execute('''CREATE TABLE ETKEN
       (ID INTEGER PRIMARY KEY     AUTOINCREMENT,
       ADI           CHAR(200)    NOT NULL,
       ADI_ID           INTEGER    NOT NULL);''')
	   
conn.execute('''CREATE TABLE PIYASA
       (ID INTEGER PRIMARY KEY     AUTOINCREMENT,
       ADI           CHAR(200)    NOT NULL,
       ADI_ID           INTEGER    NOT NULL);''')
print "Table created successfully";

tablo_index = 0
ADI = ""
HAL = ""
ERKEN = ""
PIYASA = ""
KULLANIM = ""
ENDIKASYON = ""
KONTRENDIKASYON = ""
UYARI = ""
ETKILESIM = ""

onlyfiles = [f for f in listdir('input') if isfile(join('input', f))]

for file in onlyfiles:
	filename = 'input\\' + str(file)

	try:
		filehandle = codecs.open(filename)
	except:
		print("Could not open file " + filename)
		quit() 
		
	cursor = conn.execute('SELECT max(ID) FROM ILAC')
	max_id = cursor.fetchone()[0]

	tablo_index = max_id
	
	if tablo_index == None :
		tablo_index = 0

	text = filehandle.read().split("\n",1)[1]
	text = "<!DOCTYPE html>\n" + str(text)
	filehandle.close()

	html =  text 
	son = ""
	invalid_tags = ['a']
	soup = BeautifulSoup(html )

	for tag in invalid_tags: 
		for match in soup.findAll(tag):
			match.replaceWithChildren()

	text = soup.prettify('utf-8')
	text = text.replace('&nbsp;', ' ').replace("\n", "").replace("\t", "").replace("          ", "").replace('    ', '').replace('\n', ' ').replace('\r', '')		
	soup = BeautifulSoup(text)
	son = soup.findAll("span", { "class" : "style16" })
	son2 = soup.findAll("span", { "class" : "style17" })
	text = ""
	baslik = ''
	icerik = ''

	for name in soup.findAll('title'):
		baslik = name.findAll(text=True)[0].strip()
		try:
			icerik = baslik[baslik.find("(")+1:baslik.find(")")].strip()
		except:
			icerik = ''
		finally:
			baslik =baslik[:baslik.find("(")].strip()
		
	text =baslik + ' ' +icerik +'\n' 

	ADI = baslik.replace('&#39;', ' ').replace('\'', '"').encode("utf-8")
	HAL = icerik.replace('&#39;', ' ').replace('\'', '"').encode("utf-8")

	i = 0
	for name in soup.findAll('span'):
		if name.has_key('class'):
			if name['class'] == "style17":
				t= name.findAll(text=True)
				try:
					t = t[0].strip()
				except:
					t = ""
				text = text +'!!!!!'+t + '\n'
				i += 1
				
			elif name['class'] == "style16":
				t= name.findAll(text=True)
				try:
					t = t[0].strip()
				except:
					t = ""
				text = text +t + '\n'
				if i ==1:
					string = "INSERT INTO ETKEN (ADI,ADI_ID) VALUES ('"+t.replace('&#39;', ' ').replace('\'', '"').encode("utf-8")+"', "+str(tablo_index)+")"
					print string
					conn.execute(string);
				if i ==2: 
					string = "INSERT INTO PIYASA (ADI,ADI_ID) VALUES ('"+t.replace('&#39;', ' ').replace('\'', '"').encode("utf-8")+"', "+str(tablo_index)+")"
					print string
					conn.execute(string);
				if i ==3:
					KULLANIM = t.replace('&#39;', ' ').replace('\'', '"').encode("utf-8")
				if i ==4:
					ENDIKASYON = t.replace('&#39;', ' ').replace('\'', '"').encode("utf-8")
				if i ==5:
					KONTRENDIKASYON = t.replace('&#39;', ' ').replace('\'', '"').encode("utf-8")
				if i ==6:
					UYARI = t.replace('&#39;', ' ').replace('\'', '"').encode("utf-8")
				if i ==7:
					ETKILESIM = t.replace('&#39;', ' ').replace('\'', '"').encode("utf-8")

	string = "INSERT INTO ILAC (ADI,HAL,KULLANIM,ENDIKASYON,KONTRENDIKASYON,UYARI,ETKILESIM) \
		  VALUES ('"+ADI+"','"+HAL+"','"+KULLANIM+"','"+ENDIKASYON+"','"+KONTRENDIKASYON+"','"+UYARI+"','"+ETKILESIM+"')"
	conn.execute(string);	
	connnection.commit()
connnection.close()
