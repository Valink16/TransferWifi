from myLib import *
import ReceptionV2,EnvoiV2
print("Send or Receive ?: ")
ch=input().upper()
if(ch=="R"):
    ReceptionV2.recv()
elif(ch=="S"):
    EnvoiV2.send()
