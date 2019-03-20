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
		self.frametop=Frame(master)
		self.frametop.pack(side=TOP)
		self.btn=Button(root, text="Select an image", command=self.select_image)
		self.btn.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")
		self.panelA= None
		self.panelB= None
		self.imageA=None
		self.input=None
		self.imageB=None
		self.homography= Button(self.frametop,text='Compute',command=self.compute)
		self.homography.grid(row=0,column=2)

		self.delete_button = Button(self.frametop,text = 'Delete Selection',fg='red',command=self.delete_clicks)
		self.delete_button.grid(row=0,column=0)
		self.quitButton = Button(self.frametop,text='Quit',command=self.frametop.quit)
		self.quitButton.grid(row=0,column=1)

		self.clicksA=[]
		self.clicksB=[]

	def select_image(self):
	
 
		# open a file chooser dialog and allow the user to select an input
		# image
		path = tkinter.filedialog.askopenfilename()  

		# ensure a file path was selected
		if len(path) > 0:
			image = cv2.imread(path)
			

			# OpenCV represents images in BGR order; however PIL represents
			# images in RGB order, so we need to swap the channels
			image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
			self.imageA=image
			self.input=image
			height=image.shape[0]
			width=image.shape[1]
			image = Image.fromarray(image)

			
			#blank_image=np.zeros((height,width,3), np.uint8)
			#blank_image=self.grid(height,width)
			blank_image=np.zeros((height,width,3), np.uint8)
			self.imageB=blank_image
			# ...and then to ImageTk format
			image = ImageTk.PhotoImage(image)
			blank_image= Image.fromarray(blank_image)
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

	def delete_clicks(self):
		if len(self.clicksA)>0:
			print('Deleting a point')
			self.clicksA=[]
			self.clicksB=[]
	def grid(self,height,width):
		step_count = 10

		if len(sys.argv) == 2:
			step_count = int(sys.argv[1])

		image = Image.new(mode='L', size=(height, width), color=255)

		# Draw some lines
		draw = ImageDraw.Draw(image)
		y_start = 0
		y_end = image.height
		step_size = int(image.width / step_count)

		for x in range(0, image.width, step_size):
			line = ((x, y_start), (x, y_end))
			draw.line(line, fill=128)

		x_start = 0
		x_end = image.width

		for y in range(0, image.height, step_size):
			line = ((x_start, y), (x_end, y))
			draw.line(line, fill=128)

		del draw
		return(image)
	def compute(self):
		height,width,_=self.imageB.shape
		dest=np.array([(0,0),(height,0),(height,width),(0,width)])
		h, status = cv2.findHomography(np.array(self.clicksA)[-4:], dest,cv2.RANSAC, 5.0)
		output=np.zeros((height,height,0),np.uint8)
		
		im_out = cv2.warpPerspective(self.input,h,(height,height))
		self.imageB=im_out
		cv2.imwrite('output.png',im_out)
		im_out= Image.fromarray(im_out)
		im_out=ImageTk.PhotoImage(im_out)
		self.panelB.configure(image=im_out)
		self.panelB.image = im_out
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