import thinkstats2 as ts
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm,t
from scipy import optimize as op
class Hyptest:
    def __init__(self):
        kek=open('data.csv','r+')
        student_info=[]
        for i in kek:
            student_info.append(i.strip())

        student_info=student_info[1:]
        stuinfo=[]
        for info in student_info:
            stu=info.split(',')
            stuinfo.append(stu)

        self.sex=[]
        self.age=[]
        self.time=[]
        self.gpa=[]
        self.gender=[]

        for inf in stuinfo:
            if inf[0]=='M':
                self.sex.append(0)
            else:
                self.sex.append(1)
            self.gender.append(inf[0])
            self.age.append(int(inf[1]))
            self.time.append(int(inf[2]))
            self.gpa.append(float(inf[3]))
        print 'CATEGORY','-','MEAN','-','STD.DEVIATION'
        self.meansex=np.mean(self.sex)
        self.devsex=np.std(self.sex)
        print 'SEX','-',self.meansex,'-',self.devsex
        self.meanage=np.mean(self.age)
        self.devage=np.std(self.age)
        print 'AGE','-',self.meanage,'-',self.devage
        self.meantime=np.mean(self.time)
        self.devtime=np.std(self.time)
        print 'TIME','-',self.meantime,'-',self.devtime
        self.meangpa=np.mean(self.gpa)
        self.devgpa=np.std(self.gpa)
        print 'GPA','-',self.meangpa,'-',self.devgpa

    def P1Q1(self):
        print 'Part I Question 1'
        a=0.05
        H0='Time spent on Facebook has no effect on GPA'
        H1='Time spent on Facebook has an effect on GPA'

        corrcoef=np.corrcoef(self.time,self.gpa)
        tval=(corrcoef*np.sqrt(len(self.gpa)-2))/np.sqrt(1-(corrcoef**2))#deg of freedom=n-2
        tdist=t.sf(np.abs(tval),len(self.gpa)-2)#for some reason , values come out as 2 nested lists in a list instead of just one value
        
        pval=0
        for items in tdist:#so i just summed them up
            for item in items:
                pval=pval+item
        print 'P-Value',pval
        if pval>=a:
            print H0

        elif pval<a:
            print 'Null Hypothesis Rejected'
            print H1

    def P1Q2(self):#same as first question , just the variables changed
        print 'Part I Question 2'
        a=0.05
        H0='Age has no effect on time spent on Facebook'
        H1='Age has an effect on time spent on Facebook'

        corrcoef=np.corrcoef(self.age,self.time)
        tval=(corrcoef*np.sqrt(len(self.age)-2))/np.sqrt(1-(corrcoef**2))#def of freedom=n-2
        tdist=t.sf(np.abs(tval),len(self.gpa)-2)
        pval=0
        for items in tdist:
            for item in items:
                pval=pval+item
        print 'P-Value',pval
        if pval>=a:
            print H0

        elif pval<a:
            print 'Null Hypothesis Rejected'
            print H1
         
        

    def P1Q3(self):
        print 'Part I Question 3'
        a=0.05
        H0='Gender has no effect on time spent on Facebook'
        #H0 assumes males are the norm
        H1='Gender as an effect on time spent on Facebook, Females use it More'
        sextime=[]
        for index in range(0,119):
            sextime.append((self.sex[index],self.time[index]))
        mantime=[]
        womantime=[]
        for item in sextime:
            if item[0]==0:
                mantime.append(item[1])
            else:
                womantime.append(item[1])

        est_std_samp=np.std(womantime)/np.sqrt(len(womantime))#estimate std. dev. using std dev of our female sample
        zval=(np.mean(womantime)-np.mean(mantime))/est_std_samp
        pval=norm.sf(abs(zval))*2
        
        print 'P-Value',pval

        if pval>=a:
            print H0

        elif pval<a:
            print 'Null Hypothesis Rejected'
            print H1


    def P2(self):
        print 'Part II is plotted'
        plt.scatter(self.time,self.gpa)

        par=np.polyfit(self.time,self.gpa,1,full=True)

        slope=par[0][0]
        intercept=par[0][1]
        x=[min(self.time), max(self.time)]
        y=[slope*xs+intercept for xs in x]

        plt.xlabel('Time Spent on Facebook')
        plt.ylabel('GPA')

        plt.plot(x,y,'-r')
        plt.show()
        

        variance=np.var(yd)
        res=[slope*xs+intercept-ys for xs,ys in zip(self.time,self.gpa)]
        residual=np.var(res)
        
        plt.scatter(self.time,res)
        plt.xlabel('Time Spent on Facebook')
        plt.ylabel('Residuals')
        plt.show()


    def plot(self):#all the data is sorted and plotted for visualization
        student_index=[index for index in range(0,len(self.gpa))]
        plt.plot(student_index,sorted(self.time),'-r')
        plt.ylabel('Time Spent on Facebook')
        plt.show()
        plt.scatter(student_index,self.sex)
        plt.ylabel('Gender ; M=0 F=1')
        plt.show()
        plt.plot(student_index,sorted(self.gpa),'-r')
        plt.ylabel('GPA')
        plt.show()
        plt.plot(student_index,sorted(self.age),'-r')
        plt.ylabel('Age')
        plt.show()
        
bob=Hyptest()
bob.plot()
bob.P1Q1()
bob.P1Q2()
bob.P1Q3()
bob.P2()


