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
    nbInvendus

    def __init__(self,serviceCible,s1,s2,s3):
        self.sc=serviceCible
        self.s1=s1
        self.s2=s2
        self.s3=s3

    def stockTotal(self):
        somme=self.s1+self.s2+self.s3
        return somme

    def nouvelleSemaine(self,demande):
        #On cherche à répondre à la demande

        #ON décale les semaines

        #On initialise la nouvelle semaine

    
    def printStock(self):
        print("mon stock total actuel est de \n")
        print(self.stockTotal())

monStock=Stock(2,3,4)
print("hey")
print(monStock.s1)
monStock.printStock()
