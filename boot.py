import ugit
import network
import os
import urequests
import json
import hashlib
import binascii
import machine
import time
import network
import main as mainScript
    
    
def main():
    ugit.wificonnect()
    ugit.pull_all()
    print("pulled done")
    mainScript.main()
    
if __name__ == "__main__":
    main()






