# coding: utf-8 

"""

On s’intéresse au stock de produits P1, le plus vendu.
On considère que la demande hebdomadaire de produits 
P1 peut être modélisée par une loi Normale N(155,38.9)

stock de sécurité : SS= alpha*sigma
demande ~ N(155,60)
(demande-155)/(60/sqrt(n)) ~ N(0,1)
P(-U(1-a/2)<demande-155)/(60/sqrt(n))< U(1-a/2))=1-a

alpha = étant fixé
"""
import numpy as np
import matplotlib.pyplot as plt
#import GestionDeTab

class Stock:
    '''représente l'état du stock sur les semaines'''


    def __init__(self,serviceCible,stockCible,ListeSemainesDeStock):
        self.sc=float(serviceCible)#proportion de clients servis
        self.semaines=ListeSemainesDeStock#liste de stock
        self.dechet=0.0#on aurait pu mettre comme une semaine suplémentaire...
        self.nbNonSatifait = 0.0
        self.produitNonLivre=0
        self.stockCible = float(stockCible)
        self.fournis= float(self.stockTotal())

    def stockTotal(self):
        return np.sum(self.semaines)

    def nouvelleSemaine(self,demande):
        #On cherche à répondre à la demande
        #On considère qu'on doit livrer qu'un seul client
        
        self.semaines,demande = tabProduitMoinsDemande(self.semaines,demande)

        if demande>0 :
            self.nbNonSatifait+= 1.0
            self.produitNonLivre+=demande

        #ON décale les semaines
        self.dechet+=1.0*self.semaines[len(self.semaines)-1]
        decalCaseTab(self.semaines)
        
        #On initialise la nouvelle semaine
        self.semaines[0]=0.0
        self.semaines[0]=1.0*(self.stockCible-self.stockTotal())
        self.fournis+=self.semaines[0]
    
    def printStock(self):
        print("stockTotal=",self.stockTotal())
        print("etatDuStock=",self.semaines)
        print("stockFournis=",self.fournis)
        print("stockDechet=",self.dechet)
        print("PersonnesNOnsatisfaites=",self.nbNonSatifait)



nbSemPermenption = 3
ListeSemainesDeStock = np.zeros(nbSemPermenption)



def decalCaseTab(tab):
    #retoune le tableau avec les valeurs décallées mais avec la premiere case <- derniere nouvelle case
    for i in range (len(tab)):
        tab[len(tab)-1-i]=tab[len(tab)-2-i]
    return tab

def tabProduitMoinsDemande(tab,demande):
    for i in range (len(tab)-1):
        if tab[len(tab)-1-i]>demande:
            tab[len(tab)-1-i]-=demande
            demande=0
        else:
            demande-=tab[len(tab)-1-i]
            tab[len(tab)-1-i]=0

    return tab,demande

def testtabProduitMoinsDemande():
    tab,demande=np.arange(0,3,1),100
    tab,demande=tabProduitMoinsDemande(tab,demande)
    print(tab)
    print(demande)

#testtabProduitMoinsDemande()

def testChangementSemaine():
    stockCible = 3
    demande=0
    ListeSemainesDeStock = np.arange(0,3,1)
    monStock=Stock(1,stockCible,ListeSemainesDeStock)
    for i in np.zeros(10):
        monStock.printStock()
        monStock.nouvelleSemaine(demande)
        #monStock.printStock()

#testChangementSemaine()
def simulerSemainesStockCible(nbSemaines,stockCible,demandes):
    ListeSemainesDeStock[0]=stockCible
    monStock=Stock(1,stockCible,ListeSemainesDeStock)

    for i in demandes:
        monStock.nouvelleSemaine(i)

    serviceCibleReel = 1 - (float(monStock.nbNonSatifait)/float(nbSemaines))
   
    return serviceCibleReel

def dechetsSemainesStockCible(nbSemaines,stockCible,demandes):
    ListeSemainesDeStock[0]=stockCible
    monStock=Stock(1,stockCible,ListeSemainesDeStock)

    for i in demandes:
        monStock.nouvelleSemaine(i)
    
    tauxDechet=0.0
    try:
        tauxDechet = float(monStock.dechet)/monStock.fournis
    except:
        return 0.0

    print([tauxDechet,monStock.dechet,monStock.semaines[len(monStock.semaines)-1],monStock.fournis,monStock.stockTotal()])
    return tauxDechet#semble trop faible



def simulerTabStockCible(nbSemaines,tabStockCible,mesDemandes):
    tabService = []
    for i in tabStockCible:
        tabService.append( simulerSemainesStockCible(nbSemaines,i,mesDemandes))
    return(tabService)

def dechetTabStockCible(nbSemaines,tabStockCible,mesDemandes):
    tabDechet = []
    for i in tabStockCible:
        tabDechet.append( dechetsSemainesStockCible(nbSemaines,i,mesDemandes))
    return(tabDechet)


def simulationPousse():

    tabStockCible=np.arange(1,500,10)
    mu, sigma = 155, 60 # demande moyenne et equart type de la demande moyenne

    nbsemaine=1000
    mesDemandes = np.random.normal(mu, sigma, nbsemaine)

    tabServiceSimule =simulerTabStockCible(nbsemaine,tabStockCible,mesDemandes)
    dechets = dechetTabStockCible(nbsemaine,tabStockCible,mesDemandes)

    plt.ylabel("Service Reel Simule")
    plt.xlabel("Stock Cible")
    plt.plot(tabStockCible,tabServiceSimule,'ro')
    plt.plot(tabStockCible,dechets)
    print(tabServiceSimule)
    print(dechets)
    plt.show()

simulationPousse()

def simulationFacile():
    tabStockCible=np.arange(0,20,0.1)

    nbsemaine=10
    mesDemandes = np.arange(0,10,1)

    tabServiceSimule =simulerTabStockCible(nbsemaine,tabStockCible,mesDemandes)
    dechets = dechetTabStockCible(nbsemaine,tabStockCible,mesDemandes)

    plt.ylabel("Service Reel Simule")
    plt.xlabel("Stock Cible")
    plt.plot(tabStockCible,tabServiceSimule,'ro')
    plt.plot(tabStockCible,dechets)
    print(tabServiceSimule)
    print(dechets)
    plt.show()

#simulationFacile()

#print(dechetsSemainesStockCible(100,200))


#print(serviceCibleReel)
