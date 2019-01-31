import socket
import os
from myLib import log
from time import sleep,time
from sys import getsizeof
def send():

    fichier=b''
    server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    nomFichier=input("Enter file name: ")
    ext='.'+nomFichier.split(".")[1]
    with open(nomFichier, "rb") as file:
        log("{} Open on rb".format(nomFichier))
        fichier=file.read()
    port = int(input("OPEN PORT: "))
    server.bind(('', port))
    server.listen(1)
    log("Listening")
    client, infos=server.accept()
    log("Someone just connected\n{} :{}".format(infos[0], infos[1]))
    log("Length of opened file :{} bytes".format(getsizeof(fichier)))
    length=getsizeof(fichier)
    client.send((str(length)+','+ext).encode())
    log("Sleeping for 0.5 second to be sure client is ready")
    sleep(1)
    log("Sending...")
    temps=time()
    client.send(fichier)
    temps=time()-temps
    log('Sended in {} seconds'.format(str(temps)[:5]))
    server.close()
    client.close()
