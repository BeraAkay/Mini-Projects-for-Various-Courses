from Tkinter import *
from ttk import Combobox
import os
import tkFileDialog
import tkMessageBox
import anydbm
import pickle
from xlrd import open_workbook
import recommendations as rcm


class Legwork:
    def __init__(self):#these could have been in the second class but i
        #made this anyway for the initial definings for the stuff not directly related to GUI
        self.menu=open_workbook('Menu.xlsx')
        self.sheet=self.menu.sheet_by_index(0)
        self.meals=[self.sheet.cell(index,0).value for index in range(1,68)]
        self.userratings=anydbm.open('userratings.db','c')
        self.ratings=anydbm.open('cc_ratings.db','c')
        self.ratdict={'currentuser':{}}
        for meals in self.userratings.keys():
            self.ratdict['currentuser'][pickle.loads(meals)]=int(self.userratings[meals])
        for users in self.ratings.keys():
            self.ratdict[users]=pickle.loads(self.ratings[users])

class GUI(Frame,Legwork):
    def __init__(self,root):#basic definings and other initial callings are made here
        self.root=root
        self.methop=StringVar()
        self.methop.set('userbased')
        self.recop=StringVar()
        self.recop.set('sim_distance')
        self.recnumber=StringVar()
        self.recnumber.set('10')
        self.simscore=[]
        self.recmeals=[]
        self.mymeals=[]
        self.similaritems=[]
        Legwork.__init__(self)
        Frame.__init__(self)
        self.initUI()
        
    def initUI(self):#calls to initialize the frame creating functions below
        self.grid()
        self.title_frame()
        self.rate_frame()
        self.op_frame()
        self.rec_frame()

    def title_frame(self):#title is defined here
        self.titleframe=Frame(self,background='Blue')
        self.titleframe.grid(row=0,sticky=W+E)
        self.title=Label(self.titleframe,text='Cafe Crown Meal Recommendation Engine',foreground='White',background='Blue',font='Arial 26')
        self.title.grid(row=0,pady=15,padx=55)

    def rate_frame(self):#creating the top frame which takes users ratings
        self.rateframe=Frame(self)
        self.rateframe.grid(row=1)
        self.meallabel=Label(self.rateframe,text='Choose a Meal:',foreground='Blue',font='Arial 15')
        self.meallabel.grid(row=0,column=0,padx=(0,35))
        self.meallister=Combobox(self.rateframe,values=self.meals,state='readonly')
        self.meallister.current(0)
        self.meallister.grid(row=1,column=0,padx=(0,35))
        self.ratelabel=Label(self.rateframe,text='Enter Rating:',foreground='Blue',font='Arial 15')
        self.ratelabel.grid(row=0,column=1)
        self.ratescale=Scale(self.rateframe,from_=1,to=10,orient=HORIZONTAL)
        self.ratescale.grid(row=1,column=1)
        self.ratingsscroll=Scrollbar(self.rateframe)
        self.ratingsscroll.grid(row=0,column=4,rowspan=2,sticky=N+S)
        self.scrollhori=Scrollbar(self.rateframe,orient=HORIZONTAL)
        self.scrollhori.grid(row=2,column=3,sticky=W+E)
        self.myratings=Listbox(self.rateframe,yscrollcommand=self.ratingsscroll.set,xscrollcommand=self.scrollhori.set,height=6,width=25)
        self.myratings.grid(row=0,rowspan=2,column=3)
        self.ratebut=Button(self.rateframe,text='Rate Selected',command=self.rate)
        self.ratebut.grid(row=1,column=2,padx=35)
        self.deleterate=Button(self.rateframe,text='Remove Selected',foreground='Red',command=self.removerate)
        self.deleterate.grid(row=0,rowspan=2,column=5,padx=20)
        for meal in self.userratings.keys():
            self.myratings.insert(END,pickle.loads(meal)+'>'+str(self.userratings[meal]))
        self.ratingsscroll.config(command=self.myratings.yview)
        self.scrollhori.config(command=self.myratings.xview)

    def op_frame(self):#middle frame with the small frame in it is defined here
        self.opframe=Frame(self,width=10)
        self.opframe.grid(row=2)
        self.oplabel=Label(self.opframe,text='Options',foreground='Blue',font='Arial 15')
        self.oplabel.grid(row=0,column=0,sticky=W,padx=10)
        self.recno=Frame(self.opframe)
        self.recno.grid(row=1,column=0,sticky=W,rowspan=6)
        self.amountlabel=Label(self.recno,text='Number of Recommendations')
        self.amountlabel.grid(row=0,column=0,padx=10)
        self.amount=Entry(self.recno,width=2,textvariable=self.recnumber)
        self.amount.grid(row=0,column=1)
        self.emptylabel=Label(self.opframe,text=' '*50)
        self.emptylabel.grid(row=1,column=2)
        self.radmethlabel=Label(self.opframe,text='Select Recommendation Method',foreground='Blue')
        self.radmethlabel.grid(row=1,column=3)
        self.radmeth1=Radiobutton(self.opframe,text='User-based',variable=self.methop,value='userbased')
        self.radmeth1.grid(row=2,column=3)
        self.radmeth2=Radiobutton(self.opframe,text='Item-based',variable=self.methop,value='itembased')
        self.radmeth2.grid(row=3,column=3)
        self.radreclabel=Label(self.opframe,text='Select Recommendation Metric',foreground='Blue')
        self.radreclabel.grid(row=4,column=3)
        self.radrec1=Radiobutton(self.opframe,text='Euclidean Score',variable=self.recop,value='sim_distance')
        self.radrec1.grid(row=5,column=3)
        self.radrec2=Radiobutton(self.opframe,text='Pearson Score   ',variable=self.recop,value='sim_pearson')
        self.radrec2.grid(row=6,column=3)
        self.radrec3=Radiobutton(self.opframe,text='Jaccard Score    ',variable=self.recop,value='sim_jaccard')
        self.radrec3.grid(row=7,column=3)
        self.recommendbutton=Button(self.opframe,text='Get Recommendations',command=self.recommend)
        self.recommendbutton.grid(row=0,rowspan=8,column=4,padx=35)
        
    def rec_frame(self):#the lower frame is defined here
        self.recframe=Frame(self)
        self.recframe.grid(row=3,columnspan=3)
        self.ratetitle=Label(self.recframe,text='Recommendations',foreground='Blue',font='Arial 15')
        self.ratetitle.grid(row=0,column=0)
        self.midbox=StringVar()
        self.midbox.set('Similar users')
        self.similaruser=Label(self.recframe,text=self.midbox.get(),foreground='Blue',font='Arial 15')
        self.similaruser.grid(row=0,column=2,padx=(35,0))
        self.selecteduser=Label(self.recframe,text="Selected Ratings",foreground='Blue',font='Arial 15')
        self.selecteduser.grid(row=0,column=4,padx=(35,0))
        self.resscroll=Scrollbar(self.recframe)
        self.resscroll.grid(row=1,column=1,sticky=N+S)
        self.userscroll=Scrollbar(self.recframe)
        self.userscroll.grid(row=1,column=3,sticky=N+S)
        self.usrrscroll=Scrollbar(self.recframe)
        self.usrrscroll.grid(row=1,column=5,sticky=N+S+E)
        self.resbox=Listbox(self.recframe,yscrollcommand=self.resscroll.set,height=5,width=35)
        self.resbox.grid(row=1,column=0,padx=0)
        self.userbox=Listbox(self.recframe,yscrollcommand=self.userscroll.set,height=5,width=35)
        self.userbox.grid(row=1,column=2,padx=(35,0))
        self.userbox.bind("<<ListboxSelect>>",self.userreader)
        self.ussrbox=Listbox(self.recframe,yscrollcommand=self.usrrscroll.set,height=5,width=35)
        self.ussrbox.grid(row=1,column=4,padx=(35,0),sticky=E)
        self.resscroll.config(command=self.resbox.yview)
        self.userscroll.config(command=self.userbox.yview)
        self.usrrscroll.config(command=self.ussrbox.yview)

    def userreader(self,event):#this is the event that triggers if user selects an item from the middle bottom box
        self.ussrbox.delete(0,END)
        if self.methop.get()=='userbased':
            i=0
            username=self.userbox.get(self.userbox.curselection())
            while  self.userbox.get(self.userbox.curselection())[i]!='>':
                i+=1
            username=username[:i]
            for meals in self.ratdict[username].keys():
                self.ussrbox.insert(END,meals+'>'+str(self.ratdict[username][meals]))
        elif self.methop.get()=='itembased':#this doesnt quite work since the function in the recommendations module doesnt quite work.
            for meals in self.similaritems[0:10]:#so i wrote something to just fill the gap
                self.ussrbox.insert(END,meals)

    def recommend(self):#this function calls and connects the results of the functions of recommendations.py
        recom=[]
        self.resbox.delete(0,END)
        self.userbox.delete(0,END)
        if self.recop.get()=='sim_distance':
            recom=rcm.getRecommendations(self.ratdict,'currentuser',rcm.sim_distance)
            similaruser=rcm.topMatches(self.ratdict,'currentuser',10,rcm.sim_distance)
            for score,item in recom[:int(self.recnumber.get())]:
                self.resbox.insert(END,item+'>'+str(score))
        elif self.recop.get()=='sim_pearson':
            recom=rcm.getRecommendations(self.ratdict,'currentuser')
            similaruser=rcm.topMatches(self.ratdict,'currentuser',10)
            if len(recom)==0:
                tkMessageBox.showinfo("You're Special",'No similar user found')
            else:
                for score,item in recom[:int(self.recnumber.get())]:
                    self.resbox.insert(END,item+'>'+str(score))
        elif self.recop.get()=='sim_jaccard':
            recom=rcm.getRecommendations(self.ratdict,'currentuser',rcm.sim_jaccard)
            similaruser=rcm.topMatches(self.ratdict,'currentuser',10,rcm.sim_jaccard)
            for score,item in recom[:int(self.recnumber.get())]:
                 self.resbox.insert(END,item+'>'+str(score))
        if self.methop.get()=='userbased':
            self.midbox.set('Similar Users')
            self.similaruser.destroy()
            self.similaruser=Label(self.recframe,text=self.midbox.get(),foreground='Blue',font='Arial 15')        
            self.similaruser.grid(row=0,column=2,padx=(35,0))
            for sim,user in similaruser:
                if sim>0:
                    self.userbox.insert(END,user+'>'+str(sim))
                else:
                    pass
        elif self.methop.get()=='itembased':#this doesnt quite work since the function in the recommendations module doesnt quite work.
            #so i wrote something to just fill the gap
            self.midbox.set('Your Items')
            self.similaruser.destroy()
            self.similaruser=Label(self.recframe,text=self.midbox.get(),foreground='Blue',font='Arial 15')        
            self.similaruser.grid(row=0,column=2,padx=(35,0))
            similaruser=similaruser[:len(similaruser)]
            self.similaritems=[]
            for user in similaruser:
                for meal in self.ratdict[user[1]].keys():
                    if self.ratdict[user[1]][meal]>=6:
                        self.similaritems.append(meal)
            for item in self.ratdict['currentuser'].keys():
                self.userbox.insert(END,item)
            
    def rate(self):#this function is what user rates with, tells user to remove a rating in order to re add it
        item=self.meallister.get()
        score=self.ratescale.get()
        if item in self.ratdict['currentuser'].keys():
            tkMessageBox.showinfo('Whoops','That is already rated. If you want to change , remove rating first')
        else:
            self.userratings[pickle.dumps(item)]=str(score)
            self.ratdict['currentuser'][item]=score
            self.myratings.insert(END,self.meallister.get()+'>'+str(score))
            self.userratings.close()
            self.userratings=anydbm.open('userratings.db','c')
        
            
    def removerate(self):#this function removes rates , gives an error if no item is selected in the Listbox and tells user to select one
        try:
            itemnameraw=self.myratings.get(self.myratings.curselection())
            i=0
            while itemnameraw[i]!='>':
                i+=1
            itemname=itemnameraw[:i]
            item=self.myratings.curselection()[0]
            self.myratings.delete(int(item),int(item))
            del self.ratdict['currentuser'][itemname]
            del self.userratings[pickle.dumps(itemname)]
            self.userratings.close()
            self.userratings=anydbm.open('userratings.db','c')
        except NameError:
            tkMessageBox.showinfo('No Item Selected','Select an Item to Remove')


root=Tk()
master=GUI(root)
master.mainloop()

