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


    def __init__(self,serviceCible,stockCible,s1,s2,s3):
        self.sc=serviceCible
        self.semaines=[s1,s2,s3]
        self.dechet=0#on aurait pu mettre comme une semaine suplémentaire...
        self.nbNonSatifait = 0
        self.stockCible = stockCible

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
        self.dechet=self.semaines[len(self.semaines)-1]
        for i in range (0, len(self.semaines) - 1):
            self.semaines[len(self.semaines)-i-1]=self.semaines[len(self.semaines)-i-2]
        
        #On initialise la nouvelle semaine
        self.semaines[0]=self.stockCible#TODO
    
    def printStock(self):
        print("mon stock total actuel est de \n")
        print(self.stockTotal())


monStock=Stock(1,2,0,0,0)
'''
print(monStock.semaines[0])
monStock.printStock()
monStock.nouvelleSemaine(2)
monStock.printStock()
print(monStock.semaines[0])
'''

mu, sigma = 10, 0.1 # mean and standard deviation

s = np.random.normal(mu, sigma, 10)
count, bins, ignored = plt.hist(s, 30, normed=True)

#plt.plot(bins, 1/(sigma * np.sqrt(2 * np.pi)) * np.exp( - (bins - mu)**2 / (2 * sigma**2) ),linewidth=2, color='r')

#plt.show()

#TODO
#generer un tableau de valeur suivant une loi normale : s = np.random.normal(mu, sigma, 100000)
#utiliser la fonction demande n fois

demandes = [0,0,0,0,3]
for i in demandes:
    monStock.nouvelleSemaine(i)
    monStock.printStock()




#faire varier l'approcisionnement pour voir le moment ou le service cible est atteint