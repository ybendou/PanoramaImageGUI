# import the necessary packages
from tkinter import *
from PIL import Image
from PIL import ImageTk
import tkinter.filedialog
import cv2
import numpy as np
 

# initialize the window toolkit along with the two image panels
root = Tk()

# create a button, then when pressed, will trigger a file chooser
# dialog and allow the user to select an input image; then add the
# button the GUI


 
class first_page():
	def __init__(self):
		self.btn=Button(root, text="Select an image", command=self.select_image)
		self.btn.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")
		self.panelA= None
		self.panelB= None
	def select_image(self):
	
 
		# open a file chooser dialog and allow the user to select an input
		# image
		path = tkinter.filedialog.askopenfilename()  

		# ensure a file path was selected
		if len(path) > 0:
			image = cv2.imread(path)
			gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
			edged = cv2.Canny(gray, 50, 100)

			# OpenCV represents images in BGR order; however PIL represents
			# images in RGB order, so we need to swap the channels
			image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
			height=int(1.5*(image.shape[0]))
			width=int(1.5*(image.shape[1]))
			image = Image.fromarray(image)


			blank_image=np.zeros((height,width,3), np.uint8)
			blank_image= Image.fromarray(blank_image)

			# ...and then to ImageTk format
			image = ImageTk.PhotoImage(image)
			blank_image = ImageTk.PhotoImage(blank_image)
			# if the panels are None, initialize them
			if self.panelA is None or self.panelB is None:
				# the first panel will store our original image
				self.panelA = Label(image=image)
				self.panelA.image = image
				self.panelA.pack(side="left", padx=10, pady=10)

				# while the second panel will store the edge map
				self.panelB = Label(image=blank_image)
				self.panelB.image = blank_image
				self.panelB.pack(side="right", padx=10, pady=10)

			# otherwise, update the image panels
			else:
				# update the pannels
				self.panelA.configure(image=image)
				self.panelB.configure(image=edged)
				self.panelA.image = image
				self.panelB.image = blank_image


class select_points():
	def __init__(self,openwindow):
		self.openwindow=openwindow
		self.openwindow.panelA.bind('<Button-1>',self.left_click)
	def left_click(self,event):
		x,y=event.x,event.y
		print('x coordinates : {}, y coordinates : {}'.format(x,y))




Openwindow=first_page()
points_image=select_points(Openwindow)

# kick off the GUI
root.mainloop()