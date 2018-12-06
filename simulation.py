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
        self.produitNonLivre=0.0
        self.stockCible = float(stockCible)
        self.fournis= stockCible
        self.age=0
    
    def profit(self):
        return (self.fournis-self.dechet)*100-self.fournis*97

    def stockTotal(self):
        return np.sum(self.semaines)

    def nouvelleSemaine(self,demande):
        #On cherche à répondre à la demande
        #On considère qu'on doit livrer qu'un seul client
        self.age+=1
        
        self.semaines,demande = tabProduitMoinsDemande(self.semaines,demande)

        if np.floor(demande)>0.1 :
            self.nbNonSatifait+= 1.0
            self.produitNonLivre+=demande

        #ON décale les semaines
        self.dechet+=self.semaines[len(self.semaines)-1]
        decalCaseTab(self.semaines)
        
        #On initialise la nouvelle semaine
        self.semaines[0]=0.0
        self.semaines[0]=1.0*(self.stockCible-self.stockTotal())
        self.fournis+=self.semaines[0]
    
    def printStock(self):
        print("age=",self.age)
        print("stockTotal=",self.stockTotal())
        print("etatDuStock=",self.semaines)
        print("stockFournis=",self.fournis)
        print("stockDechet=",self.dechet)
        print("tauxDechet=",self.tauxDechet())
        print("PersonnesNOnsatisfaites=",self.nbNonSatifait)

    def tauxDechet(self):
        if self.fournis>1.0 :
            return (self.dechet/float(self.fournis))
        return 0.0



nbSemPermenption = 3
ListeSemainesDeStock = np.zeros(nbSemPermenption)



def decalCaseTab(tab):
    #retoune le tableau avec les valeurs décallées mais avec la premiere case <- derniere nouvelle case
    for i in range (len(tab)):
        tab[len(tab)-1-i]=tab[len(tab)-2-i]
    return tab

def tabProduitMoinsDemande(tab,demande):
    for i in range (len(tab)):
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
        #monStock.printStock()

    #print([tauxDechet,monStock.dechet,monStock.semaines[len(monStock.semaines)-1],monStock.fournis,monStock.stockTotal()])
    return monStock.tauxDechet()#semble trop faible


def simulerTabStockCible(nbSemaines,tabStockCible,mesDemandes):
    tabService = []
    for i in tabStockCible:
        tabService.append( simulerSemainesStockCible(nbSemaines,i,mesDemandes))
    return(tabService)

def dechetTabStockCible(nbSemaines,tabStockCible,mesDemandes):
    return [dechetsSemainesStockCible(nbSemaines,i,mesDemandes) for i in tabStockCible]
    
def profitTabStockCible(nbSemaines,tabStockCible,mesDemandes):
    tabProfit=[]
    for s in tabStockCible:
        monStock=Stock(1,s,ListeSemainesDeStock)
        for i in mesDemandes:
            monStock.nouvelleSemaine(i)
        tabProfit.append(monStock.profit())
    
    return tabProfit


def simulationPousse():

    tabStockCible=np.arange(0,350,10)
    mu, sigma = 155, 60 # demande moyenne et equart type de la demande moyenne

    nbsemaine=1000
    mesDemandes = np.random.normal(mu, sigma, nbsemaine)
    mesDemandes[mesDemandes<0]=0

    tabServiceSimule =simulerTabStockCible(nbsemaine,tabStockCible,mesDemandes)
    dechets = dechetTabStockCible(nbsemaine,tabStockCible,mesDemandes)
    profits = profitTabStockCible(nbsemaine,tabStockCible,mesDemandes)

    plt.ylabel("Service Reel Simule")
    plt.xlabel("Stock Cible")
    plt.plot(tabStockCible,tabServiceSimule,'ro')

    plt.plot(tabStockCible,dechets)
    #print(tabServiceSimule)
    #print(dechets)
    #plt.show()

    plt.plot(tabStockCible,profits/np.amax(profits),'go')
    plt.show()

simulationPousse()

def simulationFacile():
    tabStockCible=np.arange(0,10,1)

    nbsemaine=10
    mesDemandes = np.ones(10)

    tabServiceSimule =simulerTabStockCible(nbsemaine,tabStockCible,mesDemandes)
    dechets = dechetTabStockCible(nbsemaine,tabStockCible,mesDemandes)
    profits = profitTabStockCible(nbsemaine,tabStockCible,mesDemandes)
    plt.ylabel("Service Reel Simule")
    plt.xlabel("Stock Cible")

    plt.plot(tabStockCible,tabServiceSimule,'ro')
    plt.plot(tabStockCible,dechets)
    #print(tabServiceSimule)
    #print(dechets)
    plt.show()
    plt.plot(tabStockCible,profits,'go')
    plt.show()

#simulationFacile()

def distributionTauxDechet(stockCible):

    tabStockCible=[stockCible]*1000
    mu, sigma = 155, 60 # demande moyenne et equart type de la demande moyenne

    nbsemaine=100
    mesDemandes = np.random.normal(mu, sigma, nbsemaine)
    mesDemandes[mesDemandes<0]=0
    dechets = dechetTabStockCible(nbsemaine,tabStockCible,mesDemandes)
    dechets[0]=dechets[1]
    plt.hist(dechets)
    plt.show()

#distributionTauxDechet(1500)