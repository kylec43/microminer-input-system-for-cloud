from Event import Event
import Constants
from time import time
from time import sleep
import requests

def submitToKwicSystem(parent, inputData, noiseWordsData):

	success = True
	try:
		parent.addEvent(Event(Constants.EVT_SUBMIT_STARTED))

		
		response = requests.get(Constants.KWIC_WEBSERVER_URl, params={Constants.GET_ARG_ORIGINAL_URL_KEYWORDS: inputData, Constants.GET_ARG_NOISE_WORDS: noiseWordsData})
		response = response.text
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
