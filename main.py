#Main program

from tkinter import *

#2 Buttons

#2 Types of clicks, Left and Right

class Window(object):

    def __init__(self,master):
        pass
    def left_click(self,event):
        pass


class first_image(Window):
    def __init__(self,master):
        super().__init__(master)
        self.frametop=Frame(master)
        self.framebottom=Frame(master)
        self.frametop.pack(side=TOP)
        self.framebottom.pack(side=BOTTOM)

        #Buttons from top frame
        self.delete_button = Button(self.frametop,text = 'Delete',fg='red',command=self.delete_clicks)
        self.delete_button.grid(row=0,column=0)
        self.quitButton = Button(self.frametop,text='Quit',command=self.frametop.quit)
        self.quitButton.grid(row=0,column=1)
        

        #Canvas
        self.canvas=Canvas(self.framebottom,height=300,width=300,bg='blue')
        self.canvas2=Canvas(self.framebottom,height=300,width=300,bg='red')
        self.canvas.pack(side=LEFT)
        self.canvas2.pack(side=RIGHT)

        self.clicks_canvas=[]
        self.clicks_canvas_2=[]
        self.canvas.bind('<Button-1>',self.left_click)


    def left_click(self,event):
        super().left_click(event)
        x,y=event.x,event.y
        print('x coordinates : {}, y coordinates : {}'.format(x,y))
        print('First image')
        self.clicks_canvas.append((x,y))
        print(self.clicks_canvas)

    def delete_clicks(self):
        if len(self.clicks_canvas)>0:
            print('Deleting a point')
            self.clicks_canvas.pop()
        
        


root=Tk()
#root.geometry('300x300')
window1=first_image(root)
#window2=second_image(root)
root.mainloop()