from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
import os
import mysql.connector

def connectToDB(hostname, uname, pwd, dbase):
	db = mysql.connector.connect(
		host=hostname,
		user=uname,
		password=pwd,
		database=dbase
	)
	return db

# Key derivation uses Scrypt, and generates a new salt if you don't provide one
# This should be run twice, once to make an index key and once to make an encryption key, both using different salts
def deriveKey(pwd, salt=os.urandom(16)):
	kdf = Scrypt(
		salt=salt,
		length=32,
		n=2**14,
		r=8,
		p=1,
	)
	key = kdf.derive(pwd)
	return key, salt

def encrypt(key, plaintext, associated_data):
	# Generate a random 96-bit IV.
	iv = os.urandom(12)

	# Construct an AES-GCM Cipher object with the given key and a
	# randomly generated IV.
	encryptor = Cipher(
		algorithms.AES(key),
		modes.GCM(iv),
	).encryptor()

	# associated_data will be authenticated but not encrypted,
	# it must also be passed in on decryption.
	encryptor.authenticate_additional_data(associated_data)

	# Encrypt the plaintext and get the associated ciphertext.
	# GCM does not require padding.
	ciphertext = encryptor.update(plaintext) + encryptor.finalize()

	return (iv, ciphertext, encryptor.tag)
    
def decrypt(key, associated_data, iv, ciphertext, tag):
	# Construct a Cipher object, with the key, iv, and additionally the
	# GCM tag used for authenticating the message.
	decryptor = Cipher(
		algorithms.AES(key),
		modes.GCM(iv, tag),encrypt(key, plaintext, associated_data)
	).decryptor()

	# We put associated_data back in or the tag will fail to verify
	# when we finalize the decryptor.
	decryptor.authenticate_additional_data(associated_data)

	# Decryption gets us the authenticated plaintext.
	# If the tag does not match an InvalidTag exception will be raised.
	return decryptor.update(ciphertext) + decryptor.finalize()

# The blind index is also using Scrypt with the index key as the salt, as per the article's recommendation
def getBlindIndex(indexKey, plaintext):
	kdf = Scrypt(
		salt=indexKey,
		length=32,
		n=2**14,
		r=8,
		p=1,
	)
	bidx = kdf.derive(plaintext)
	return bidx

# This is a placeholder. We'll decide what database and what column to encrypt later
def findHumansBySSN(db, plaintext, indexKey):
	index = getBlindIndex(indexKey, plaintext)
	cursor = db.cursor()
	cursor.execute("SELECT * FROM humans WHERE ssn_bidx = " + index)
	result = cursor.fetchall()
	return result
	
key, salt = deriveKey(b"mysupersecretpassword")
print(key)
db=connectToDB('cloudstorage.cwyqmpoiw0xl.us-east-1.rds.amazonaws.com', 'symmetric', 'encryption', 'world')
cursor = db.cursor(dictionary=True)
cursor.execute("SELECT code FROM country")
for row in cursor:
    print ("plaintext",row["code"])
    plaintext=row["code"].encode('UTF-8')
    ciphertext=encrypt(key, plaintext, b"Additional Data")
    print("ciphertext",ciphertext)



