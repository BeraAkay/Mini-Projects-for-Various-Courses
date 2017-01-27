from Tkinter import *
import os
from PIL import ImageTk , Image
from tkColorChooser import askcolor

class Paint:
    def __init__(self,master):
        self.master=master
        self.master.resizable(width=False,height=False)
        self.master.config(bg='Indian Red')
        self.images()
        self.mode=StringVar()
        self.mode.set('line')
        self.fillcolor='Black'
        self.bordcolor='Black'
        self.topFrame()
        self.botFrame()
        self.mode.trace('w',self.cursorChange) #if the tool changes trace method calls the cursorchange function
        self.master.mainloop()

    def images(self): #images are opened
        self.imdrag=ImageTk.PhotoImage(file=os.getcwd()+'/assets/drag.png')
        self.imeraser=ImageTk.PhotoImage(file=os.getcwd()+'/assets/eraser.png')
        self.imline=ImageTk.PhotoImage(file=os.getcwd()+'/assets/line.png')
        self.imoval=ImageTk.PhotoImage(file=os.getcwd()+'/assets/oval.png')
        self.imrect=ImageTk.PhotoImage(file=os.getcwd()+'/assets/rectangle.png')
        
    def topFrame(self):
        self.topWidgets()
        self.topPlace()

    def botFrame(self):
        self.botWidgets()
        self.botPlace()

    def topWidgets(self):
        self.frame_top=Frame(self.master)
        self.label_title=Label(self.frame_top,text='My Paint',font='Arial 25',bg='Indian Red',fg='gold')        

    def botWidgets(self):
        self.frame_bot=Frame(self.master,bg='gold')
        self.rect=Radiobutton(self.frame_bot,image=self.imrect,variable=self.mode,value='rect',indicatoron=0,height=25) #instead of using the suggested events and labels combo we used radiobuttons
        self.oval=Radiobutton(self.frame_bot,image=self.imoval,variable=self.mode,value='oval',indicatoron=0,height=25) 
        self.line=Radiobutton(self.frame_bot,image=self.imline,variable=self.mode,value='line',indicatoron=0,height=25)
        self.drag=Radiobutton(self.frame_bot,image=self.imdrag,variable=self.mode,value='drag',indicatoron=0,height=25)
        self.eraser=Radiobutton(self.frame_bot,image=self.imeraser,variable=self.mode,value='eraser',indicatoron=0,height=25)
        self.fill=Label(self.frame_bot,text='Fill Color',bg='gold')
        self.fillcol=Button(self.frame_bot,command=self.getColorfill,bg=self.fillcolor,width=2,relief=FLAT)
        self.bord=Label(self.frame_bot,text='Border Color',bg='gold')
        self.bordcol=Button(self.frame_bot,command=self.getColorbord,bg=self.bordcolor,width=2,relief=FLAT)
        self.thick=Label(self.frame_bot,text='Weight',bg='gold')
        self.thicc=Spinbox(self.frame_bot,from_=1,to=50,width=3)
        self.clear=Button(self.frame_bot,text='Clear ALL',command=self.clear)
        self.canvas=Canvas(self.frame_bot,bg='White',width=1200,height=600,cursor=self.cursor())
        self.canvas.bind('<B1-Motion>',self.clickmove)
        self.canvas.bind('<Button-1>',self.start)
        self.bg=Button(self.frame_bot,text='Background Color',command=self.bgColor)

    def cursor(self): #Detects which cursor is going to used
        if self.mode.get()=='rect' or self.mode.get()=='oval' or self.mode.get()=='line':
            return 'cross'
        elif self.mode.get()=='drag':
            return 'hand2' #We werent able to find the tag that the assistant used on the video
        elif self.mode.get()=='eraser':
            return 'X_cursor'

    def cursorChange(self,*args): #callback function for the tool change to change the cursor
        self.canvas.config(cursor=self.cursor())

    def bgColor(self): #changes canvas bg color using askcolor method
        color=askcolor()
        self.canvas.config(bg=color[1])# second item in askcolor method is the rgb value
   
    def getColorfill(self): #changes fill color using askcolor method
        color=askcolor()
        self.fillcol.config(bg=color[1])
        self.fillcolor=color[1]

    def getColorbord(self): #changes border color using askcolor method
        color=askcolor()
        self.bordcol.config(bg=color[1])
        self.bordcolor=color[1]

    def topPlace(self): #topframe grid functions
        self.frame_top.grid(row=0)
        self.label_title.grid()

    def botPlace(self): #botframe grid functions
        self.frame_bot.grid(row=1)
        self.rect.grid(row=1,column=195,padx=0)
        self.oval.grid(row=1,column=196,padx=0)
        self.line.grid(row=1,column=197,padx=0)
        self.drag.grid(row=1,column=198,padx=0)
        self.eraser.grid(row=1,column=199,padx=0)
        self.fill.grid(row=1,column=200,padx=0)
        self.fillcol.grid(row=1,column=201,padx=0)
        self.bord.grid(row=1,column=202,padx=0)
        self.bordcol.grid(row=1,column=203,padx=0)
        self.thick.grid(row=1,column=204,padx=0)
        self.thicc.grid(row=1,column=205,padx=0)
        self.canvas.grid(row=2,columnspan=400)
        self.clear.grid(row=1,column=399)
        self.bg.grid(row=1,column=398)

    def start(self,event): #initial clicking position
        self.startx,self.starty=event.x,event.y
        self.shape=None
        self.canvas.widget=event.widget#clicked widget
        if self.mode.get()=='eraser':
            self.canvas.widget.delete('current')#currently clicked object in widget is deleted

    def clickmove(self,event):#since the event tracks the movement of mouse when the m1 button is clicked , we can use it like a for loop in some parts 
        if self.mode.get()=='rect':
            if self.shape: #if the user changes shape without letting go of click we delete the prevous shape 
                self.canvas.delete(self.shape)
            obj=self.canvas.create_rectangle(event.x,event.y,self.startx,self.starty,fill=self.fillcolor,outline=self.bordcolor,width=int(self.thicc.get()))
            self.shape=obj #we record the current object id to delete if the user keep changing without letting go of the click
        elif self.mode.get()=='oval': #same as rectangle
            if self.shape:
                self.canvas.delete(self.shape)
            obj=self.canvas.create_oval(self.startx,self.starty,event.x,event.y,fill=self.fillcolor,outline=self.bordcolor,width=int(self.thicc.get()))
            self.shape=obj
        elif self.mode.get()=='line': #same as rectangle
            if self.shape:
                self.canvas.delete(self.shape)
            obj=self.canvas.create_line(event.x,event.y,self.startx,self.starty,fill=self.fillcolor,width=int(self.thicc.get()))
            self.shape=obj
        elif self.mode.get()=='drag': #we calculate the change amount by the difference between x and y values of the previous and current cursor position 
                x,y=(event.x-self.startx ), (event.y-self.starty)
                self.canvas.widget.move('current',x,y) #we move the currently selected object with the calculated x and y values
                self.startx,self.starty=event.x,event.y #we update previous x and y values for the next use

    def clear(self):#clear all function
        self.canvas.delete('all')
        
if __name__=='__main__':
    bob=Tk()
    master=Paint(bob)
