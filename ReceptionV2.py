import socket
from os import getcwd,chdir
from myLib import *
from sys import getsizeof
from time import time
def recv():

	client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	loadThread=loadingThread()
	broadcast=-1
	while(broadcast==-1):
		broadcast=getBroadcast()

	if(broadcast=="127.0.0.1"):
		log("IP is set to localhost")
		ip=broadcast
	else:
		loadThread.start()
		res=my_nmap("-F",broadcast+"*")
		nTab, ipTab=getIps(res)
		loadThread.running=False #loadThread checks every loop if running is True, if not, stops.
		loadThread.join()
		for a,ip in enumerate(ipTab):
			print("[{}]{} : {}".format(a+1,nTab[a],ip))
		selectedIP=int(input("Chose an IP: "))-1
		ip=ipTab[selectedIP]

	port=int(input("PORT:"))
	client.connect((ip,port))
	print('[*]Connected')
	fichier=bytes()# Where received data will be stored
	recu=client.recv(1024).decode("utf-8")
	taille,ext=recu.split(',')#recu contains the length of file and file extension, separated by a comma
	taille=int(taille)
	tailleRecu=0
	print("The length of {} is {} bytes\n[*]Receiving...".format(ext,taille))
	stop=False
	debut=time()
	recCount=0
	while(not(stop)):
		recu=client.recv(1024*1024)
		tailleRecu=getsizeof(fichier)
		recCount+=1
		if(recu==b'stop' or recu==b''):
			fichier+=recu
			break
		fichier+=recu
		print('\r{}/{}'.format(tailleRecu,taille),end='')
	print('\r{}/{} in {} tries'.format(tailleRecu,taille,recCount))
	print('[*]All received !')
	duree=time()-debut
	print('Speed: {} B/s'.format(float(taille)/duree))
	print("Print received file?(may be unreadable)(o/N)")
	if(Rep1_0()==True):
		print(fichier)
	else:
		print("[*]Not printing")
	print("Save received file?")
	if(Rep1_0()==True):
		print("Enter path for saving(# = {})".format(getcwd()))
		chemin=input()
		if (not(chemin=="#")):
			chdir(chemin)
		print("Enter file name(without extension)")
		nomFichier=input()+ext
		with open(nomFichier,"wb") as file:
			file.write(fichier)
		print("[*]Saving done")
	print("[*]Bye !")
	client.close()
