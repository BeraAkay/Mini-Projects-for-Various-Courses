from Tkinter import *
import tkMessageBox
import urllib2
import urllib
from bs4 import BeautifulSoup
from selenium import webdriver
from xlrd import open_workbook
import tkFileDialog

class GUI(Frame):
    def __init__(self,master):
        self.master=master
        self.master.config(background='indian red')
        self.master.resizable( width = False, height = False )
        self.timer=0
        self.CheckVar1 = IntVar()
        self.CheckVar2 = IntVar()
        self.defineWidgets()
        self.placeWidgets()
        self.links=['http://www.sehir.edu.tr/en/Pages/Academic/Bolum.aspx?BID=12','http://www.sehir.edu.tr/en/Pages/Academic/Bolum.aspx?BID=13','http://www.sehir.edu.tr/en/Pages/Academic/Bolum.aspx?BID=14','http://www.sehir.edu.tr/en/Pages/Academic/Bolum.aspx?BID=32']
        for link in self.links:
            self.listbox_url.insert(END,link)
        self.all_courses={}
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

    def titleFrame(self):
        self.frame_title=Frame(self.master,background='indian red')
        self.label_title=Label(self.frame_title,text='Guess My Grade',font='Arial 25',foreground='White',background='indian red')
        
    def topFrame(self):
        self.frame_top=Frame(self.master)
        self.label_browse=Label(self.frame_top,text='Please Upload your Curriculum File with the Grades',font='Arial 15')
        self.button_browse=Button(self.frame_top,text='Browse',background='indian red',foreground='White',font='Arial 15',command=self.readExcel)
        self.label_url=Label(self.frame_top,text='     Enter URLs for Course Descriptions',font='Arial 15')
        
    def midFrame(self):
        self.frame_mid=Frame(self.master)
        self.frame_url=Frame(self.frame_mid)
        self.entry_url=Entry(self.frame_url,width=63)
        self.button_url=Button(self.frame_url,text='Add URL',background='indian red',foreground='White',font='Arial 15',command=self.addUrl)
        self.button_delurl=Button(self.frame_url,text='Remove URL',background='indian red',foreground='White',font='Arial 15',command=self.removeUrl)
        self.listbox_url=Listbox(self.frame_url,width=108)
        self.label_key=Label(self.frame_mid,text='   Key:',font='Arial 15')
        self.label_A=Label(self.frame_mid,text='   A   ',background='green',font='Arial 20',foreground='White')
        self.label_B=Label(self.frame_mid,text='   B   ',background='pale green',font='Arial 20',foreground='White')
        self.label_C=Label(self.frame_mid,text='   C   ',background='orange',font='Arial 20',foreground='White')
        self.label_D=Label(self.frame_mid,text='   D   ',background='red',font='Arial 20',foreground='White')
        self.label_F=Label(self.frame_mid,text='   F   ',background='black',font='Arial 20',foreground='White')
        self.button_predict=Button(self.frame_mid,command=self.predict,text='Predict Grades',background='indian red',foreground='White',font='Arial 15')

    def botFrame(self):
        self.frame_bot=Frame(self.master)
        self.label_grades=Label(self.frame_bot,text='  Predicted Grades',font='Arial 15')
        self.scrollbar_grades=Scrollbar(self.frame_bot)
        self.listbox_grades=Listbox(self.frame_bot,width=109,yscrollcommand=self.scrollbar_grades.set)
        self.scrollbar_grades.config(command=self.listbox_grades.yview)
        
        
    def placeTitle(self):
        self.frame_title.grid(row=0)
        self.label_title.grid()
        
    def placeTop(self):
        self.frame_top.grid(row=1)
        self.label_browse.grid(row=0,column=0,sticky=W,padx=(25,59),pady=5)
        self.button_browse.grid(row=0,column=1,padx=35,pady=40)
        self.label_url.grid(row=1,s=W,column=0,pady=10)
        
    def placeMid(self):
        self.frame_mid.grid(row=2)
        self.frame_url.grid(row=0,columnspan=6,padx=(13,18))
        self.entry_url.grid(row=0,column=0,sticky=W,padx=(7,7))
        self.button_url.grid(row=0,column=1,padx=10)
        self.button_delurl.grid(row=0,column=2,padx=10)
        self.listbox_url.grid(row=1,column=0,columnspan=4,pady=15)
        self.label_key.grid(row=2,column=0,sticky=W)
        self.label_A.grid(row=3,padx=10,column=0)
        self.label_B.grid(row=3,padx=10,column=1)
        self.label_C.grid(row=3,padx=10,column=2)
        self.label_D.grid(row=3,padx=10,column=3)
        self.label_F.grid(row=3,padx=10,column=4)
        self.button_predict.grid(row=3,column=5,padx=12)
        
    def placeBot(self):
        self.frame_bot.grid(row=4)
        self.label_grades.grid(row=0,column=0,sticky=W,padx=7,pady=(5,0))
        self.listbox_grades.grid(row=1,column=0,padx=(10,0),pady=10)
        self.scrollbar_grades.grid(row=1,column=1,sticky=N+S,padx=(0,11),pady=10)

    def addUrl(self):
        url=self.entry_url.get()
        self.listbox_url.insert(END,url)

    def removeUrl(self):
        urlindex=self.listbox_url.curselection()
        self.listbox_url.delete(urlindex)

        
    def readUrl(self):#this function tries to get course names (but fails miserably for EE and CS)
        links=self.listbox_url.get(0,END)
        for link in links:
            if link[-2:]=='32':
                c=urllib2.urlopen(link)
                deck=BeautifulSoup(c.read(),'html.parser')
                for soup in deck.find_all('div','fakulte_ack'):
                    var=soup.find_all('p')
                unidesc=[]
                for item in var[4:]:
                    unidesc.append(item.get_text())
                
                unititle=[]
                for index in range(len(unidesc)):
                    try:
                        if str(unidesc[index][:3])=='UNI':
                            unititle.append(unidesc[index][:7])
                            self.all_courses[unidesc[index][:7]]=unidesc[index+2].split()
                        if str(unidesc[index][:4])=='*UNI':
                            unititle.append(unidesc[index][1:8])
                            self.all_courses[unidesc[index][1:8]]=unidesc[index+2].split()
                    except:
                        pass
                #cheapskate
                self.all_courses[u'UNI 112']=self.all_courses[u'UNI 111']
                self.all_courses[u'UNI 124']=self.all_courses[u'UNI 123']
                self.all_courses[u'UNI 222']=self.all_courses[u'UNI 221']
                q=[u'UNI 116',u'UNI 215',u'UNI 216',u'UNI 315',u'UNI 316']
                for item in q:
                    self.all_courses[item]=self.all_courses[u'UNI 115']
     
                
            else:                    
                driver = webdriver.Firefox()
                driver.get(link)
                elem=driver.find_elements_by_class_name("hLink")

                for el_tomato in elem:
                    val=el_tomato.text
                    if val=="Course Descriptions":
                        menuid=el_tomato.get_attribute("menuid")
                driver.close()
                
                path="http://www.sehir.edu.tr/"
                c=urllib2.urlopen(link)
                deck=BeautifulSoup(c.read(),"html.parser")
                dil=str(1)
                for soup in deck.find_all("div","ak_all"):#this isn't actually a loop , it just works once, the reason for usage is ;
                    #without the for loop we could not get it to work due to the retun value of the function being an object
                    scripte=str(soup.script)
                    scripa= scripte.split("\n")
                    scripa=scripa[21].split("'")
                    layouts="_" + str(scripa[1].split("_")[1])
                    desclink=path+layouts+menuid+scripa[3]+dil
                    
                d=urllib2.urlopen(desclink)
                feela=BeautifulSoup(d.read(),"html.parser")
                for soup in feela.find_all("div"):
                    cour=soup.find_all("p")
                    for item in cour:
                        x=item.get_text()
                        x.split()
                if link[-2:]=='12':
                    count=0
                    coursenamen=[]
                    for soup in feela.find_all("strong"):
                        coursename=soup
                        for item in coursename:
                            if count%3==0:
                                coursenamen.append(item.string)
                            count+=1

                    coursecodes=[]

                    for item in coursenamen:
                        x=item.split()[:2]
                        coursecodes.append(" ".join(x))
                    for courses in coursecodes:
                        self.all_courses[courses]=[u'data',u'science',u'web',u'crawling',u'data',u'science',u'web',u'crawling',u'data',u'science',u'web',u'crawling',u'data',u'science',u'web',u'crawling',u'data',u'science',u'web',u'crawling']
                        
                if link[-2:]=='13':
                    coursenamen=[]
                    maxcharnumberEE=0
                    for soup in feela.find_all("strong"):
                        coursename=soup
                        for item in coursename:

                            try:
                                b=item.string.split("(")[0]
                                if len(b)<12:
                                    pass
                                else:
                                    if len(item.string) > maxcharnumberEE:
                                        maxcharnumberEE = len(item.string)
                                    coursenamen.append(b)
                            except:
                                pass
                    coursecodes=[]


                    for item in coursenamen:
                        x=item.split()[:2]
                        coursecodes.append(" ".join(x))


                    EEcoursedesc=[]
                    for soup in feela.find_all("div"):
                        coursedesc=soup
                        for item in coursedesc:

                            try:
                                if len(item.string)>maxcharnumberEE:
                                    xaxa = item.string.split()[0]
                                    if xaxa == "Textbook:":
                                        pass
                                    else:

                                        exo=item.string
                                        if exo.split(":")[0]=="http":
                                            pass
                                        else:
                                            if exo.split(",")[-1].isdigit():
                                                pass
                                            else:
                                                EEcoursedesc.append(item.string)
                            except:
                                pass


                    count=0
                    for coursecode in coursecodes:
                        coursedescaaa=EEcoursedesc[count].split()
                        for word in coursedescaaa:
                            self.all_courses[coursecode].append(word)
                        count+=1
                if link[-2:]=='14':
                    coursenamen=[]
                    maxcharnumberIE=0
                    for soup in feela.find_all("strong"):
                        coursename=soup
                        for item in coursename:
                            try:
                                if len(item.string)>6:
                                    if len(item.string)>maxcharnumberIE:
                                        maxcharnumberIE=len(item.string)
                                    coursenamen.append(item.string)
                            except:
                                pass
                    IEcoursedesc=[]
                    for soup in feela.find_all("div"):
                        coursedesc=soup
                        for item in coursedesc:
                            try:
                                if len(item.string)>maxcharnumberIE:
                                    xaxa=item.string.split()[0]
                                    if xaxa=="Textbook:":
                                        pass
                                    else:
                                        IEcoursedesc.append(item.string)
                            except:
                                pass
                    IEcoursedesc.pop(0)
                    coursenamen.pop(0)
                    courselist=[]
                    count=0
                    for item in coursenamen:
                        x=' '.join(item.split()[:2])
                        courselist.append(x)
                        count=+1
                    index=0
                    for item in courselist:
                        self.all_courses[item]=IEcoursedesc[index]
                        index=+1



    def readExcel(self):#reads excel file of user grades
        filename=tkFileDialog.askopenfilename()#browsing file
        self.wb=open_workbook(filename)#opening file
        self.sheet=self.wb.sheet_by_index(0)#opening sheet
        self.user_dep=' '.join(self.sheet.cell(1,0).value.split()[-2:])#determining the department of the user
        grade_loc=[6,18,29,40]#locations to be checked for grades, the start locations are always the same , the template is always same so no need for searching
        self.student_grades={}
        special=['P','U','S']#special grades to be ignored
        for rows in grade_loc:
            for row in range(rows,rows+7):
                if self.sheet.cell(row,6).value!='' and self.sheet.cell(14,9).value not in special:#if course is taken and the grade isnt  p ,u or s
                    self.student_grades[self.sheet.cell(row,0).value]=self.sheet.cell(row,6).value[0]
                if self.sheet.cell(row,15).value!='' and self.sheet.cell(14,9).value not in special:
                    self.student_grades[self.sheet.cell(row,9).value]=self.sheet.cell(row,15).value[0]
        if self.sheet.cell(14,15).value!='' and self.sheet.cell(14,9).value not in special:#exception for UNI100 , it is out of place
            self.student_grades[self.sheet.cell(14,9).value]=self.sheet.cell(14,15).value[0]
        
    def predict(self):#tries to predict the grades of courses if they were taken
        try:
            self.readUrl()
            self.courscore={}
            for courses in self.all_courses.keys():
                self.courscore.setdefault(courses,0)
            for course in self.student_grades.keys():
             if course==u'ENGR 100':#ENGR 100 not on page
                 pass
             else:
               try:
                for courses in self.all_courses.keys():
                    for words in self.all_courses[courses]:
                             for word in self.all_courses[course]:
                                if word==words:
                                    self.courscore[courses]=+1
               except:
                   pass

            self.listbox_grades.delete(0,END)
            for keys in self.courscore.keys():
                if self.courscore[keys]>0:
                    try:
                        self.listbox_grades.insert(END,keys+'-->'+self.student_grades[keys])
                    except:
                        pass
        except:
            tkMessageBox.showinfo('More Input Necessary','User Course Info Needed')
                
                    
                
                
if __name__=='__main__':#callings
    bob=Tk()
    master=GUI(bob)
