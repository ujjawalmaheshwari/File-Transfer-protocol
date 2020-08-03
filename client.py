# Import socket module 
import socket 
import json
import pickle
import time
import sys
#import threading

def func(s,usr):
	print("Your file directory on the server is -\n")
	dirc = pickle.loads(s.recv(1024))
	print(dirc)
	print("Enter 0 for storing new file on the server or the file number for fetching the file from the server")
	fno = int(input())
	while(fno not in range(len(list(dirc.keys()))+1)):
			print("\nPlease enter a valid number: ")
			fno = int(input())
	s.send(str(fno).encode('ascii'))
	if(fno==0):
		#Lock = threading.RLock()
		#Lock.acquire()
		print("Enter the name of the file")
		fname = input()
		print("Enter the full path of the file")
		fpath = input()
		sendfile(s,usr,fname,fpath)
		#Lock.release()
	else:
		fname = (s.recv(1024)).decode('ascii')
		f = open(fname,'wb')
		l = s.recv(1024)
		while (l):
			f.write(l)
			l = s.recv(1024)
			print('Recieving data...')
		f.close()
		print("Data received")

def sendfile(s,usr,fname,fpath):
	
	
	
	s.send(fname.encode('ascii'))
	time.sleep(0.5)
	#s.send(fpath.encode('ascii'))
	try:
		f = open(fpath,'rb')
	except:
		print('Please enter the correct path')
		sys.exit()
	l = f.read(1024)

	while(l):
		s.send(l)
		l = f.read(1024)
		print('Sending data...')
	f.close()
	print("Data sent")

	

def Main(): 
	# local host IP '127.0.0.1' 
	host = '127.0.0.1'

	# Define the port on which you want to connect 
	port = 12346
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 

	# connect to server on local computer 
	s.connect((host,port)) 

	# message you send to server 
	print("Connected to the drive server\n")
	while True: 
		print("Enter 0 for new user, 1 for existing user: ")
		n = int(input())
		while(n not in [0,1]):
			print("\nPlease enter 0 or 1: ")
			n = int(input())
		s.send(str(n).encode('ascii'))
		print()
		if(n==0):
			print("Enter username: ")
			usr = input()
			print("\nEnter password: ")
			pas = input()
			print("\nConfirm password: ")
			pas2 = input()
			l = [usr,pas,pas2]
			s.send(pickle.dumps(l))
			reply = str((s.recv(1024)).decode('ascii'))
			print()
			print(reply,'\n')
			if(reply == "Account successfully created!"):
				print("Logged in as ",usr,'\n')
				func(s,usr)
				break

		elif(n==1):
			print("Enter username: ")
			usr = input()
			print("\nEnter password: ")
			pas = input()
			l = [usr,pas]
			s.send(pickle.dumps(l))
			reply = str((s.recv(1024)).decode('ascii'))
			print()
			print(reply,'\n')
			if(reply == "Login successful!"):
				print("Logged in as ",usr,'\n')
				func(s,usr)
				break
		break
		# message sent to server 
		#s.send(message.encode('ascii')) 
		# messaga received from server 
		#data = str((s.recv(1024)).decode('ascii'))

		# print the received message 
		# here it would be a reverse of sent message 
		
	# close the connection 
	s.close() 

if __name__ == '__main__': 
	Main() 
