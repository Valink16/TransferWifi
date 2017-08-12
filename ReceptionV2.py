import socket
from os import getcwd,chdir
from fonctionPratiques import *
from sys import getsizeof
from time import time
client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ip=input('IP:')
port=int(input("PORT:"))
client.connect((ip,port))
print('[*]Connected')
fichier=bytes()
recu=client.recv(1024).decode("utf-8")
taille,ext=recu.split(',')
taille=int(taille)
tailleRecu=0
print("The length of {} is {} bytes\n[*]Receiving...".format(ext,taille))
stop=False
debut=time()
while(not(stop)):
	recu=client.recv(taille)
	tailleRecu=getsizeof(fichier)
	if(recu==b'stop' or recu==b''):
		fichier+=recu
		break
	fichier+=recu
	print('\r{}/{}'.format(tailleRecu,taille),end='')
print('\r{}/{}'.format(tailleRecu,taille))
print('[*]All received !')
duree=time()-debut
print('Speed: {} B/s'.format(float(taille)/duree))
print("Print received file?(may be unreadable)(o/N)")
if(Rep1_0()==True):
	print(fichier)
else:
	print("[*]Not printing")
print("Save reveived file?")
if(Rep1_0()==True):
	print("Enter path for saving(enter # if you want to save {})".format(getcwd()))
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
