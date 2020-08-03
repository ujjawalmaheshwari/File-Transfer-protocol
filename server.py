# import socket programming library 
import socket 
import pickle
# import thread module 
from _thread import *
import threading 
import time
import sys
#print_lock = threading.Lock() 
try:
	users_database = pickle.load( open( "udb.p", "rb" ) )
except:
	users_database = dict()
try:
	users_files = pickle.load( open( "ufiles.p", "rb" ) )
except:
	users_files = dict()	
# thread fuction 
def login(c):
	n = int((c.recv(24)).decode('ascii'))
	if(n==0):
		l = pickle.loads(c.recv(1024))
		usr = str(l[0])
		pas = str(l[1])
		pas2 = str(l[2])
		if((pas == pas2) and (usr not in users_database.keys())):
			message = "Account successfully created!"
			c.send(message.encode('ascii'))
			users_database[usr] = pas
			users_files[usr] = dict()
			return usr
		elif(usr in users_database.keys()):
			message = "Username already taken.\nClosing the connection.."
			c.send(message.encode('ascii'))
			c.close()
		elif(pas != pas2):
			message = "The passwords do not match.\nClosing the connection.."
			c.send(message.encode('ascii'))
			c.close()

	elif(n==1):
		l = pickle.loads(c.recv(1024))
		usr = str(l[0])
		pas = str(l[1])                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
		if(usr not in users_database.keys()):
			message = "User does not exist!\nClosing the connection..."
			c.send(message.encode('ascii'))
			c.close()
		elif(users_database[usr] != pas):
			message = "Wrong password!\nClosing the connection..."
			c.send(message.encode('ascii'))
			c.close()
		elif(users_database[usr] == pas):
			message = "Login successful!"
			c.send(message.encode('ascii'))
			return usr


def func(usrn,c):
	time.sleep(1)
	c.send(pickle.dumps(users_files[usrn]))
	fno = int((c.recv(24)).decode('ascii'))
	if(fno == 0):
		fname = (c.recv(1024)).decode('ascii')
		#time.sleep(1)
		file = fname
		f = open(file,'wb')
		l = c.recv(1024)
		while (l):
			f.write(l)
			l = c.recv(1024)
		f.close()
		m = max(len(list(users_files[usrn].keys()))+1,1)
		users_files[usrn][m] = fname
		print("Recieved file ",fname," from user - ",usrn)
		c.close()
	else:
		fname = users_files[usrn][fno]
		c.send(fname.encode('ascii'))
		time.sleep(0.5)
		f = open(fname,'rb')
		l = f.read(1024)
		while (l):
			c.send(l)
			l = f.read(1024)
		f.close()
		print("Sent file ",fname," to user - ",usrn)
		c.close()


	#print('fno - ',fno,' fname - ',fname,' fpath - ',fpath)

def threaded(c,addr):
	usrn = login(c) 
	if(usrn != None):
		print(addr[0],':',addr[1],' logged in as ',usrn)
		pickle.dump( users_database, open( "udb.p", "wb" ) )
		pickle.dump( users_files, open( "ufiles.p", "wb" ) )
		res = func(usrn,c)
	else:
		print(addr[0],':',addr[1],' failed to login')

def Main(): 
	host = "" 

	# reverse a port on your computer 
	# in our case it is 12345 but it 
	# can be anything 
	port = 12346
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
	s.bind((host, port)) 
	print("socket binded to port", port) 

	# put the socket into listening mode 
	s.listen(5) 
	print("socket is listening") 

	# a forever loop until client wants to exit 
	while True: 

		# establish connection with client 
		c, addr = s.accept() 

		# lock acquired by client 
		#print_lock.acquire() 
		print('Connected to :', addr[0], ':', addr[1]) 

		# Start a new thread and return its identifier 
		start_new_thread(threaded, (c,addr)) 
	s.close() 


if __name__ == '__main__': 
	Main() 
