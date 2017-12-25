import netifaces
import subprocess
from threading import Thread
from time import sleep
def ask(msg,pos,neg):
	#simple neg or pos answer asking function
	#args must be string type
	loopInput=True
	while(loopInput):
		reponse=input(msg)
		if(reponse.upper()==pos.upper()):
			return True
		elif(reponse.upper()==neg.upper()):
			return False
		else:
			print("Enter {} or {}".format(pos,neg))

def getBroadcast():
	"""
	This function finds the broadcast of the user's interface.
	An example of broadcast : 192.168.43.255 #In a broadcast,  255 can be replaced by 2-254, not 1 because it's usually the router
	"""
	interfaces=netifaces.interfaces()
	log("Chose a network interface please.",True)
	for a,i in enumerate(interfaces): #We print the list of interfaces
		print("[{}]:{}".format(a,i))
	interNo=int(input())
	if(interfaces[interNo]=="lo"): #if the user choses the loopback interface, we assume that ip=localhost/127.0.0.1
		return "127.0.0.1"
	interInfos=netifaces.ifaddresses(interfaces[interNo])
	try: #We use a try block because some interfaces don't have the wanted ipv4Infos
		ipv4Infos=interInfos[netifaces.AF_INET]
		return ipv4Infos[0]["broadcast"][:11] # [:11] because we just need the 3 first digits.
	except:
		log("This interface can't be used.",True)
		return -1
def log(str,returnLine=True):
	finalStr="[*]"+str
	if(returnLine):
		finalStr+="\n"
	print(finalStr,end="")

def my_nmap(args,ipRangeStr,prCmd=False): # Simply excecutes a command and returns the output
	"""
	This just runs nmap with some args.
	RETURN : a String containing nmap's output
	"""
	cmd="nmap "+args+" "+ipRangeStr
	if(prCmd):
		print(cmd)
	resCmd=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
	res, placeholder=resCmd.communicate()
	res=res.decode()
	return res

def getIps(res): # Here we search for detected IPs on the local network in a loop
	"""
	This function gets the ip and host name information from the res String var.
	res contains the output of a nmap command.
	nmap is launched by "my_nmap" function.
	RETURN : 2 tables, the 1st contains hostNames and the 2nd the IPs.
	"""
	resTab=res.split("\n")
	ChoiceTab=[]
	ipTab=[]
	for l in resTab:
		if(l.startswith("Nmap scan report for")): #What we search
			name=l[21:]
			nameCpy=name
			try: #We handle an IndexError here *[*read down*]*
				ip=name.split(" ")[1]# There will be an IndexError because ip will not have " " in it and split will return a 1 length table
				name=name.split(" ")[0] #ip will not have " " if nmap didn't find the name because nmap prints the hostname+" "+ip
				ChoiceTab.append(name)
				ip=ip[1:len(ip)-1]
				separatedIp=ip.split(".")
				ip=""
				for part in separatedIp:
					ip+="."+str(part)

				ip=ip[1:]
				ipTab.append(ip)
			except IndexError:
				ipTab.append(nameCpy)
				ChoiceTab.append("UNKNOWN")


	return ChoiceTab,ipTab

def getPort(ip,portRange):
	res=my_nmap("-p "+portRange,ip,False)
	resTab=res.split("\n")
	openPorts=[]
	for lnumber,l in enumerate(resTab):
		if(l.startswith("PORT")):
			portStartLine=lnumber # We will use this in the next for loop
			break

	for portInfos in resTab[portStartLine:]:
		print(portInfos)

class loadingThread(Thread):
	def __init__(self):
		Thread.__init__(self)
		self.loadIndex=0
		self.loadingText=["-","\\","|","/"]
		self.running=True
	def run(self):
		while(self.running):
			print("\rSearching... {}".format(self.loadingText[self.loadIndex]),end="")
			self.loadIndex+=1
			if(self.loadIndex>3):
				self.loadIndex=0
			sleep(0.5)
		print("")
