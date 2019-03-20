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
		self.panelC=None
		self.third_image=None

		
		self.quitButton = Button(self.frametop,text='Quit',command=self.frametop.quit)
		self.quitButton.grid(row=0,column=1)

		self.clicksA=[]
		self.clicksB=[]

	def select_image(self):
 
		# open a file chooser dialog and allow the user to select an input
		# image
		#path = tkinter.filedialog.askopenfilename()  
		path='./img2/im03.jpg'
		# ensure a file path was selected
		if len(path) > 0:
			imageA = cv2.imread(path)
			

			# OpenCV represents images in BGR order; however PIL represents
			# images in RGB order, so we need to swap the channels
		
			
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
				#self.panelB.configure(image=imageB)
				self.panelA.image = imageA
				#self.panelB.image = imageB
			#self.btn.pack(side="top", fill="both", expand="yes", padx="10", pady="10")
			self.btn.grid(row=0,column=2)
			#self.panelB.bind('<Button-1>',self.B_click)
	def select_third_image(self):
 
			# open a file chooser dialog and allow the user to select an input
		# image
		#path = tkinter.filedialog.askopenfilename()  
		path='./img2/im04.jpg'
		# ensure a file path was selected
		if len(path) > 0:
			imageB = cv2.imread(path)
			

			# OpenCV represents images in BGR order; however PIL represents
			# images in RGB order, so we need to swap the channels
		
			if imageB.shape[1]>900:
				imageB=cv2.resize(imageB, dsize=(800, 800), interpolation=cv2.INTER_CUBIC)
			self.third_image=imageB.copy()
			
			imageB= Image.fromarray(imageB)
			imageB = ImageTk.PhotoImage(imageB)
		

              
			# if the panels are None, initialize them
			if self.panelC is None:
				# the first panel will store our original image
				newwinB = Toplevel(self.master)
				homography= Button(newwinB,text='Compute',command=self.compute)
				homography.pack()
				self.panelC = Label(newwinB,image=imageB)
				self.panelC.image = imageB
				self.panelC.pack()
				quitButton = Button(newwinB,text='Quit',command=newwinB.quit)
				quitButton.pack()
                		
			
			# otherwise, update the image panels
			else:
				# update the pannels
				self.panelC.quit
				self.panelC=Label(Toplevel(self.master),image=imageB)
				self.panelC.configure(image=imageB)
				#self.panelB.configure(image=imageB)
				self.panelC.image = imageB
				
    
	def select_second_image(self):
        	# open a file chooser dialog and allow the user to select an input
		# image
		#path = tkinter.filedialog.askopenfilename()  
		path='./img2/im02.jpg'
		# ensure a file path was selected
		if len(path) > 0:
			imageB = cv2.imread(path)
			

			# OpenCV represents images in BGR order; however PIL represents
			# images in RGB order, so we need to swap the channels
		
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
				#homography= Button(newwinB,text='Compute',command=self.compute)
				#homography.pack()
				self.panelB = Label(newwinB,image=imageB)
				self.panelB.image = imageB
				self.panelB.pack()
				quitButton = Button(newwinB,text='Quit',command=newwinB.quit)
				quitButton.pack()
				self.btn_third=Button(newwinB, text="Select a third image", command=self.select_third_image)	
				self.btn_third.pack()
			# otherwise, update the image panels
			else:
				# update the pannels
				self.panelB.quit
				self.panelB=Label(Toplevel(self.master),image=imageB)
				self.panelB.configure(image=imageB)
				#self.panelB.configure(image=imageB)
				self.panelB.image = imageB
		
				
	def homography_matching(self,img1,img2):
  		#Find keypoints
        # Initiate ORB detector
		orb = cv2.ORB_create()
		# find the keypoints and descriptors with ORB
		kp1, des1 = orb.detectAndCompute(img2,None)
		kp2, des2 = orb.detectAndCompute(img1,None)
		#Draw matches
		# create BFMatcher object
		bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
		# Match descriptors.
		matches = bf.match(des1,des2)
		# Sort them in the order of their distance.
		matches_sorted = sorted(matches, key = lambda x:x.distance)
		# Draw first 10 matches.
		#img3 = cv2.drawMatches(img2,kp1,img3,kp2,matches_sorted[:100],None,flags=2)
		src=[]
		dest=[]
		for match in matches_sorted[:100]:
			kp_img1=kp1[match.queryIdx]
			kp_img2=kp2[match.trainIdx]
			src.append((kp_img1.pt[0],kp_img1.pt[1]))
			dest.append((kp_img2.pt[0],kp_img2.pt[1]))         
        #Compute homography matrix
		h, status = cv2.findHomography(np.array(src), np.array(dest),cv2.RANSAC, 5.0)
		print(h)
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
		before_stitch=im_out.copy()
		im_out[translation_dist[1]:rows1+translation_dist[1],translation_dist[0]:cols1+translation_dist[0]] = img1
		return(before_stitch,im_out)
	def compute(self):
		
		_,intermediate_image=self.homography_matching(self.output,self.input)
		_,im_out=self.homography_matching(intermediate_image,self.third_image)
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