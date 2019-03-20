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
		self.btn=Button(self.frametop, text="Select a second image After selecting the four points in the first image", command=self.select_second_image)
		

		self.btn_first=Button(root, text="Select a first image", command=self.select_image)
		self.btn_first.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")


		self.panelA= None
		self.panelB= None
		self.imageA=None
		self.input=None
		self.imageB=None
		self.output=None
		

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
			imageA = cv2.imread(path)
			
		
			
			if imageA.shape[1]>900:
				imageA=cv2.resize(imageA, dsize=(800, 800), interpolation=cv2.INTER_CUBIC)
			self.input=imageA
			self.imageA=imageA.copy()
			imageA= Image.fromarray(imageA)
			imageA = ImageTk.PhotoImage(imageA)
			
			# if the panels are None, initialize them
			if self.panelA is None:
				# the first panel will store our original image
				self.panelA = Label(image=imageA)
				self.panelA.image = imageA
				self.panelA.pack()
               
			# otherwise, update the image panels
			else:
				# update the pannels
				self.panelA.configure(image=imageA)
				self.panelA.image = imageA
			self.panelA.bind('<Button-1>',self.A_click)
			self.btn.grid(row=0,column=2)
    
	def select_second_image(self):
        	# open a file chooser dialog and allow the user to select an input
		# image
		path = tkinter.filedialog.askopenfilename()  

		# ensure a file path was selected
		if len(path) > 0:
			imageB = cv2.imread(path)
			

		

			if imageB.shape[1]>900:
				imageB=cv2.resize(imageB, dsize=(800, 800), interpolation=cv2.INTER_CUBIC)
			self.imageB=imageB.copy()
			self.output=imageB
			
			imageB= Image.fromarray(imageB)
			imageB = ImageTk.PhotoImage(imageB)
		

              
			# if the panels are None, initialize them
			if self.panelB is None:
				# the first panel will store our original image
				newwinB = Toplevel(self.master)
				homography= Button(newwinB,text='Compute',command=self.compute)
				homography.pack()
				self.panelB = Label(newwinB,image=imageB)
				self.panelB.image = imageB
				self.panelB.pack()
				quitButton = Button(newwinB,text='Quit',command=newwinB.quit)
				quitButton.pack()
           
                
			# otherwise, update the image panels
			else:
				# update the pannels
				self.panelB.quit
				self.panelB=Label(Toplevel(self.master),image=imageB)
				self.panelB.configure(image=imageB)
				self.panelB.image = imageB
			self.panelB.bind('<Button-1>',self.B_click)
	def A_click(self,event):
		x,y=event.x,event.y
		print('x coordinates : {}, y coordinates : {}'.format(x,y))
		print('First image')
		image_before=self.imageA
		
		for i in range(-2,3):
			if -1<x+i<(image_before.shape[1]) and -1<y+i<(image_before.shape[0]):
				image_before[y+i][x+i]=(255,0,0)
				image_before[y-i][x+i]=(255,0,0)

		if -1<x<(image_before.shape[1]) and -1<y<(image_before.shape[0]):
			self.clicksA.append((x,y))
		else:
			errorwin=Toplevel(self.master)
			display=Label(errorwin,text='Your selection is outside the boundaries \n Reselect again')
			display.pack()

		

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
        
		image_before=self.imageB
		for i in range(-2,3):
			if -1<x+i<(image_before.shape[1]) and -1<y+i<(image_before.shape[0]):
			
				image_before[y+i][x+i]=(255,0,0)
				image_before[y-i][x+i]=(255,0,0)

		if -1<x<(image_before.shape[1]) and -1<y<(image_before.shape[0]):
			self.clicksB.append((x,y))
		else:
			errorwin=Toplevel(self.master)
			display=Label(errorwin,text='Your selection is outside the boundaries \n Reselect again')
			display.pack()


		image= Image.fromarray(image_before)
		image=ImageTk.PhotoImage(image)
		self.panelB.configure(image=image)
		self.panelB.image = image
		print(self.clicksB)

	def delete_clicks(self):
		if len(self.clicksA)>0:
			print('Deleting points')
			self.clicksA=[]
			self.clicksB=[]
			if self.panelA is not None:
				imageA=self.input.copy()
				imageA= Image.fromarray(imageA)
				imageA = ImageTk.PhotoImage(imageA)
				self.panelA.configure(image=imageA)
				self.panelA.image=imageA
				self.imageA=self.input

			if self.panelB is not None:
				imageB=self.output.copy()
				imageB= Image.fromarray(imageB)
				imageB = ImageTk.PhotoImage(imageB)
				self.panelB.configure(image=imageB)
				self.panelB.image=imageB
				self.imageB=self.output
	def compute(self):
		
		dest=np.array(self.clicksB)[-4:]
		h, status = cv2.findHomography(np.array(self.clicksA)[-4:], dest,cv2.RANSAC, 5.0)
		height,width=self.output.shape[:2]
		im_out = cv2.warpPerspective(self.input,h,(width,height))
		print('im_out',im_out.shape)
		self.imageB=im_out
		cv2.imwrite('output.png',im_out)
		im_out= Image.fromarray(im_out)
		im_out=ImageTk.PhotoImage(im_out)
		self.frametop.quit
		#self.panelA.quit
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