from tkinter import ttk
import tkinter as tk
from InputPage import InputPage
from SubmitPage import SubmitPage
import Constants



class Form (tk.Tk):

	def __init__(self):

		tk.Tk.__init__(self) 
		
		self.eventQueue = []
		

		self.after(1, self._executeEvents)

		self.title('Microminer Input System')
		self.minsize(800, 600)

		#configure notebook
		notebook_style = ttk.Style()
		notebook_style.configure('Custom.TNotebook.Tab', padding=[36, 6], font=('Helvetica 12 bold'))
		self.tabControl = ttk.Notebook(self, style = 'Custom.TNotebook')
		self.input_tab = InputPage(self)
		self.submit_tab = None
		self.tabControl.add(self.input_tab, text ='Input')
		
		#configure grid
		self.gridSizeRows = 1
		for i in range(self.gridSizeRows):
			self.grid_rowconfigure(i, weight = 1)

		self.gridSizeColumns = 1
		for i in range(self.gridSizeColumns):
			self.grid_columnconfigure(i, weight = 1)

		self.tabControl.grid(row=0, column = 0, columnspan = self.gridSizeColumns, sticky = 'NESW')


	def addEvent(self, event):
		self.eventQueue.append(event)


	def _executeEvents(self):

		if len(self.eventQueue) > 0:

			if self.eventQueue[0].code == Constants.EVT_SUBMIT_STARTED:

				if self.submit_tab == None:
					self.submit_tab = SubmitPage(self)
					self.tabControl.add(self.submit_tab, text ='Output')
					
				self.input_tab.setSubmitButtonState(False)
				self.submit_tab.displayLoadingScreen()
				self.tabControl.select(1)

			elif self.eventQueue[0].code == Constants.EVT_SUBMIT_SUCCESS:
				self.submit_tab.displaySuccessScreen()
				self.input_tab.setSubmitButtonState(True)

			elif self.eventQueue[0].code == Constants.EVT_SUBMIT_FAILURE:
				self.submit_tab.displayFailScreen()
				self.input_tab.setSubmitButtonState(True)

			elif self.eventQueue[0].code == Constants.EVT_CLOSE_SUBMIT_PAGE:
				self.tabControl.forget(1)
				self.submit_tab = None

			self.eventQueue.pop(0)
		
		self.after(1, self._executeEvents)


