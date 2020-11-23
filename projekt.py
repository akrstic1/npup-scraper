from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
from time import sleep
import smtplib

email = "mojtestnimail097"
password = "testmail123#"
email_odrediste = "arno.krstic@gmail.com"

page_url = "https://studentskiservis.unizd.hr/poslovi"

def dohvatiHtml():
	urlClient = urlopen(page_url)

	psoup = soup(urlClient.read(), "html.parser")
	urlClient.close()

	return psoup

def dohvatiOglase(psoup):
	lista_oglasa = []

	#Nadi sve oglase
	oglasi = psoup.find("div", class_="edn__articleListWrapper edn_18193_article_list_wrapper").findAll("div", class_="edn-item")

	for oglas in oglasi:

		#Dohvati naslov,opis,link
		naslov = oglas.find("a", class_="c-item__link-title").text
		opis = oglas.find("div", class_="c-item__summary o-text-body c-contents__content").p.text
		link = oglas.find("a", class_="c-item__link-title").get("href")

		#Pospremi u listu
		lista_oglasa.append([naslov,opis,link])	

	return lista_oglasa

def saljiMail(oglas):
	with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
		smtp.ehlo()
		smtp.starttls()
		smtp.ehlo()

		smtp.login(email, password)

		subject = "NOVI OGLAS!!!"
		body = "Naslov: " + oglas[0] + "\nOpis: " + oglas[1] + "\nLink: " + oglas[2]

		msg = f'Subject: {subject}\n\n{body}'

		smtp.sendmail(email, email_odrediste, msg.encode())


#################
#Inicijalizacija#
#################

psoup = dohvatiHtml()
lista_oglasa_start = dohvatiOglase(psoup)

###############
#Infinite loop#
###############
while True:
	#broj novih oglasa za ispis u konzolu
	novi_oglas = 0

	#Scrapeamo oglase za usporedbu sa prošlima
	psoup = dohvatiHtml()
	lista_oglasa = dohvatiOglase(psoup)

	lista_oglasa[0][0] = "promjena"
	lista_oglasa[2][1] = "test"

	#Prodi kroz sve oglase
	for oglas in lista_oglasa:
		#Podudaraju li se novi oglasi sa starim,
		#u slučaju da se ne podudara znači da je novi oglas, šalji mail
		if(oglas not in lista_oglasa_start):
			novi_oglas += 1

			print("Novi oglas: ", oglas[0], "\nOpis: ", oglas[1], "\nLink:", oglas[2])
			saljiMail(oglas)

	print("Broj novih oglasa: ", novi_oglas)
	#Postavimo listu za usporedbu na novo pronađene oglase
	lista_oglasa_start = lista_oglasa

	#20 sekundi pauza
	sleep(20)


