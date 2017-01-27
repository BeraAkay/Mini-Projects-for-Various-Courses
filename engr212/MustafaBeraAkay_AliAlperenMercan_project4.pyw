from bs4 import BeautifulSoup
import os
from Tkinter import *
import tkMessageBox
from ttk import Combobox
import urllib2
import urllib
from PIL import Image, ImageTk



class GUI(Frame):
    def __init__(self,master):
        self.master=master
        self.master.config(background='darkblue')
        self.defineWidgets()
        self.placeWidgets()
        self.buyProduct()
        self.alltogether=[]

        self.master.mainloop()

    def buyProduct(self):#a little joke
        tkMessageBox.showinfo('Trial Activated','You have activated your 30 Days Trial , You can buy this product at Alperen&BeraCo.com')

    def titleCreate(self):#function that creates the title frame
        self.title_frame=Frame(self.master)
        self.title_frame.config(background='darkblue')
        self.title=Label(self.title_frame,text='SEHIR Research Projects Analyzer',font='Arial 17',background='darkblue',foreground='White')

    def topFrameCreate(self):#function that creates the top frame (url bar and fetch button)
        self.top_frame=Frame(self.master,background='darkblue')
        self.label_url=Label(self.top_frame,text='Please provide a URL:',background='darkblue',foreground='White',font='Arial 12')
        self.bar_url=Entry(self.top_frame,width=100)
        self.bar_url.insert(END,"http://cs.sehir.edu.tr/en/research/")
        self.button_fetch=Button(self.top_frame,text='Fetch Research Projects',command=self.fetch_and_fill,background='darkblue',foreground='White',font='Arial 12')
        

    def midFrameCreate(self):#function that creates the middle frame (comboboxes , listbox , and title and description buttons)
        self.mid_frame=Frame(self.master,background='darkblue')
        self.filters_label=Label(self.mid_frame,text='Filter Research Projects By:',font='Arial 12',background='darkblue',foreground='White')
        self.label_year=Label(self.mid_frame,text='Year:',background='darkblue',foreground='White',font='Arial 12')
        self.label_prof=Label(self.mid_frame,text='Principal Investigator:',background='darkblue',foreground='White',font='Arial 12')
        self.label_fund=Label(self.mid_frame,text='Funding Institution:',background='darkblue',foreground='White',font='Arial 12')
        self.combo_year=Combobox(self.mid_frame, state="readonly",width=50)
        self.combo_prof=Combobox(self.mid_frame, state="readonly",width=50)
        self.combo_fund=Combobox(self.mid_frame, state="readonly",width=50)
        self.label_listbox=Label(self.mid_frame,text='Pick A Project',font='Arial 12',background='darkblue',foreground='White')
        self.scroll_box=Scrollbar(self.mid_frame)
        self.list_proj=Listbox(self.mid_frame,yscrollcommand=self.scroll_box.set,width=70)
        self.scroll_box.config(command=self.list_proj.yview)
        self.button_display=Button(self.mid_frame,text='Display Project Titles',command=self.listbox_update,font='Arial 12',background='darkblue',foreground='White')
        self.button_description=Button(self.mid_frame,text='Show Description',command=self.canvas_update,font='Arial 12',background='darkblue',foreground='White')
        
        
    def botFrameCreate(self):#function that creates the bottom frame (canvas and text)
        self.bot_frame=Frame(self.master,background='darkblue')
        self.canvas_img=Canvas(self.bot_frame,bg='White',width=470,height=175)
        self.label_desc=Label(self.bot_frame,text='Project Description:',font='Arial 12',foreground='White',background='darkblue')
        self.scroll_desc=Scrollbar(self.bot_frame)
        self.text_desc=Text(self.bot_frame,width=55,height=11,yscrollcommand=self.scroll_desc.set,state=DISABLED)
        self.scroll_desc.config(command=self.text_desc.yview)

    def titlePlace(self):#places widgets in frame
        self.title_frame.grid(row=0,pady=15)
        self.title.grid()

    def topPlace(self):#places widgets in frame
        self.top_frame.grid(row=1,pady=15)
        self.label_url.grid(row=0,column=0)
        self.bar_url.grid(row=1,column=0,padx=15)
        self.button_fetch.grid(row=0,column=1,rowspan=2,columnspan=2,padx=(0,15),s=N+S)
    
    def midPlace(self):#places widgets in frame
        self.mid_frame.grid(row=2,pady=15)
        self.filters_label.grid(row=0,column=0,columnspan=2)
        self.label_year.grid(row=1,column=0,sticky=W,padx=(15,0))
        self.label_prof.grid(row=2,column=0,sticky=W,padx=(15,0))
        self.label_fund.grid(row=3,column=0,sticky=W,padx=(15,0))
        self.combo_year.grid(row=1,column=1,padx=15)
        self.combo_prof.grid(row=2,column=1,padx=15)
        self.combo_fund.grid(row=3,column=1,padx=15)
        self.label_listbox.grid(row=0,column=2)
        self.scroll_box.grid(row=1,column=3,rowspan=3,sticky=N+S,padx=(0,15))
        self.list_proj.grid(row=1,column=2,rowspan=3)
        self.button_display.grid(row=4,column=0,columnspan=2,pady=15)
        self.button_description.grid(row=4,column=2,columnspan=4,pady=15)
        
    
    def botPlace(self):#places widgets in frame
        self.bot_frame.grid(row=3,pady=(0,15))
        self.canvas_img.grid(row=1,column=0,columnspan=2,padx=(0,15))
        self.label_desc.grid(row=0,column=3)
        self.scroll_desc.grid(row=1,column=4,s=N+S)
        self.text_desc.grid(row=1,column=3)

    def defineWidgets(self):#all widget definiings called
        self.titleCreate()
        self.topFrameCreate()
        self.midFrameCreate()
        self.botFrameCreate()

    def placeWidgets(self):#all widgets placed
        self.titlePlace()
        self.topPlace()
        self.midPlace()
        self.botPlace()
        
    def clear(self):#clear function for development purposes
        self.title_frame.destroy()
        self.top_frame.destroy()
        self.mid_frame.destroy()
        self.bot_frame.destroy()
        self.defineWidgets()
        self.placeWidgets()

    def fetch_and_fill(self):#the data on the web page is read and saved to a list
        c=urllib2.urlopen(self.bar_url.get())#url is read from the url bar and opened using the urlopen and taken as a variable
        contents=c.read()#the page is read in html
        chicken_soup=BeautifulSoup(contents,"html.parser")#using beautifulsoup we parsed the html so we can navigate

        path="http://cs.sehir.edu.tr"#added this to eliminate problems during fetching the project image, could not take the whole url for the image link

        for soup in chicken_soup.find_all('li','list-group-item'):#for loop to fetch the names,instructors , funding inst. etc of all projects
            #list group item and li tag is used at framing of a project in the code

            projectname=soup.a['id']#name of the project with variable id in html
            fundingname=soup.find_all('p')[1].get_text().split(':')[1]#funding inst. 1st item is fund
            instructor=soup.find_all('p')[2].get_text().split(':')[1]#2. index with p tag in the project is the instructor 
            year1=soup.p.string.split()[2]#starting year
            year2=soup.p.string.split()[6]#ending year
            imgurl=path+soup.img['src']#the link for the image using the image tag, url is saved as src in the page
            projectdesc=soup.find_all('p')[4].get_text()#4th index in with te p tag on the project is the description

            tempy=" "#this part is used to trim the instructor and funding inst. names of the unnecessary spaces
            instructor=instructor.split()
            instructor=tempy.join(instructor)
            fundingname=fundingname.split()
            fundingname=tempy.join(fundingname)



            tup=(projectname,fundingname,instructor,year1,year2,imgurl,projectdesc)# all the read project info are added as a tuple to our list of projects
            self.alltogether.append(tup)



        temp_years=[]
        temp_investigator=[]
        temp_institution=[]
        for i in self.alltogether:#all the project info are put into lists to add them to the combobox
            temp_institution.append(i[1])
            temp_investigator.append(i[2])
            temp_years.append(i[3])
            temp_years.append(i[4])

        #years
        years=[]
        for i in temp_years:
            if i not in years:
                years.append(i)
            else:
                pass
        years.sort()
        years.insert(0,"All Years")
        self.combo_year["values"]=years
        self.combo_year.current(0)


        #investigator
        investigator=[]
        for i in temp_investigator:
            if i not in investigator:
                investigator.append(i)
            else:
                pass
        investigator.insert(0,"All Investigators")
        self.combo_prof["values"]=investigator
        self.combo_prof.current(0)

        #funding institution
        institution=[]
        for i in temp_institution:
            if i not in institution:
                institution.append(i)
            else:
                pass
        institution.insert(0,"All Institutions")
        self.combo_fund["values"]=institution
        self.combo_fund.current(0)

    def listbox_update(self):#function filters the data from the web page according to year , instructor and funding inst. and puts the project titles into the listbox
        self.list_proj.delete(0,END)#the listbox is cleared
        x=self.combo_year.get()#the selected year in the respective combobox
        y=self.combo_prof.get()#the selected instructor in the respective combobox
        z=self.combo_fund.get()#the selected funding inst. in the respective combobox
        if x=='' or y=='' or z=='':#if the comboboxes are empty a.k.a no projects fetched , user is told to fetch the data
            tkMessageBox.showinfo('NOPE','Fetch the data first')
            return
        selection_list=[]
        selection_list2=[]
        selection_list3=[]

        if x=="All Years" and y=="All Investigators" and z=="All Institutions":#if all the criteria are all for every category ,
            for projname in self.alltogether:#then all the names from the project list are put into the listbox
                self.list_proj.insert(END,projname[0])#insertion to listbox
        elif x!="All Years":#if years are selected ,
            for i in self.alltogether:#the year given is searched through all the project time periods and the projects are put into the list
                start_year=i[3]
                end_year=i[4]
                if x>=start_year and x<=end_year:
                    selection_list.append(i)
                else:
                    pass

            if y!="All Investigators":#after checking years, if the instructor is selected , the projects are filtered to fit the instructor
                for i in selection_list:
                    investigator=i[2]
                    if y==investigator:
                        selection_list2.append(i)
                    else:
                        pass

                if z!="All Institutions":#after checking instructor, filtering for institutions are applied if institution selected
                    for i in selection_list2:
                        institution = i[1]
                        if z==institution:
                            selection_list3.append(i)
                        else:
                            pass
                    for proname in selection_list3:#insertion to listbox
                        self.list_proj.insert(END,proname[0])
                else:#if no inst. selected , the last filtered data is put to the listbox
                    selection_list3=selection_list2
                    for proname in selection_list3:#insertion to listbox
                        self.list_proj.insert(END, proname[0])
            else:#if no instructor selected,the last filtered data is filtered again if institution selected , otherwise , its put into the listbox
                selection_list2=selection_list
                if z != "All Institutions":
                    for i in selection_list2:
                        institution = i[1]
                        if z == institution:
                            selection_list3.append(i)
                        else:
                            pass
                    for proname in selection_list3:
                        self.list_proj.insert(END, proname[0])#insertion to listbox
                else:
                    selection_list3 = selection_list2
                    for proname in selection_list3:
                        self.list_proj.insert(END, proname[0])#insertion to listbox

        else:#if year is not selected , the others are checked for filtering
            selection_list=self.alltogether
            if y != "All Investigators":#if instructor selected , the data up to now is filtered for that instructor if one is selected
                for i in selection_list:
                    investigator = i[2]
                    if y == investigator:
                        selection_list2.append(i)
                    else:
                        pass

                if z != "All Institutions":#after checking instructor , the data up to now is filtered for that institution if one is selected
                    for i in selection_list2:
                        institution = i[1]
                        if z == institution:
                            selection_list3.append(i)
                        else:
                            pass
                    for proname in selection_list3:
                        self.list_proj.insert(END, proname[0])
                else:# if no inst. selected , the last filtered data is inserted to listbox
                    selection_list3 = selection_list2
                    for proname in selection_list3:
                        self.list_proj.insert(END, proname[0])#insertion to listbox
            else:#if instructor is not selected , the data up to now is checked for institution selection
                selection_list2 = selection_list
                if z != "All Institutions":#if inst. selected ,the data is filtered accordingly, then inserted to listbox
                    for i in selection_list2:
                        institution = i[1]
                        if z == institution:
                            selection_list3.append(i)
                        else:
                            pass
                    for proname in selection_list3:
                        self.list_proj.insert(END, proname[0])#insertion to listbox
                else:#if no inst. selected, the data up to now is put into the listbox
                    selection_list3 = selection_list2
                    for proname in selection_list3:
                        self.list_proj.insert(END, proname[0])#insertion to listbox

    def canvas_update(self):#function puts images to the canvas and calls the description function for text 
        self.list_selected = self.list_proj.get(ACTIVE)# getting the name of the selected project from the listbox
        for link in self.alltogether:#checking for all projects if the name matches the selected name from listbox
            if link[0]==self.list_selected:#if matches , the project link we created above
                urllib.urlretrieve(link[5],"image12345678a")# is used to retrieve the image using urllib
                image=Image.open("image12345678a")#the image we saved using urllib is opened with PIL



                width=450
                height=160

                image=image.resize((width,height), Image.BILINEAR)#resized the image using PIL to fit the canvas



                photo=ImageTk.PhotoImage(image)#saving the image as an object to use with tkinter
                self.canvas_img.create_image(10,10,image=photo,anchor="nw")#put the image to canvas
                self.canvas_img.image=photo#the reference is created so if tkinter screws up the image wont go transparent/disappear
            else:
                pass

        self.desc_update()

    def desc_update(self):#function puts description in text widget
        self.text_desc.config(state=NORMAL)
        self.text_desc.delete('1.0', END)#previous info cleared 
        for item in self.alltogether:
            if item[0]==self.list_selected:#finding the selected project to get description
                self.text_desc.insert(END,item[6])#description put in text widget
            else:
                pass
        try:#if it cannot delete the image it means that the image is not retrieved hence we know that user needs to get the project titles
            os.remove("image12345678a")#deletes the image after putting it on canvas
        except:
            tkMessageBox.showinfo('NOPE','Get the projects first')
        self.text_desc.config(state=DISABLED)

if __name__=='__main__':#callings
    bob=Tk()
    master=GUI(bob)
