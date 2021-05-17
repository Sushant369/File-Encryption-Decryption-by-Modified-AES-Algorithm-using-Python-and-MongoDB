from pymongo import MongoClient

# https://www.youtube.com/watch?v=VQnmcBnguPY

import base64 
#OOOWeb Host connection
import requests
from bs4 import BeautifulSoup
import json

import os
try:
  from Crypto.Cipher import AES
except ImportError:
  print("Trying to Install required module: pycrypto\n")
  os.system('python -m pip install pycrypto')

import hashlib
import time

def pad_file(file_name):
    while len(file_name) % 16 !=0:
        file_name = file_name + b'0'
    return file_name

start_time = time.time() # start of execution

#############Generating Two Keys 10 bytes #########################################################
password1="EXTC-@2021".encode()
key1=hashlib.sha256(password1).digest()

password2="Vesit@2021".encode()
key2=hashlib.sha256(password2).digest()

mode=AES.MODE_CBC   #Block cipher mode
IV='This is an IV456'  #Initialization vector should be 16 bytes only

###########Creating object of AES Algorithm################################################

cipher1=AES.new(key1,mode,IV)
cipher2=AES.new(key2,mode,IV)

########################Load image#########################################################

with open(r'C:\Users\sushant shelar\Desktop\Final Encryption Decryption\DSC_0927.JPG','rb') as  f:
    orig_file=f.read()

# print(len(orig_file))

#########################Ex-Or operation##########################################################
Ex_Or_key=22
image = bytearray(orig_file)
for index, values in enumerate(image): 
    image[index] = values ^ Ex_Or_key  


#########################converting byte array to  bytes##########################################
orig_file=bytes(image)
# print("after exor ",type(orig_file))

#########################Split image into two parts###############################################
data1=orig_file[0:len(orig_file)//2]

data2=orig_file[(len(orig_file)//2):]


######performing padding operation because the data should be in multiple of 16 bytes ###########

data1=pad_file(data1) ##Data1 must be in multiple of 16
data2=pad_file(data2) ##Data2 must be in multiple of 16


###################Encrypt two part with different keys #########################################
encrypted_data1 = cipher1.encrypt(data1)
encrypted_data2 = cipher2.encrypt(data2)


# mongodb+srv://test:test@cluster0.cz8rm.mongodb.net/Encryption_db?retryWrites=true&w=majority

client=MongoClient("mongodb+srv://test:test@cluster0.cz8rm.mongodb.net/Encryption_db?retryWrites=true&w=majority")

db=client.get_database('Encryption_db')

records=db.ENC_FILE

# print(records.count_documents({}))

new1={"id":"enc1", "data":encrypted_data1}
new2={"id":"enc2", "data":encrypted_data2}

# response1=records.insert_one(new1)
# response2=records.insert_one(new2)

# print(response1)
# print(response2)


Enc1_update ={"data":encrypted_data1}
Enc2_update ={"data":encrypted_data2}
records.update({"id":"enc1"},{'$set':Enc1_update})
records.update({"id":"enc2"},{'$set':Enc2_update})

print("Encrypted data uploaded successfully on MongoDb Atlas Server")

end_time = time.time()

print('Execution time (s): ',end_time-start_time)