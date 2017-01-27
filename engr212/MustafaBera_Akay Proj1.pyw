from xlrd import open_workbook
from ttk import Combobox
from Tkinter import *
import os
import tkFileDialog
import tkMessageBox
import anydbm
import pickle

class Excel:
    def __init__(self):
        #the attributes for excel browsing are defined here also the db file is created
        self.height=10
        self.length=7
        self.sem_list=[]
        self.sems_cells=anydbm.open('curriculum.db','c')
        self.cells=[]        
    def listsem(self,filename):         #the function puts the semester names with their coordinates in a list read from the selected excel file
        self.wb=open_workbook(str(filename))
        self.sheet=self.wb.sheet_by_index(0)
        for row in range(self.sheet.nrows):
            for col in range(self.sheet.ncols):
                try:
                    if self.sheet.cell(row,col).value[0:10]=='Semester I' or self.sheet.cell(row,col).value[0:10]=='Semester V' :
                        self.sem_list.append([str(self.sheet.cell(row,col).value),row,col])
                except (TypeError):
                    pass
                else:
                    pass
        return self.sem_list
    def backup(self,filename):          #the function backs the whole excel file up in the database by the cells of the semesters in pickled lists
        self.listsem(filename)
        self.sems_cells['name']=str(filename)
        for sems in range(len(self.sem_list)):
            cells=[]
            for row in range(self.height):
                for col in range(self.length):
                    if str(self.sheet.cell(self.sem_list[sems][1]+row,self.sem_list[sems][2]+col).value)[:13]=='Abbreviations':
                        cells.append('')
                    else:
                        cells.append(str(self.sheet.cell(self.sem_list[sems][1]+row,self.sem_list[sems][2]+col).value))          
            self.sems_cells[str(sems)]=pickle.dumps(cells)
        self.sems_cells.close()
        self.sems_cells=anydbm.open('previously_on_curriculum_viewer.db','c')
    def opfile_list_semesters(self,filename,chosensemester):            #the function puts the cells in the selected semester in a list, tells to select semester if its not selected
        self.listsem(filename)
        try:
            cells=[]
            for row in range(self.height):
                for col in range(self.length):
                        cells.append(str(self.sheet.cell(self.sem_list[chosensemester][1]+row,self.sem_list[chosensemester][2]+col).value))          
            return cells    
        except(TypeError):
            self.mr_destroy()
            tkMessageBox.showinfo('Insufficient Input', 'You must select a semester')
            self.celllabel=Label(self._cellframe,text='You must select a semester')
            self.celllabel.grid()
            
    def mr_destroy(self): #the function clears and recreates the frame in which the cells are listed
     try:
        self._cellframe.destroy()
        self._cellframe=Frame(self)
        self._cellframe.grid(columnspan=2)
     except:
         pass

class GUI(Frame,Excel):
    def __init__(self,root):    # attributes for listing are created and Excel class is inherited
        self.rowbreak=0
        self.semdrop=['Semester I','Semester II','Semester III','Semester IV','Semester V','Semester VI','Semester VII','Semester VIII']
        Excel.__init__(self)
        Frame.__init__(self)
        self.root=root
        self.initUI()
        
    def filebrowser(self):  #the function takes the name of the selected file from the browser and calls the backup function to back the file up, also calls the function to display file adress 
        self.browsedfile=tkFileDialog.askopenfilename()
        self.backup(self.browsedfile)
        self.title_frame()
        return self.browsedfile
    def fileopener(self,sem=0): #the function puts the outputs of the semester choosing function and file browsing function in the semester listing function 
        try:
            sem=self.chosen_sem()
        except:
            pass
        try:
            return pickle.loads(self.sems_cells[str(sem)])                    
        except:
            if self.semselect.get() not in self.semdrop:    #tells to select semester or file if its not selected
                self.mr_destroy()
                tkMessageBox.showinfo('Insufficient Input', 'You must select a semester')
                self.celllabel=Label(self._cellframe,text='You must select a semester')
                self.celllabel.grid()
            else:
                self.mr_destroy()
                tkMessageBox.showinfo('Insufficient Input', 'You must select a file')
                self.celllabel=Label(self._cellframe,text='You must select a file')
                self.celllabel.grid()            
        return self.opfile_list_semesters(self.browsedfile,self.chosen_sem())
        

    def chosen_sem(self): #treturns the output of the semester selecting widget ,  tells to select semester if its not selected
        a=self.semselect.get()
        for sem in range(len(self.semdrop)):
            if a==self.semdrop[sem]:
                try:
                    return sem
                except (UnboundLocalError):
                    self.mr_destroy()
                    tkMessageBox.showinfo('Insufficient Input', 'You must select a semester')
                    self.celllabel=Label(self._cellframe,text='You must select a semester')
                    self.celllabel.grid()
    def list_cells(self): #lists the cells of the semester on screen, tells to select semester if its not selected
        cells=self.fileopener()
        self.mr_destroy()
        try:
            for cellindex in range(len(cells)):
                self.celllabel=Label(self._cellframe,text=cells[cellindex])
                self.celllabel.grid(row=self.rowbreak,column=cellindex%7)
                if (cellindex+1)%7==0:
                    self.rowbreak+=1
            self.rowbreak=0
        except:
            tkMessageBox.showinfo('Insufficient Input', 'You must select a semester')
            self.celllabel=Label(self._cellframe,text='You must select a semester')
            self.celllabel.grid()
    def title_frame(self): # creates and changes the title if the file is changed
        try:
            self.titleframe.destroy()
        except:
            pass
        self.titleframe=Frame(self,background='Blue')
        self.titleframe.grid(row=0,column=0,stick=W + E)
        self.titlelabel=Label(self.titleframe,text='CURRICULUM VIEWER',background='Blue',foreground='White')
        self.titlelabel.grid(row=0,stick=W + E)
        try:
            self.filelabel=Label(self.titleframe,text=self.browsedfile,background='Blue',foreground='White')
        except:
            try:
                self.filelabel=Label(self.titleframe,text=self.sems_cells['name'],background='Blue',foreground='White')
            except:
                self.filelabel=Label(self.titleframe,text='No file selected,no previous data found',background='Blue',foreground='White')
        self.filelabel.grid(row=1,stick=W + E)
        self.filelabel.grid(row=1,stick=W + E)
    def initUI(self): # the main widgets are defined here
        self.grid()
        self.title_frame()
        self.userframe=Frame(self,background='Blue')                    
        self.userframe.grid(row=0,column=1,stick=E+W+N+S)
        self._cellframe=Frame(self)
        self.but=Button(self.userframe,text='Browse',command=self.filebrowser)
        self.semselect=Combobox(self.userframe,values=self.semdrop)
        self.semselect.grid(row=0,column=0,stick=S+E)
        self.but.grid(row=0,column=1,stick=S+E)
        self.but2=Button(self.userframe,text='Display',command=self.list_cells)
        self.but2.grid(row=0,column=2,stick=S+E)
        self._cellframe.grid(columnspan=2)

#the final calls are made here
bob=Tk()
master=GUI(bob)
master.mainloop()


