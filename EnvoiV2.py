def send():
    import socket
    import os
    from time import sleep,time
    from sys import getsizeof
    fichier=b''
    server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    nomFichier=input("Enter file name:")
    ext='.'+nomFichier.split(".")[1]
    with open(nomFichier, "rb") as file:
        print("[*]{} Open on rb".format(nomFichier))
        fichier=file.read()
    port = int(input("OPEN PORT:"))
    server.bind(('', port))
    server.listen(1)
    print("[*]Listening")
    client, infos=server.accept()
    print("[*]Someone just connected himself\n{} :{}".format(infos[0], infos[1]))
    print("[*]Length of opened file :{} bytes".format(getsizeof(fichier)))
    length=getsizeof(fichier)
    client.send((str(length)+','+ext).encode())
    print("[*]Sleeping for 0.5 second to be sure client is ready")
    sleep(1)
    print("[*]Sending...")
    temps=time()
    client.send(fichier)
    temps=time()-temps
    print('[*]Sended in {} seconds'.format(str(temps)[:5]))
    server.close()
    client.close()
