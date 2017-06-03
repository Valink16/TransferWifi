import socket
import os
import time
import sys
fichier=b''
server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)


print("Entrez le nom du fichier")
nomFichier=input()
ext='.'+nomFichier.split(".")[1]
with open(nomFichier, "rb") as file:
    print("[*]{} ouvert en rb".format(nomFichier))
    fichier=file.read()
    print(sys.getsizeof(fichier))

print('port:', end='')
port = int(input())
server.bind(('', port))
server.listen(1)
print("[*]Ecoute")
client, infos=server.accept()
print("[*]Un client vient de se connecter\n{} :{}".format(infos[0], infos[1]))
print("[*]Taille du fichier ouvert :{} octets".format(sys.getsizeof(fichier)))
print("Envoyer une confirmation au client?(o/N)")
choix=input().upper()
if (choix.upper()=="O"):
    length=sys.getsizeof(fichier)
    a=0
    client.send((str(length)+','+ext).encode())
    recuClient=client.recv(1024).decode()
    if(recuClient.upper()=='O'):
        print("[*]Initialisation de l'envoi")
        temps=time.time()
        client.send(fichier)
        temps=time.time()-temps
        print('[*]Envoye en {} secondes'.format(str(temps)[:5]))
else:
    client.send(b"N")
server.close()
client.close()
