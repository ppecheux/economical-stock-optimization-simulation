# coding: utf-8 

"""

On s’intéresse au stock de produits P1, le plus vendu.
On considère que la demande hebdomadaire de produits 
P1 peut être modélisée par une loi Normale N(155,38.9)

'''

'''question 11

il faut liquider apres 4 semaines

on a un niveau de service cible SC

on doit déterminer la proportion de produit à se débarasser chaque semaine
'''
"""
import numpy as np
import matplotlib.pyplot as plt

class Stock:
    '''représente l'état du stock sur les semaines'''


    def __init__(self,serviceCible,stockCible,ListeSemainesDeStock):
        self.sc=serviceCible
        self.semaines=ListeSemainesDeStock
        self.dechet=0#on aurait pu mettre comme une semaine suplémentaire...
        self.nbNonSatifait = 0
        self.stockCible = stockCible
        self.fournis= self.stockTotal()

    def stockTotal(self):
        somme=0
        for i in self.semaines:
            somme+=i
        return somme

    def nouvelleSemaine(self,demande):
        #On cherche à répondre à la demande
        #On considère que chaque client achete un produit
        temp=[]
        for i in self.semaines:
            
            if i>demande :
                i-=demande
                demande=0
            else:
                demande-=i
                i=0
            
            #pour voir le stock de la semaine i:
            #print(i)

            temp.append(i)

        if demande>0 :
            self.nbNonSatifait+=demande

        self.semaines=temp

        #ON décale les semaines
        self.dechet+=self.semaines[len(self.semaines)-1]
        for i in range (0, len(self.semaines) - 1):
            self.semaines[len(self.semaines)-i-1]=self.semaines[len(self.semaines)-i-2]
        
        #On initialise la nouvelle semaine
        self.semaines[0]=self.stockCible-self.stockTotal()#TODO #c'est bon
        self.fournis+=self.semaines[0]
    
    def printStock(self):
        print("\nmon stock total actuel est de ")
        print(self.stockTotal())

mu, sigma = 155, 60 # demande moyenne et equart type de la demande moyenne
nbSemPermention = 3
ListeSemainesDeStock = np.zeros(nbSemPermention)


def simulerSemainesStockCible(nbSemaines,stockCible):
    monStock=Stock(1,stockCible,ListeSemainesDeStock)
    demandes = np.random.normal(mu, sigma, nbSemaines)
    for i in demandes:
        monStock.nouvelleSemaine(i)

    
    serviceCibleReel =1- monStock.nbNonSatifait/np.sum(demandes)
    conclusions = serviceCibleReel
    return conclusions

def dechetsSemainesStockCible(nbSemaines,stockCible):
    monStock=Stock(1,stockCible,ListeSemainesDeStock)
    demandes = np.random.normal(mu, sigma, nbSemaines)
    for i in demandes:
        monStock.nouvelleSemaine(i)
    
    dechet =monStock.dechet/monStock.fournis
    return dechet#semble trop faible

def simulerTabStockCible(nbSemaines,tabStockCible):
    tabService = []
    for i in tabStockCible:
        tabService.append( simulerSemainesStockCible(nbSemaines,i))
    return(tabService)

def dechetTabStockCible(nbSemaines,tabStockCible):
    tabDechet = []
    for i in tabStockCible:
        tabDechet.append( dechetsSemainesStockCible(nbSemaines,i))
    return(tabDechet)

tabStockCible=np.arange(0,5000,1000)
tab =simulerTabStockCible(100000,tabStockCible)
dechets = dechetTabStockCible(100000,tabStockCible)

#plt.yscale("log")
plt.ylabel("Service Reel Simule")
plt.xlabel("Stock Cible")
plt.plot(tabStockCible,tab,'ro')


plt.plot(tabStockCible,dechets)
plt.show()
#print(dechetsSemainesStockCible(100,200))


#print(serviceCibleReel)
