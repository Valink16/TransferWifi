from myLib import *
import ReceptionV2,EnvoiV2
print("(S)end or (R)eceive ?: ")
ch=input().upper()
if(ch=="R"):
    ReceptionV2.recv()
elif(ch=="S"):
    EnvoiV2.send()
