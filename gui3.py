# import the necessary packages
from tkinter import *
from PIL import Image
from PIL import ImageTk
import tkinter.filedialog
import cv2
import numpy as np
from PIL import ImageDraw


# initialize the window toolkit along with the two image panels
root = Tk()

# create a button, then when pressed, will trigger a file chooser
# dialog and allow the user to select an input image; then add the
# button the GUI


 
class first_page():
	def __init__(self,master):
		self.master=master
		self.frametop=Frame(master)
		self.frametop.pack(side=TOP)
		self.btn=Button(root, text="Select a second image", command=self.select_image)
		self.btn.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")

		self.btn_first=Button(root, text="Select a first image", command=self.select_first_image)
		self.btn_first.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")


		self.panelA= None
		self.panelB= None
		self.imageA=None
		self.input=None
		self.imageB=None
		self.output=None
		self.homography= Button(self.frametop,text='Compute',command=self.compute)
		self.homography.grid(row=0,column=2)

		self.delete_button = Button(self.frametop,text = 'Delete Selection',fg='red',command=self.delete_clicks)
		self.delete_button.grid(row=0,column=0)
		self.quitButton = Button(self.frametop,text='Quit',command=self.frametop.quit)
		self.quitButton.grid(row=0,column=1)

		self.clicksA=[]
		self.clicksB=[]

	def select_first_image(self):
		path=tkinter.filedialog.askopenfilename()  
		if len(path) > 0:
			image = cv2.imread(path)
			image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
			self.imageA=image
			self.input=image
			
	def select_image(self):
 
		# open a file chooser dialog and allow the user to select an input
		# image
		path = tkinter.filedialog.askopenfilename()  

		# ensure a file path was selected
		if len(path) > 0:
			imageB = cv2.imread(path)
			

			# OpenCV represents images in BGR order; however PIL represents
			# images in RGB order, so we need to swap the channels
			image = self.imageA
			image = Image.fromarray(image)
			image = ImageTk.PhotoImage(image)

		
			self.imageB=imageB
			self.output=imageB
			imageB= Image.fromarray(imageB)
			imageB = ImageTk.PhotoImage(imageB)
			# if the panels are None, initialize them
			if self.panelA is None or self.panelB is None:
				# the first panel will store our original image
				self.panelA = Label(image=image)
				self.panelA.image = image
				self.panelA.pack(side="left")

				self.panelB = Label(image=imageB)
				self.panelB.image = imageB
				self.panelB.pack(side="right")

			# otherwise, update the image panels
			else:
				# update the pannels
				self.panelA.configure(image=image)
				self.panelB.configure(image=imageB)
				self.panelA.image = image
				self.panelB.image = imageB
			self.panelA.bind('<Button-1>',self.A_click)
			self.panelB.bind('<Button-1>',self.B_click)

	def A_click(self,event):
		x,y=event.x,event.y
		print('x coordinates : {}, y coordinates : {}'.format(x,y))
		print('First image')
		self.clicksA.append((x,y))
		image_before=self.imageA
		for i in range(-2,3):		
			image_before[y+i][x+i]=(255,0,0)
			image_before[y-i][x+i]=(255,0,0)

		

		image= Image.fromarray(image_before)
		image=ImageTk.PhotoImage(image)
		self.panelA.configure(image=image)
		self.panelA.image = image
		print(np.array(image))
		
		print(self.clicksA)
	
	def B_click(self,event):
		x,y=event.x,event.y
		print('x coordinates : {}, y coordinates : {}'.format(x,y))
		print('Second image')
		self.clicksB.append((x,y))
		print(self.clicksB)
		image_before=self.imageB
		for i in range(-2,3):		
			image_before[y+i][x+i]=(255,0,0)
			image_before[y-i][x+i]=(255,0,0)

		

		image= Image.fromarray(image_before)
		image=ImageTk.PhotoImage(image)
		self.panelB.configure(image=image)
		self.panelB.image = image

	def delete_clicks(self):
		if len(self.clicksA)>0:
			print('Deleting a point')
			self.clicksA=[]
			self.clicksB=[]
	
	def compute(self):
		height,width,_=self.output.shape
		print('output',self.output.shape)
		print('input',self.input.shape)
		#height,width,_=self.input.shape
		#dest=np.array([(0,0),(height,0),(height,width),(0,width)])
		dest=np.array(self.clicksB)[-4:]
		h, status = cv2.findHomography(np.array(self.clicksA)[-4:], dest,cv2.RANSAC, 5.0)
		output=np.zeros((height,height,0),np.uint8)
		
		im_out = cv2.warpPerspective(self.input,h,(height,width))
		print('im_out',im_out.shape)
		self.imageB=im_out
		cv2.imwrite('output.png',im_out)
		im_out= Image.fromarray(im_out)
		im_out=ImageTk.PhotoImage(im_out)
		self.frametop.quit
		self.panelA.quit
		self.panelB.quit
		newwin = Toplevel(self.master)
		display = Label(newwin, text="Computation Result")
		display.configure(image=im_out)
		display.image=im_out
		display.pack()   
		#self.panelB.configure(image=im_out)
		#self.panelB.image = im_out
class select_points():
	def __init__(self,openwindow):
		self.openwindow=openwindow
		self.openwindow.panelA.bind('<Button-1>',self.left_click)
	def left_click(self,event):
		x,y=event.x,event.y
		print('x coordinates : {}, y coordinates : {}'.format(x,y))




Openwindow=first_page(root)

# kick off the GUI
root.mainloop()