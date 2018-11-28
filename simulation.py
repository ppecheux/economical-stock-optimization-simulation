# coding: utf-8 on top of the file.

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

class Stock:
    '''représente l'état du stock sur les semaines'''


    def __init__(self,serviceCible,s1,s2,s3):
        self.sc=serviceCible
        self.semaines=[s1,s2,s3]
        self.nbNonSatifait = 0

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
            print(i)
            temp.append(i)

        if demande>0 :
            self.nbNonSatifait+=demande

        self.semaines=temp

        #ON décale les semaines
        for i in range (0, len(self.semaines) - 1):
            self.semaines[len(self.semaines)-i-1]=self.semaines[len(self.semaines)-i-2]
        
        #On initialise la nouvelle semaine
        self.semaines[0]=0#TODO
    
    def printStock(self):
        print("mon stock total actuel est de \n")
        print(self.stockTotal())

monStock=Stock(1,1,1,1)
print("hey")
print(monStock.semaines[0])
monStock.printStock()
monStock.nouvelleSemaine(2)
monStock.printStock()
print(monStock.semaines[0])