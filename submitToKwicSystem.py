from Event import Event
import Constants
from time import time
from time import sleep
import socket

def submitToKwicSystem(parent, inputData, noiseWordsData):

	success = True
	try:
		parent.addEvent(Event(Constants.EVT_SUBMIT_STARTED))

		
		inputData = inputData.encode('utf-8')
		noiseWordsData = noiseWordsData.encode('utf-8')


		SERVER_IP = 'localhost'  
		PORT = 12000

		#Create Client Socket
		client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		print('created')
		client_socket.settimeout(10)

		#Connect to Server Socket
		client_socket.connect((SERVER_IP, PORT))
		client_socket.settimeout(10)

		#Send Message to Server
		client_socket.sendall(inputData)
		response = client_socket.recv(100)
		if response == Constants.SERVER_RESPONSE_UPLOAD_FAILURE:
			raise Exception(Constants.SERVER_RESPONSE_UPLOAD_FAILURE)
		client_socket.sendall(noiseWordsData)


		#Recieve a response from the Server
		client_socket.settimeout(120)
		response = client_socket.recv(100)
		print('Received:', response.decode('utf-8'))
		if response == Constants.SERVER_RESPONSE_UPLOAD_FAILURE:
			raise Exception('SUBMIT FAILURE')

	except Exception as e:
		success = False
		print(e)
	finally:
		if success:
			parent.addEvent(Event(Constants.EVT_SUBMIT_SUCCESS))
		else:
			parent.addEvent(Event(Constants.EVT_SUBMIT_FAILURE))

		client_socket.close()

