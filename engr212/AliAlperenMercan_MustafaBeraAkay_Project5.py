from bs4 import BeautifulSoup
import os
from Tkinter import *
import tkMessageBox
from ttk import Combobox
import urllib2
import urllib
from PIL import Image, ImageTk
import time
import shelve
import pickle

class GUI(Frame):
    def __init__(self,master):
        self.master=master
        self.master.config(bg='Pink')
        self.pubnumber=0
        self.timer=0
        self.CheekiVar1 = IntVar()
        self.CheekiVar2 = IntVar()
        self.defineWidgets()
        self.placeWidgets()
        self.master.mainloop()

    def defineWidgets(self):#widgets are defined collectively
        self.titleFrame()
        self.topFrame()
        self.midFrame()
        self.botFrame()

    def placeWidgets(self):#widgets are placed collectively
        self.placeTitle()
        self.placeTop()
        self.placeMid()
        self.placeBot()

    def titleFrame(self):#title frame defined
        self.frame_title=Frame(self.master,bg='pink')
        self.title=Label(self.frame_title,text='Sehir Scholar',font='Arial 18',bg='Pink')

    def topFrame(self):#top frame defined
        self.frame_top=Frame(self.master,bg='Pink')
        self.label_url=Label(self.frame_top,text='URL for Faculty List:',font='Arial 12',bg='Pink')
        self.entry_url=Entry(self.frame_top,width=60)
        self.button_buildin=Button(self.frame_top,text='Build Index',font='Arial 12',bg='Pink',command=self.fetch_and_index)
        self.entry_filter=Entry(self.frame_top,width=80)
        self.entry_url.insert(END,"http://cs.sehir.edu.tr/en/people/")

    def midFrame(self):#mid frame defined
        self.frame_mid=Frame(self.master,bg='Pink')
        self.label_crit=Label(self.frame_mid,text='Ranking Criteria',font='Arial 12',bg='Pink')
        self.label_wgt=Label(self.frame_mid,text='Weight',font='Arial 12',bg='Pink')
        self.label_filter=Label(self.frame_mid,text='Filter Papers',font='Arial 12',bg='Pink')
        self.cheeki_freq=Checkbutton(self.frame_mid,text='Word Frequency',font='Arial 12',bg='Pink',variable=self.CheekiVar1,onvalue=1,offvalue=0)
        self.cheeki_citcount=Checkbutton(self.frame_mid,text='Citation Count',font='Arial 12',bg='Pink',variable=self.CheekiVar2,onvalue=1, offvalue=0)
        self.entry_freq=Entry(self.frame_mid,width=3)
        self.entry_citcount=Entry(self.frame_mid,width=3)
        self.scrollbar_filterbox=Scrollbar(self.frame_mid,orient=HORIZONTAL)
        self.listbox_filter=Listbox(self.frame_mid,xscrollcommand=self.scrollbar_filterbox.set)
        self.scrollbar_filterbox.config(command=self.listbox_filter.xview)
        self.button_search=Button(self.frame_mid,text='Search',font='Arial 12',bg='Pink',command=self.text_update)
        self.entry_freq.insert(END,1)
        self.entry_citcount.insert(END,1)
        self.listbox_filter.config(selectmode="multiple")

    def botFrame(self):#bot frame defined
        self.frame_bot=Frame(self.master,bg='Pink')
        self.label_timer=Label(self.frame_bot,bg='Pink',text=str(self.pubnumber)+' Publications'+'('+str(self.timer)+' seconds)')
        self.scrollbar_text=Scrollbar(self.frame_bot)
        self.text_publist=Text(self.frame_bot,height=10,yscrollcommand=self.scrollbar_text.set)
        self.scrollbar_text.config(command=self.text_publist.yview)        
        self.label_page=Label(self.frame_bot,text='Page:',font='Arial 12',bg='Pink')
        self.button_next=Button(self.frame_bot,text='Next',font='Arial 12',bg='Pink',command=self.nextButton)
        self.button_prev=Button(self.frame_bot,text='Previous',font='Arial 12',bg='Pink',command=self.prevButton)
        self.entry_pagecounter=Entry(self.frame_bot,width=2)
        self.button_clear=Button(self.frame_bot,text='Clear',font='Arial 12',bg='Pink',command=self.clear)
        self.entry_pagecounter.insert(END,"1")
        self.entry_pagecounter.config(state=DISABLED)

    def placeTitle(self):#title placed
        self.frame_title.grid(row=0)
        self.title.grid(pady=10)        

    def placeTop(self):#top frame placed
        self.frame_top.grid(row=1)
        self.label_url.grid(row=0,column=0,padx=15,pady=15)
        self.entry_url.grid(row=0,column=1,columnspan=2,padx=15,pady=15)
        self.button_buildin.grid(row=0,column=3,padx=15,pady=15)
        self.entry_filter.grid(row=1,column=0,columnspan=4,padx=15,pady=15)



    def placeMid(self):#mid frame placed
        self.frame_mid.grid(row=2)
        self.label_crit.grid(row=0,column=0,columnspan=2,padx=15,pady=10)
        self.label_wgt.grid(row=0,column=2,padx=15,pady=10)
        self.label_filter.grid(row=0,column=3,columnspan=2,padx=15,pady=10)
        self.cheeki_freq.grid(row=1,column=0,columnspan=2,padx=15,pady=10,s=W)
        self.cheeki_citcount.grid(row=2,column=0,columnspan=2,padx=15,pady=10,s=W)
        self.entry_freq.grid(row=1,column=2,padx=15,pady=10)
        self.entry_citcount.grid(row=2,column=2,padx=15,pady=10)
        self.listbox_filter.grid(row=1,column=3,columnspan=2,rowspan=2,padx=15,pady=(10,0))
        self.scrollbar_filterbox.grid(row=3,column=3,columnspan=2,s=E+W,padx=15)
        self.button_search.grid(row=1,column=5,rowspan=2,padx=15,pady=10)
        
        
    def placeBot(self):#bot frame placed
        self.frame_bot.grid(row=3)
        self.label_timer.grid(row=0,column=0,padx=15,pady=15)
        self.scrollbar_text.grid(row=1,column=12,s=N+S,padx=(0,15))
        self.text_publist.grid(row=1,column=0,columnspan=12,padx=(15,0))
        self.label_page.grid(row=2,column=8,pady=(5,15))
        self.button_next.grid(row=2,column=11,pady=(5,15))
        self.button_prev.grid(row=2,column=9,pady=(5,15))
        self.entry_pagecounter.grid(row=2,column=10,pady=(5,15))
        self.button_clear.grid(row=2,column=0,pady=(5,15))
        
    def clear(self):#clear function for development purposes
        self.frame_title.destroy()
        self.frame_top.destroy()
        self.frame_mid.destroy()
        self.frame_bot.destroy()
        self.defineWidgets()
        self.placeWidgets()

    def fetch_and_index(self):#page is crawled and data is indexed
        try:#this tries to get the data from database if backed up previously
            db = shelve.open("database", "c")
            self.pubs=db["0"]
            self.listbox_filter.delete(0, END)

            type_listo=[]
            for type in self.pubs.keys():
                type_listo.append(type)
            type_listo.sort()
            for i in type_listo:
                self.listbox_filter.insert(END, i)
            self.listbox_filter.select_set(first=0, last=END)
            db.close()

        except:#if not , we crawl the pages
            c=urllib2.urlopen(self.entry_url.get())
            contents=c.read()
            seasoned_tomato_soup=BeautifulSoup(contents,"html.parser")#page is read
            path="http://cs.sehir.edu.tr"
            peeps=[]
            doodlinks=[]
            counter=0#counters are used throughout the code since some stuff cannot be used with len() method
            teachcount=0
            for squad in seasoned_tomato_soup.find_all('section',id='people'): #no way to escape for loop
                for a in squad.find_all("a",href=True):
                    if counter%3==0:
                        peeps.append(a['href'])#the path/directory of each teacher on the /people page
                        teachcount+=1
                    counter+=1

            publications = {}
            publics =[]
            publication_type=[]
            for teacher in range(teachcount):
                publication_type.append(list())#creating lists for each teacher in publication type list
            counter=0
            teachercounter1=0
            pub_amount=0
            pub_amount_list=[]
            for link in peeps:
                d=urllib2.urlopen(path+link)
                rene=d.read()
                descartes=BeautifulSoup(rene,"html.parser")#reading pages of each teacher
                for cogitoergosum in descartes.find_all('div',id="publication"):
                    for pubname in cogitoergosum.find_all('p'):#publication names are added to our dictionary for each teacher
                        publication_type[teachercounter1].append(pubname.get_text())
                        publications.setdefault(pubname.get_text(),list())
                    for i in cogitoergosum.find_all('ul'):
                        for k in i.find_all('li'):#publications are given in their category in a ul tag , each publication is in a li tag
                            if k.get_text() not in publications[publication_type[teachercounter1][counter]]:#duplicate prevention
                                publications[publication_type[teachercounter1][counter]].append(k.get_text())
                                pub_amount+=1

                        pub_amount_list.append(pub_amount)
                        pub_amount = 0
                        counter+=1
                    counter=0
                teachercounter1+=1
            self.pubs={}
            tempy=" "
            type_listo=[]
            for type in publications.keys():
                type_listo.append(type)#each paper type is listed
                for pub in publications[type]:
                        self.pubs.setdefault(type,list())
                        kek=pub.split()
                        kek2=tempy.join(kek)
                        kek2=kek2.split(' ',1)[1]#cleaning the publication from ranking on the page and \ns an whatnot
                        if kek2 not in self.pubs[type]:#duplicate prevention
                            self.pubs[type].append(kek2)#cleaned dictionary of all publications divided into groups by their categories
            self.listbox_filter.delete(0,END)
            type_listo.sort()
            for i in type_listo:#listed paper types are put into the listbox
                self.listbox_filter.insert(END,i)
            self.listbox_filter.select_set(first=0, last=END)#default selection for listbox

            db=shelve.open("database","c")#we create a database for uses in the future runs of the code
            db["0"]=self.pubs
            db.close()
    def wordFreq(self):#frequency score calculated
        filthy=self.entry_filter.get().split()#keywords are read from the entry
        score={}
        for word in filthy:
            for type in self.pubs.keys():
                for pub in self.pubs[type]:
                    for words in pub.split():#searching for our keywords in the publications
                        if word.lower()==words.lower():#if matching words are found, the score of the keyword is increased
                            score.setdefault(type+"."+pub,dict())
                            score[type+"."+pub].setdefault(word,0)
                            score[type+"." + pub][word]+=1#score for each keyword is increased
        scoreupdate={}
        for key in score.keys():
            for word in score[key].keys():
                scoreupdate.setdefault(key,1)
                scoreupdate[key]=scoreupdate[key]*score[key][word]#the score of each keyword is combined for each publication
                            
        return self.normalizescores(scoreupdate)#scores normalized

    def citCount(self):#citation score counted
        score = {}
        for type in self.pubs.keys():
           for pub in self.pubs[type]:
               try:#try-except is used since if no citation amount found except works , if found try works
                   cit=int(pub.split("[")[1][:-1].split(" ")[0])#if the citation amount is mentioned at the end of the publication , it is read
               except:
                   cit=0#if no citation amount is read , 
               score.setdefault(type + "." + pub, 0)
               score[type + "." + pub] = cit#citation amount is added to our score dictionary

        return self.normalizescores(score)#scores normalized

    def scoreCombiner(self):#scores are combined (or not depending on the user's choice)
        score={}
        scorex={}
        for type in self.pubs.keys():
            score.setdefault(type, dict())
            for pub in self.pubs[type]:#for each publication the final score is 
                    try:
                        if self.wordFreq()[type+"."+pub]!=0 and self.CheekiVar1.get()==1 and self.CheekiVar2.get()==1:
                            wgt_wordfreq = float(self.entry_freq.get())
                            wgt_citcount = float(self.entry_citcount.get())
                            scorex.setdefault(type+'.'+pub,0)#scores are combined according to weights in line below
                            scorex[type+'.'+pub]=(wgt_citcount*(self.citCount()[type+"."+pub])+wgt_wordfreq*(self.wordFreq()[type+"."+pub]))/wgt_wordfreq+wgt_citcount#added to another dict to be normalized later
                        elif self.CheekiVar2.get()==1 and self.CheekiVar1.get()!=1:
                            score[type].setdefault(pub,0)
                            score[type][pub]="%.3f" % round(self.citCount()[type+"."+pub],4)#each score is re entered to be dict-in-dict
                        elif self.wordFreq()[type+"."+pub]!=0 and self.CheekiVar1.get()==1 and self.CheekiVar2.get()!=1:
                            score[type].setdefault(pub,0)
                            score[type][pub]="%.3f" % round(self.wordFreq()[type+"."+pub],4)#each score is re entered to be dict-in-dict
                    except:
                        pass
        if self.CheekiVar1.get()==1 and self.CheekiVar2.get()==1:
            self.normalizescores(scorex)#scores normalized
            for type in self.pubs.keys():
                score.setdefault(type, dict())
                for pub in self.pubs[type]:
                    try:
                        if self.wordFreq()[type+"."+pub]!=0:
                            score[type].setdefault(pub, 0)
                            score[type][pub]="%.3f" % round(scorex[type+'.'+pub],4)#each score is re entered to be dict-in-dict
                    except:
                       pass

        return score

    def text_update(self):#fills the text widget with publications
        if self.entry_filter.get() == "":#if no keyword is declared , an error is given
            tkMessageBox.showinfo("Not Enough Parameters", "You must declare at least one keyword")
            return

        if self.CheekiVar1.get() != 1 and self.CheekiVar2.get() != 1:#if no ranking criteria is selected, an error is given
            tkMessageBox.showinfo("Not Enough Parameters", "You must select at least one ranking criteria")
            return

        currently_selected = self.listbox_filter.curselection()
        if len(currently_selected)<1:#if no paper type is selected, an error is given
            tkMessageBox.showinfo("Not Enough Parameters","You must select at least one paper type")
            return

        try:
            if self.CheekiVar1.get()==1 and self.CheekiVar2.get()==1:#checks if the weights are entered for for both criteria, if only one selected , no weight needed, so no problem there
                a=(float(self.entry_freq.get())*5)/10
                a=(float(self.entry_citcount.get())*5)/10#if the calculations fail here , it means the entries do not fit
        except:
            tkMessageBox.showinfo("Not Enough Parameters","You must declare the weights of your ranking criteria")#if weights arent declared when both criteria are checked , it gives an error

        self.entry_pagecounter.config(state=NORMAL)#pagecounter entry widget enabled for editing
        self.entry_pagecounter.delete(0,END)#pagecounter cleared
        self.entry_pagecounter.insert(END,str(1))#new page number entered to entry widget
        self.entry_pagecounter.config(state=DISABLED)#pagecounter entry widget disabled for editing

        start_time=time.time()#search timer starts
        self.text_publist.config(state=NORMAL)#text widget state is changed so we can edit
        self.text_publist.delete(1.0,END)#text widget is cleared
        
        curselect=[]
        for i in currently_selected:#currently selected paper types are read
            curselect.append(self.listbox_filter.get(i))
            
        getDict=self.scoreCombiner()#score combiner called to get scores
        self.pablo=[]
        for papertype in curselect:
            for pub in getDict[papertype]:
                a=(getDict[papertype][pub],pub)#each publication is added to our list with its score
                self.pablo.append(a)
        self.pablo.sort(reverse=True)#sorted by descending order for scores
        x=len(self.pablo)
        lastpage=x%10
        otherpages=int(x/10)#page amount is calculated
        self.fabulous_pablo={}
        count = 1
        pagecount=1
        a = 0
        b = 10
        for page in range(otherpages):#pages other than last page
            self.fabulous_pablo.setdefault(pagecount,list())
            for item in self.pablo[a:b]:
                self.fabulous_pablo[pagecount].append(str(count) + "." + item[1] + " " + str(item[0]) + "\n")#pubs are put in our dictionary and are divided in that dictionary according to page
                count += 1
            a=a+10#10 entries per page
            b=b+10
            pagecount+=1

        self.fabulous_pablo.setdefault(otherpages+1, list())
        for item in self.pablo[a:]:#last page
            self.fabulous_pablo[otherpages+1].append(str(count) + "." + item[1] + " " + str(item[0]) + "\n")#pubs are put in our dictionary and are divided in that dictionary according to page

            count += 1

        for item in self.fabulous_pablo[int(self.entry_pagecounter.get())]:#reads data from the pagecounter at the bottom of te UI and writes that page into the text widget
            self.text_publist.insert(END, item)

        self.highlight()#highlighter called
        self.text_publist.config(state=DISABLED)#text widget disabled to keep the user from writing on it

        end_time = time.time()#search timer stopped
        self.pubnumber = x#pubnumber = len(pablo), our list of matching publications
        self.timer=end_time-start_time#total time calculated
        self.label_timer.destroy()#publication amount and timer destroyed to be re entered
        self.label_timer = Label(self.frame_bot, bg='Pink',text=str(self.pubnumber) + ' Publications' + '(' + str(self.timer) + ' seconds)')#timer and publication amount re entered to UI
        self.label_timer.grid(row=0, column=0, padx=15, pady=15)

    def highlight(self):#highlighter for keywords
        for item in self.entry_filter.get().split():#reads the keywords from the entry widget
            item = item.lower()#lowers the word
            start = "1.0"#starts for 2 types of highlighting
            start2 = "1.0"
            countVar = StringVar()#word length counter
            countVar2 = StringVar()
            big = item[0].upper() + item[1:]
            while True:#all lowercase word
                pos = self.text_publist.search(item, start, stopindex="end", count=countVar, regexp=True)#word location found
                if not pos:#if no word found the loop is broken
                    break
                self.text_publist.tag_add(item, pos, "%s + %sc" % (pos, countVar.get()))#word start and end selected as tag
                self.text_publist.tag_configure(item, font="Arial 9 bold", foreground="blue")#tag color changed and made bold
                start = "%s + %sc" % (pos, countVar.get())#start is made the end of the first word found 
            while True:#first letter capitalized word
                pos2 = self.text_publist.search(big, start2, stopindex="end", count=countVar2, regexp=True)#same as above for this loop
                if not pos2:
                    break
                self.text_publist.tag_add(big, pos2, "%s + %sc" % (pos2, countVar2.get()))
                self.text_publist.tag_configure(big, font="Arial 9 bold", foreground="blue")
                start2 = "%s + %sc" % (pos2, countVar2.get())
        for item in self.fabulous_pablo[int(self.entry_pagecounter.get())]:#same loop for scores
            score=str(item.split()[-1])#score for each publication
            print score
            start3="1.0"
            counter=5
            while True:
                pos3 = self.text_publist.search(score,start3,stopindex="end",regexp=True)
                if not pos3:
                    break
                self.text_publist.tag_add(score,pos3,"%s+%sc"%(pos3,counter))
                self.text_publist.tag_configure(score,font="Arial 9 bold",foreground='red')
                start3="%s+%sc"%(pos3,counter)

    def nextButton(self):#next page button function
        self.text_publist.config(state=NORMAL)#text put to normal state for editing
        self.text_publist.delete(1.0,END)#text cleared
        pagecount=int(self.entry_pagecounter.get())#page counter read
        pagecount+=1#pagecounter increased
        self.entry_pagecounter.config(state=NORMAL)#pagecounter entry widget enabled for editing
        self.entry_pagecounter.delete(0,END)#pagecounter cleared
        self.entry_pagecounter.insert(END,str(pagecount))#new page number entered to entry widget
        try:
            for item in self.fabulous_pablo[int(self.entry_pagecounter.get())]:
                self.text_publist.insert(END, item)#that pages info is put into the text widget
            self.highlight()#highlighter called again
        except:
            tkMessageBox.showinfo("ERROR","No more pages")#if theere is an error it means no more pages left
            self.prevButton()#if no more pages in that direction, goes 1 page the other way
        self.entry_pagecounter.config(state=DISABLED)#disabled to keep user from editing
        self.text_publist.config(state=DISABLED)#disabled to keep user from editing

    def prevButton(self):#previous page button function
        self.text_publist.config(state=NORMAL)#same function as above
        self.text_publist.delete(1.0,END)
        pagecount=int(self.entry_pagecounter.get())
        pagecount-=1###################################only difference , it lowers the pagecounter
        self.entry_pagecounter.config(state=NORMAL)
        self.entry_pagecounter.delete(0, END)
        self.entry_pagecounter.insert(END, str(pagecount))
        try:
            for item in self.fabulous_pablo[int(self.entry_pagecounter.get())]:
                self.text_publist.insert(END, item)
            self.highlight()
        except:
            tkMessageBox.showinfo("ERROR", "No more pages")
            self.nextButton()
        self.entry_pagecounter.config(state=DISABLED)
        self.text_publist.config(state=DISABLED)

    def normalizescores(self, scores, smallIsBetter=0):#taken from mysearchengine.py 
        vsmall = 0.00001  # Avoid division by zero errors
        if smallIsBetter:
            minscore = min(scores.values())
            minscore = max(minscore, vsmall)
            return dict([(u, float(minscore) / max(vsmall, l)) for (u, l) \
                         in scores.items()])
        else:
            maxscore = max(scores.values())
            if maxscore == 0:
                maxscore = vsmall
            return dict([(u, float(c) / maxscore) for (u, c) in scores.items()])

if __name__=='__main__':#callings
    bob=Tk()
    master=GUI(bob)
