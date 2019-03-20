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
		#path = tkinter.filedialog.askopenfilename()  
		path='./im02.jpg'
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
		#path = tkinter.filedialog.askopenfilename()  
		path='./im01.jpg'
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
		if self.clicksA==[]:
			self.clicksA=[(292, 285), (322, 284), (322, 337), (292, 346), (118, 246), (171, 250), (170, 283), (117, 283)]
			self.clicksB=[(579, 259), (618, 258), (619, 320), (580, 328), (397, 225), (447, 228), (450, 255), (397, 257)]
		src=np.array(self.clicksA)
		dest=np.array(self.clicksB)
		h, status = cv2.findHomography(np.array(self.clicksA), dest,cv2.RANSAC, 5.0)
		height,width=self.output.shape[:2]

		img1=self.output
		img2=self.input
		rows1, cols1 = img1.shape[:2]
		rows2, cols2 = img2.shape[:2]

		list_of_points_1 = np.float32([[0,0], [0,rows1], [cols1, rows1], [cols1,0]]).reshape(-1,1,2)
		temp_points = np.float32([[0,0], [0,rows2], [cols2, rows2], [cols2,0]]).reshape(-1,1,2)

		list_of_points_2 = cv2.perspectiveTransform(temp_points, h)
		list_of_points = np.concatenate((list_of_points_1, list_of_points_2), axis=0)

		[x_min, y_min] = np.int32(list_of_points.min(axis=0).ravel() - 0.5)
		[x_max, y_max] = np.int32(list_of_points.max(axis=0).ravel() + 0.5)

		translation_dist = [-x_min, -y_min]
		H_translation = np.array([[1, 0, translation_dist[0]], [0, 1, translation_dist[1]], [0,0,1]])

		im_out = cv2.warpPerspective(self.input,H_translation.dot(h),(x_max - x_min, y_max - y_min))
		im_out[translation_dist[1]:rows1+translation_dist[1],translation_dist[0]:cols1+translation_dist[0]] = img1
		self.imageB=im_out
		cv2.imwrite('selection_points.png',im_out)
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