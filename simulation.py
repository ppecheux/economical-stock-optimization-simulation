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

elasticité= prix/volume voir sur wikipedia
volume en fonction du stock cible
c'est la fonction qui lie l e prix au volume

on a calculé que Prix=17719*volume**-0.579

prix variable

dp/p / dp/v
"""
import numpy as np
import matplotlib.pyplot as plt
import GestionDeTab as gt
sigma=60

def prixToDemandeMoyenne(prix):
    '''Prix=17719*volume**-0.579'''
    #a=17719
    #p=-0.579
    if prix>0 :
        volume=(float(prix)/17719)**(-1/0.579)#on a le volume par an
    else:
        volume=1
    #donc on divise par 52 pour l'avoir en semaine
    return volume/52

def tabApresRabaisDemandeRestante(tabStock,demande):

    if tabStock[-1]>demande:
        #l'offre répond à toute la demande
        tabStock[-1]-=demande
        demande=0

    else:
        demande-=tabStock[-1]
        tabStock[-1]=0

    return tabStock,demande

def tabProduitMoinsDemandeRabet(tabStock,prixInit=97,dRabais=0,aDrabais=0):
    #on veut simuler l'achat des articles selon leur prix dans le tableau
    stockIniDernier=tabStock[-1]
    nbVendu=0

    #if dRabais>0:#le gens vont commencer à acheter plus 
        #tant qu'il y a des produits moins chers
    prixDernier=prixInit*(1-dRabais)

    demande = np.random.normal(prixToDemandeMoyenne(prixDernier),sigma)
    demande=max(0,demande)

    tabStock,demande=tabApresRabaisDemandeRestante(tabStock,demande)

    nbVendu=stockIniDernier-tabStock[-1]
    if demande == 0:
        return tabStock,demande

    
    if len(tabStock)>2 and aDrabais>0:#le gens vont commencer à acheter plus 
        #tant qu'il y a des produits moins chers
        prixADernier=prixInit*(1-aDrabais)
        #on genere la demande en retirant la demande satisfaite par le premier stock
        demande = np.random.normal(prixToDemandeMoyenne(prixADernier),sigma)-nbVendu
        demande=max(0,demande)
        if demande>0:
            stockIniADernier=tabStock[-2]
            tabStock,demande=tabApresRabaisDemandeRestante(tabStock[:-1],demande) #on considère le sous stock
            tabStock=np.append(tabStock,[0])
            nbVendu+=stockIniADernier-tabStock[-2]

            if demande == 0:
                return tabStock,demande
    
    #finalement les autres semaines sont achetées
    if np.sum(tabStock)>0:
        #print("nbvendu=",nbVendu)
        demande=np.random.normal(prixToDemandeMoyenne(prixInit),sigma)-nbVendu
        demande=max(0,demande)
        tabStock,demande = tabProduitMoinsDemande(tabStock,demande)

    return tabStock,demande

class Stock:
    '''représente l'état du stock sur les semaines'''

    def __init__(self,serviceCible,stockCible,ListeSemainesDeStock,prixInit=100,dRabais=0,aDrabais=0):
        self.semaines=ListeSemainesDeStock#liste de stock
        self.dechet=0.0#on aurait pu mettre comme une semaine suplémentaire...
        self.volumeSemaine=np.zeros(len(ListeSemainesDeStock))#fait le cumul des produit vendu par semaine dans le stock

        self.nbNonSatifait = 0.0
        self.produitNonLivre=0.0
        
        self.fournis= stockCible
        self.stockCible = float(stockCible)

        self.prixInit = prixInit
        self.mu=prixToDemandeMoyenne(self.prixInit)
        self.age=0

        self.dRabais=dRabais#le pourcent de rabais sur le dernier produit
        self.aDrabais=aDrabais

    def chiffreAff(self):
        return (self.fournis-self.dechet)*self.prixInit

    def profit(self):
        #renvoi le tableau des profits des semaines
        prix=np.ones(len(self.semaines))
        prix[-1]*=(1-self.dRabais)
        prix[-2]*=(1-self.aDrabais)
        return np.sum(self.tabSemaineCA()*prix)-(self.fournis*97)

    def tabSemaineCA(self):
        #renvoie le ca cumulé semaine stock
        temp= np.zeros(len(self.semaines))
        temp[:2]= self.volumeSemaine[:2]*self.prixInit
        temp[-2]=self.volumeSemaine[-2]*(self.prixInit*(1-self.aDrabais))
        temp[-1]=self.volumeSemaine[-1]*(self.prixInit*(1-self.dRabais))
        return temp

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
        self.semaines[1:]=self.semaines[:-1]
        
        #On initialise la nouvelle semaine
        self.semaines[0]=0.0
        self.semaines[0]=1.0*(self.stockCible-self.stockTotal())
        self.fournis+=self.semaines[0]
    

    def nouvelleSemainePrix(self):
        self.age+=1

        #generation d'une demande aléatoire en adéquation au prix du produit
        demande = max(0,np.random.normal(self.mu, 60))

        self.semaines,demande = tabProduitMoinsDemande(self.semaines,demande)
        if(demande>0):
            self.nbNonSatifait+=1
            self.produitNonLivre+=demande
        else:
            self.dechet+=self.semaines[len(self.semaines)-1]

        #ON décale les semaines

        self.semaines[1:]=self.semaines[:-1]
        
        #On initialise la nouvelle semaine
        self.semaines[0]=0.0
        self.semaines[0]=1.0*(self.stockCible-self.stockTotal())
        self.fournis+=self.semaines[0]

    def nouvelleSemaineRabaiss(self):
        self.age+=1
        tempSemaines=np.zeros(len(self.semaines))
        tempSemaines[:]=self.semaines
        self.semaines,demande= tabProduitMoinsDemandeRabet(self.semaines,self.prixInit,self.dRabais,self.aDrabais)
        self.volumeSemaine=self.volumeSemaine+(tempSemaines-self.semaines)
        if(demande>0):
            self.nbNonSatifait+=1
            self.produitNonLivre+=demande
        else:
            self.dechet+=self.semaines[len(self.semaines)-1]

        #ON décale les semaines

        self.semaines[1:]=self.semaines[:-1]
        
        #On initialise la nouvelle semaine
        self.semaines[0]=0
        self.semaines[0]=1.0*(self.stockCible-self.stockTotal())
        self.fournis+=self.semaines[0]

    def printStock(self):
        print("age=",self.age)
        print("stockTotal=",self.stockTotal())
        print("etatDuStock=",self.semaines)
        print("vendus cumulé semaine stock=",self.volumeSemaine)
        print("ca cumulé semaine stock=",self.tabSemaineCA())
        print("stockFournis=",self.fournis)
        print("stockDechet=",self.dechet)
        print("tauxDechet=",self.tauxDechet())
        print("PersonnesNOnsatisfaites=",self.nbNonSatifait)

    def tauxDechet(self):
        if self.fournis>1.0 and self.age>0 :
            return (self.dechet/float(self.fournis))#(prixToDemandeMoyenne(self.prixInit)*self.age))#demander au prof de vérifier
        return 0.0



nbSemPermenption = 2
ListeSemainesDeStock = np.zeros(nbSemPermenption)


def tabProduitMoinsDemande(tab,demande):
    for i in range (len(tab)):
        if tab[len(tab)-1-i]>demande:
            tab[len(tab)-1-i]-=demande
            demande=0
        else:
            demande-=tab[len(tab)-1-i]
            tab[len(tab)-1-i]=0

    return tab,demande

def testChangementSemaine():
    stockCible = 600
    demande=0
    ListeSemainesDeStock = np.array([100,0,0])
    monStock=Stock(1,stockCible,ListeSemainesDeStock)
    for i in np.zeros(10):
        monStock.printStock()
        #monStock.nouvelleSemaine(demande)
        #monStock.nouvelleSemainePrix()
        monStock.nouvelleSemaineRabaiss()
        #monStock.printStock()

testChangementSemaine()

def simulerSemainesStockCible(nbSemaines,stockCible,demandes):
    ListeSemainesDeStock[0]=stockCible
    monStock=Stock(1,stockCible,ListeSemainesDeStock)

    for i in demandes:
        monStock.nouvelleSemaineRabaiss()

    serviceCibleReel = 1 - (float(monStock.nbNonSatifait)/float(nbSemaines))
   
    return serviceCibleReel

def dechetsSemainesStockCible(nbSemaines,stockCible,demandes):
    ListeSemainesDeStock[0]=stockCible
    monStock=Stock(1,stockCible,ListeSemainesDeStock)

    for i in demandes:
        monStock.nouvelleSemainePrix()
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
            monStock.nouvelleSemainePrix()
        tabProfit.append(monStock.profit())
    
    return tabProfit

def simulationPousse():

    tabStockCible=np.arange(284,287,1)
    mu, sigma = 155, 60 # demande moyenne et equart type de la demande moyenne

    nbsemaine=30000
    mesDemandes = np.zeros(nbsemaine)#np.random.normal(mu, sigma, nbsemaine)
    #mesDemandes[mesDemandes<0]=0

    tabServiceSimule =simulerTabStockCible(nbsemaine,tabStockCible,mesDemandes)
    #dechets = dechetTabStockCible(nbsemaine,tabStockCible,mesDemandes)
    profits = profitTabStockCible(nbsemaine,tabStockCible,mesDemandes)

    plt.ylabel("Service Reel Simule")
    plt.xlabel("Stock Cible")
    plt.plot(tabStockCible,tabServiceSimule,'co',label='taux de ServiceCible')

    #plt.plot(tabStockCible,dechets,'k',label='taux de Déchet')
    #print(tabServiceSimule)
    #print(dechets)
    plt.show()

    #plt.plot(tabStockCible,profits/np.amax(profits),'yo',label='taux de profit')
    #plt.show()

#simulationPousse()

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

    nbsemaine=1000
    mesDemandes = np.zeros(nbsemaine)#np.random.normal(mu, sigma, nbsemaine)
    dechets = dechetTabStockCible(nbsemaine,tabStockCible,mesDemandes)
    dechets[0]=dechets[1]
    plt.hist(dechets)
    plt.show()

#distributionTauxDechet(245)

def tauxCAD(stockCible=245,ADrabais=0,Drabais=0,nbSemaine=100,nbSemPermenption=4):
    stockIni=np.zeros(nbSemPermenption)
    monStock=Stock(1,stockCible,stockIni,dRabais=Drabais)
    for s in range(nbSemaine):
        monStock.nouvelleSemaineRabaiss()
    return monStock.caDeLaDerniereSemaine/monStock.chiffreAff()

#print(tauxCAD())

def tauxCADperemption(stockCible=245,ADrabais=0,Drabais=0,nbSemaine=100):
    taux = np.array([])
    ageRejetMax=6
    tabSemaineMax=np.arange(2,ageRejetMax,1)
    for i in tabSemaineMax:
        t=tauxCAD(stockCible=245,ADrabais=0,Drabais=0,nbSemaine=1000,nbSemPermenption=i)
        print(t)
        taux=np.append(taux,[t])

    plt.ylabel("Part de CA de la derniere semaine")
    plt.xlabel("Nombre de semaine avant le rejet")
    plt.plot(tabSemaineMax,taux)
    #plt.show()
    return taux

def tauxCADperemptionRabais(pas=0):
    #Fonction qui montre un tableau qui fait varier la semaine de peremption
    #le taux de rabais avec le pas et donne le taux de CAD de la dernière semaine
    tauxCADperemption()
    if(pas!=0):
        r=np.arange(pas,1,pas)
        for i in r:
            tauxCADperemption(Drabais=i)
    plt.show()

#tauxCADperemptionRabais(pas=0.2)

def profitRabais(stockCible=300,ADrabais=0,Drabais=0,nbSemaine=100000,nbSemPermenption=4):
    #fonction qui montre l'évolution du profit lors de la variation du rabet sur al dernière semaine
    semaineStock=np.zeros(nbSemPermenption)
    tabprofit=np.array([])
    #tabDrabais=np.arange(0,1,0.1)
    tabDrabais=np.arange(0,0.02,0.002)
    for r in tabDrabais:
        monStock=Stock(1,stockCible,semaineStock,dRabais=r)
        for s in range(nbSemaine):
            monStock.nouvelleSemaineRabaiss()
        tabprofit=np.append(tabprofit,monStock.profit())
        print(r)#pour voir à quel stade de la simulation nous sommes
    #creation du graph
    #on normalise les profits dans le graph
    '''pour afficher le tableau'''
    plt.ylabel("Profit / profit max")
    plt.xlabel("Rabais en: 0.1 -> prixInit-10%")
    plt.plot(tabDrabais,tabprofit/np.amax(tabprofit))
    plt.show()
    

    print(tabprofit)

#profitRabais()
