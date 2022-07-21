#!/usr/bin/env python3
"""
Created by Parth Sharma
Title: Linux Shadow Cracker
Description: This script cracks linux shadow file using bruteforce technique.
This script needs root privileges if you are cracking shadow file directly

"""
import crypt
import threading
import argparse

screenLock = threading.BoundedSemaphore(1) # Semaphore to lock screen so that each thread gets screen to print at a time

def crackFile(password,salt,dictPass):
	cryptWord = crypt.crypt(dictPass,salt)
	screenLock.acquire()
	print('[+] Testing for {} .....'.format(dictPass))
	if cryptWord == password:
		crackedPass = dictPass
		print('Password Found!!!!!')
		print(crackedPass)
		exit(0)	# if password found then script ends all threads/daemons stops
	screenLock.release()

def main():
	parser = argparse.ArgumentParser(description='Crack passwords by bruteforcing a shadow formatted file')
	parser.add_argument('user',help='User to crack')
	parser.add_argument('shadow',help='Shadow file to crack')
	parser.add_argument('dictionary',help='Your dictionary file')
	args = parser.parse_args()
	
	if not args.dictionary:
		print('Specify you dictionary file')
		exit(0)
	else:
		dictFile = args.dictionary
	
	if not args.user:
		print('Specify a user to crack')
		exit(0)
	else:
		userToCrack = args.user
	
	if not args.shadow:
		print('Specify your shadow file')
		exit(0)
	else:
		shadFile = args.shadow		
	
	dictionary = open(dictFile,"r") #opening dictionary file
	
	try:
		shadowFile = open(shadFile,"r")	#opening shadow file
	except:
		print('You do not have access to shadow file')
		exit(0)

	
	for line in shadowFile.readlines():
		if line.split(':')[0] == userToCrack: #picking out the user to be cracked from shadow file
			passToCrack = line.split(':')[1]
			break

	
	salt = '$' + passToCrack.split('$')[1] + '$' + passToCrack.split('$')[2] + '$' #extracting salt
	
	for line in dictionary.readlines():
		dictPass = line.strip('\n')
		t = threading.Thread(target=crackFile,args=(passToCrack,salt,dictPass),daemon=True) #daemon is created so that when password is found main() ends and script ends then all threads gets stopped
		t.start()
	


if __name__ == '__main__':
	main()
