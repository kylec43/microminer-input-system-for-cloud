import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from tkinter.filedialog import askopenfile
from tkinter import messagebox as mb
import re
from time import time
from threading import Thread
from submitToKwicSystem import submitToKwicSystem
from Event import Event
import Constants


class InputPage(tk.Frame):

	def __init__(self, parent):

		self._parent = parent
		super(InputPage, self).__init__()


		#configure grid
		self._gridSizeRows = 9
		for i in range(self._gridSizeRows):
			self.grid_rowconfigure(i, weight = 1)

		self._gridSizeColumns = 7
		for i in range(self._gridSizeColumns):
			self.grid_columnconfigure(i, weight = 1)

		self.displayInputScreen()



	def displayInputScreen(self):

		for widget in self.winfo_children():
			widget.destroy()

		#Create Input Widgets
		input_label = tk.Label(self, text = "Input", font=('Helvetica 10 bold'))
		self._input_textbox = ScrolledText(self, height = 25, width = 100, wrap='none')

		noise_words_label = tk.Label(self, text = "Noise words", font=('Helvetica 10 bold'))
		self._noise_words_entry = tk.Entry(self)

		scrollbar1 = tk.Scrollbar(self, command=self._input_textbox.xview, orient='horizontal')
		self._input_textbox['xscrollcommand'] = scrollbar1.set
		self._submit_button = ttk.Button(self, text = 'Submit to Database', command = self._uploadInput)
		load_file_button = ttk.Button(self, text = 'Load file..', command = self._loadFile)
		clear_input_textbox_button = ttk.Button(self, text = 'Clear', command = self._clearInputBox)


		#Place widgets on grid
		input_label.grid(row = 1, column = (2 + self._gridSizeColumns - 3)//2, sticky = 'e')
		self._input_textbox.grid(row = 2, rowspan = 3, column = 2, columnspan = self._gridSizeColumns-3, sticky = 'NESW')
		scrollbar1.grid(row = 5, column = 2, columnspan = self._gridSizeColumns-3, sticky = 'EW')

		noise_words_label.grid(row = 6, column = (2 + self._gridSizeColumns - 3)//2, sticky = 'e')
		self._noise_words_entry.grid(row = 7, column = 2, columnspan = self._gridSizeColumns-3, sticky = 'NESW')

		self._submit_button.grid(row = 4, column = 1, sticky='NESW')
		clear_input_textbox_button.grid(row = 2, column = 1, sticky='NSEW')
		load_file_button.grid(row = 3, column = 1, sticky='NSEW')


	def _clearInputBox(self):
		self._input_textbox.delete("1.0","end")

	def _loadFile(self):

		try:
			chosen_file = askopenfile(mode ='r')
			if chosen_file is not None:
				contents = chosen_file.read()
				self._clearInputBox()
				self._input_textbox.insert(tk.END, contents)
		except:
			mb.showerror("Error", "Error: cannot read from file")


	def _getInput(self):
		return self._input_textbox.get("1.0", 'end -1c')

	def _getNoiseWords(self):
		noiseWords = str(self._noise_words_entry.get())

		if not noiseWords == '':
			noiseWords = re.split(' *,* *,+ *,* *| +', noiseWords)
			if noiseWords[-1] == '': noiseWords.pop()
			noiseWords = [noiseWord.lower() for noiseWord in noiseWords]
			noiseWords = " ".join(noiseWords)
		
		return noiseWords



	def setGenerateButtonState(self, value):

		state = tk.DISABLED
		if value != False:
			state = tk.NORMAL

		self._submit_button.configure(state = state)


	def _uploadInput(self):

		inputData = self._getInput()
		noiseWordsData = self._getNoiseWords()
		
		if noiseWordsData == '':
			noiseWordsData = ' '

		validity = self._validInput(inputData)
		if not validity == True:
			mb.showerror("Error", validity)
			return


		kwicThread = Thread(target=submitToKwicSystem, args=(self._parent, inputData, noiseWordsData))
		kwicThread.start()


	def _validInput(self, inputData):
		print(len(inputData))
		if len(inputData) == 0:
			errorMessage = 'Please insert Url(s) and keyword(s)'
			return errorMessage

		inputData = inputData.split('\n')
		errorMessage = ''
		error = False



		for x in inputData:
			x = x.split()

			if not re.match('http://(www.)*[a-zA-Z0-9]+(\.edu|\.com|\.org|\.net)', x[0]):
				errorMessage += 'Invalid url syntax\n'	
				error = True

			if len(x) == 1:
				errorMessage += 'Missing descriptor(s)'		
				error = True

			if error:
				break	
		if error:
			return errorMessage
		else:
			return True
			


		

