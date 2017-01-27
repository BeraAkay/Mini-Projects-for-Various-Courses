
import numpy as np
import matplotlib.pyplot as plt
import math
import random
import pylab


class PARTI:
    def __init__(self):
        self.text=open('babyboom.dat','r')
        self.entries=[]
        for line in self.text:
            self.entries.append(line.strip().split())
        self.time=[]
        self.gender=[]
        self.weight=[]
        self.minpassed=[]
        self.count=0
        self.countlist=[]
        for baby in self.entries:
            self.time.append(float(baby[0]))
            self.gender.append(float(baby[1]))
            self.weight.append(float(baby[2])/1000)
            self.minpassed.append(float(baby[3]))
            self.countlist.append(self.count)
            self.count+=1
        self.babyindex=[number for number in range(1,45)]

    def CDF(self,data,dataname):
        total=sum(data)
        prob=[]
        for item in data:
            prob.append(item/float(total))
        CDF=[]
        cdf=0
        for item in prob:
            cdf+=item
            CDF.append(cdf)
        plt.plot(CDF)
        plt.title('Normal Distribution')
        plt.xlabel('Baby Index')
        plt.ylabel(dataname)
        plt.show()
        return CDF
        
    def exponential(self,data,_lambda,dataname):
        CDF=[]
        data.sort()
        for item in data:
            if item==0:
                CDF.append(0)
            else:
                CDF.append(math.exp(-_lambda*item))
        plt.plot(self.babyindex,CDF)
        plt.title('Exponential Distribution')
        plt.xlabel('Baby Index')
        plt.ylabel(dataname)
        plt.show()
        return CDF
    
    def randomCDF(self):
        randy=random.randint(1,200)/100.0
        CDF=np.random.exponential(randy,40)
        CDF.sort()
        plt.plot(CDF)
        plt.title('Random')
        plt.show()
        return CDF

    def scatterplot(self,data,dataname):
        plt.scatter(self.babyindex,data)
        plt.title('Scatter')
        plt.xlabel('Baby Index')
        plt.ylabel(dataname)
        plt.show()

    def CCDF(self,data,_lambda):
        CCDF=[]
        CDF=bob.exponential(data,_lambda)
        for item in CDF:
            CCDF.append(1-item)
        return CCDF
    
    def C_CDF(self,func,functype,dataname):
        if functype=='CDF':
            CCDF=[]
            CDF=func
            for item in func:
                CCDF.append(1-item)
        elif functype=='CCDF':
            CDF=[]
            CCDF=func
            for item in func:
                CDF.append(item+1)
        else:
            raise 'Function not recognized'
        plt.plot(CDF,'-rs')
        plt.plot(CCDF,'-bs')
        plt.title('CDF=RED - CCDF=BLUE')
        plt.xlabel('Baby Index')
        plt.ylabel(dataname)
        plt.show()
        
        

bob=PARTI()
bob.scatterplot(bob.weight,'Weights')
bob.scatterplot(bob.gender,'Gender')
bob.scatterplot(bob.minpassed,'Minutes After Midnight')
bob.CDF(bob.weight,'Weights')
bob.CDF(bob.gender,'Gender')
bob.CDF(bob.minpassed,'Minutes After Midnight')
bob.exponential(bob.weight,1,'Weights')
bob.exponential(bob.gender,1,'Gender')
bob.exponential(bob.minpassed,1,'Minutes After Midnight')
bob.randomCDF()
bob.C_CDF(bob.exponential(bob.weight,1,'Weights'),'CDF','Weights')
bob.C_CDF(bob.exponential(bob.gender,1,'Gender'),'CDF','Gender')
bob.C_CDF(bob.exponential(bob.minpassed,1,'Minutes After Midnight'),'CDF','Minutes After Midnight')

