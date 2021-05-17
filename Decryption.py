import os
from pymongo import MongoClient

try:
  from Crypto.Cipher import AES
except ImportError:
  print("Trying to Install required module: pycrypto\n")
  os.system('python -m pip install pycrypto')

try:
  import hashlib
except ImportError:
  print("Trying to Install required module: Hashlib\n")
  os.system('python -m pip install hashlib')

import time

start_time = time.time() # start of execution

password1="EXTC-@2021".encode()
key1=hashlib.sha256(password1).digest()

password2="Vesit@2021".encode()
key2=hashlib.sha256(password2).digest()

mode=AES.MODE_CBC   #Block cipher mode
IV='This is an IV456'  #Initialization vector should be 16 bytes only

cipher1=AES.new(key1,mode,IV)
cipher2=AES.new(key2,mode,IV)


###########################mongoDB##################3

client=MongoClient("Enter you mongo db connection string")

db=client.get_database('Encryption_db')

records=db.ENC_FILE


enc1=records.find_one({"id":"enc1"})

encrypted_file1=enc1["data"]


enc2=records.find_one({"id":"enc2"})

encrypted_file2=enc2["data"]



################Decrypt the Encrypted files ##################################################

decrypted_message1=cipher1.decrypt(encrypted_file1)
decrypted_message2=cipher2.decrypt(encrypted_file2)

#################Removing padding ############################################################
decrypted_message1=decrypted_message1.rstrip(b'0')
decrypted_message2=decrypted_message2.rstrip(b'0')

decrypted_message=decrypted_message1+decrypted_message2

#########################Ex-Or operation##########################################################
Ex_Or_key=22
decrypted_message = bytearray(decrypted_message)
for index, values in enumerate(decrypted_message): 
    decrypted_message[index] = values ^ Ex_Or_key  



#############Store decrypted file in .jpg or .png format############################

with open(r'C:\Users\sushant shelar\Desktop\Final Encryption Decryption\oooWebHost\New.jpg','wb') as e:
    e.write(decrypted_message)

end_time = time.time()

print('Execution time (s): ',end_time-start_time)

#dnspython
