def Rep1_0():
	loopInput=True
	while(loopInput):
		reponse=input()
		if(reponse.upper()=="O"):
			loopInput=False
			return True
		elif(reponse.upper()=="N"):
			loopInput=False
			return False
		else:
			print("Entrez 'o' pour 'oui' ou 'n' pour 'non'")
