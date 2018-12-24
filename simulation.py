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

pour 4 semaines on a 
95% de sc pour 245 de stock cible
99% de sc pour 286 de stock cible
"""
import numpy as np
import matplotlib.pyplot as plt
import GestionDeTab as gt
from math import *
from mpl_toolkits.mplot3d import Axes3D
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

def tabProduitMoinsDemande(tab,demande):
    for i in range (len(tab)):
        if tab[-1-i]>demande:
            tab[-1-i]-=demande
            demande=0
        else:
            demande-=tab[-1-i]
            tab[-1-i]=0

    return tab,demande


def tabProduitMoinsDemandeRabet(tabStock,prixInit=97,dRabais=0,aDrabais=0):
    #on veut simuler l'achat des articles selon leur prix dans le tableau
    stockIniDernier=tabStock[-1]
    nbVendu=0

    #if dRabais>0:#le gens vont commencer à acheter plus 
        #tant qu'il y a des produits moins chers
    prixDernier=prixInit*(1-dRabais)

    demande = ceil(np.random.normal(prixToDemandeMoyenne(prixDernier),sigma))
    demande=max(0,demande)

    tabStock,demande=tabApresRabaisDemandeRestante(tabStock,demande)

    nbVendu=stockIniDernier-tabStock[-1]
    if demande == 0:
        return tabStock,demande

    
    if len(tabStock)>2 and aDrabais>0:#le gens vont commencer à acheter plus 
        #tant qu'il y a des produits moins chers
        prixADernier=prixInit*(1-aDrabais)
        #on genere la demande en retirant la demande satisfaite par le premier stock
        demande = ceil(np.random.normal(prixToDemandeMoyenne(prixADernier),sigma))-nbVendu
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
        demande=ceil(np.random.normal(prixToDemandeMoyenne(prixInit),sigma))-nbVendu
        demande=max(0,demande)
        tabStock,demande = tabProduitMoinsDemande(tabStock,demande)

    return tabStock,demande

def testtabProduitMoinsDemandeRabet():
    tab=[100,100,0,100,0,100]
    tab,demande=tabProduitMoinsDemandeRabet(tab)
    print(tab,demande)

testtabProduitMoinsDemandeRabet()


class Stock:
#représente l'état du stock sur les semaines

    def __init__(self,stockCible,ListeSemainesDeStock,prixInit=100,dRabais=0,aDrabais=0):
        self.semaines=ListeSemainesDeStock#liste des stocks qui vont évoluer de semaine en semaine
        self.dechet=0.0
        self.volumeSemaine=np.zeros(len(ListeSemainesDeStock))
        #fait le cumul des produit vendu par semaine dans le stock

        self.nbNonSatifait = 0.0#nombre cumulé des semaines ou la demande n'a pas ete satisfaite
        self.produitNonLivre=0.0#nombre cumulé des demandes non satisfaites
        
        self.fournis= stockCible #nombre de produits que l'on a acheté au fournisseur
        self.stockCible = float(stockCible) #stock avant de répondre à la demande

        self.prixInit = prixInit #prix du produit que l'on veut vendre avec la marge maximale
        self.mu=prixToDemandeMoyenne(self.prixInit) #demande moyenne selon l'elasticité de nos produits
        self.age=0 #nombre de changement de semaine

        self.dRabais=dRabais#le pourcent de rabais sur le dernier produit
        self.aDrabais=aDrabais#le pourcentage de rabais pour l'avant derniere semaine


    def profit(self):
    #renvoi le profit réalisé par les produits du stock
        print(np.sum(self.tabSemaineCA()))
        return np.sum(self.tabSemaineCA())-(self.fournis*97)

    def tabSemaineCA(self):
        #renvoie le ca cumulé semaine stock
        temp= np.zeros(len(self.semaines))
        temp[:2]= self.volumeSemaine[:2]*self.prixInit
        temp[-2]=self.volumeSemaine[-2]*(self.prixInit*(1-self.aDrabais))
        temp[-1]=self.volumeSemaine[-1]*(self.prixInit*(1-self.dRabais))
        return temp

    def stockTotal(self):
        return np.sum(self.semaines)


    #fonctions de passage à une nouvelle semaine
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
        tempSemaines=np.empty_like(self.semaines)
        tempSemaines[:]=self.semaines
        self.semaines,demande= tabProduitMoinsDemandeRabet(self.semaines,self.prixInit,self.dRabais,self.aDrabais)
        self.volumeSemaine=self.volumeSemaine+(tempSemaines-self.semaines)
        if(demande>0):
            self.nbNonSatifait+=1
            self.produitNonLivre+=demande
        else:
            self.dechet+=self.semaines[-1]

        #ON décale les semaines

        self.semaines[1:]=self.semaines[:-1]
        
        #On initialise la nouvelle semaine
        self.semaines[0]=0
        self.semaines[0]=1.0*(self.stockCible-self.stockTotal())
        self.fournis+=self.semaines[0]

    def printStock(self):
        print("age=",self.age)
        # print("stockTotal=",self.stockTotal())
        print("etatDuStock=",self.semaines)
        # print("vendus cumulé semaine stock=",self.volumeSemaine)
        # print("ca cumulé semaine stock=",self.tabSemaineCA())
        # print("stockFournis=",self.fournis)
        print("stockDechet=",self.dechet)
        print("tauxDechet=",self.tauxDechet())
        print("PersonnesNOnsatisfaites=",self.nbNonSatifait)

    def tauxDechet(self):
        if self.fournis>1.0 and self.age>0 :
            return (self.dechet/float(self.fournis))#(prixToDemandeMoyenne(self.prixInit)*self.age))#demander au prof de vérifier
        return 0.0



nbSemPermenption = 4
ListeSemainesDeStock = np.zeros(nbSemPermenption)




def testChangementSemaine():
    stockCible = 1000
    demande=0
    ListeSemainesDeStock = np.array([stockCible,0,0,0,0])
    monStock=Stock(stockCible,ListeSemainesDeStock)
    for i in np.zeros(10):
        monStock.printStock()
        #monStock.nouvelleSemaine(demande)
        #monStock.nouvelleSemainePrix()
        monStock.nouvelleSemaineRabaiss()
        #monStock.printStock()

#testChangementSemaine()

def simulerSemainesStockCible(nbSemaines,stockCible,demandes):
    ListeSemainesDeStock[0]=stockCible
    monStock=Stock(stockCible,ListeSemainesDeStock)

    for i in demandes:
        monStock.nouvelleSemaineRabaiss()

    serviceCibleReel = 1 - (float(monStock.nbNonSatifait)/float(nbSemaines))
   
    return serviceCibleReel

def dechetsSemainesStockCible(nbSemaines,stockCible,demandes):
    ListeSemainesDeStock[0]=stockCible
    monStock=Stock(stockCible,ListeSemainesDeStock)

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
        monStock=Stock(s,ListeSemainesDeStock)
        for i in mesDemandes:
            monStock.nouvelleSemaineRabaiss()
        tabProfit.append(monStock.profit())
    
    return tabProfit

def simulationPousse():

    tabStockCible=np.arange(0,500,30)
    mu, sigma = 155, 60 # demande moyenne et equart type de la demande moyenne

    nbsemaine=10000
    mesDemandes = np.zeros(nbsemaine)#np.random.normal(mu, sigma, nbsemaine)
    #mesDemandes[mesDemandes<0]=0

    '''#pour visualiser le service cible'''
    # tabServiceSimule =simulerTabStockCible(nbsemaine,tabStockCible,mesDemandes)
    # plt.plot(tabStockCible,tabServiceSimule,'co',label='taux de ServiceCible')
    # plt.ylabel("Service Reel Simule")
    # plt.show()

    '''#pour les déchets'''
    # dechets = dechetTabStockCible(nbsemaine,tabStockCible,mesDemandes)
    # plt.plot(tabStockCible,dechets,'k',label='taux de Déchet')
    # plt.ylabel("taux de déchet")

    '''#pour le profit'''
    profits = profitTabStockCible(nbsemaine,tabStockCible,mesDemandes)
    plt.plot(tabStockCible,profits,'yo',label='taux de profit')
    plt.ylabel("profit") 
 
    plt.xlabel("Stock Cible")

    #plt.show() 
    #print(tabServiceSimule)
    #print(dechets)
    plt.show()

    
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
    monStock=Stock(stockCible,stockIni,dRabais=Drabais)
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
        monStock=Stock(stockCible,semaineStock,dRabais=r)
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

def dechetsSemaines(nbSemaineSimulation=3000):
#OBJECTIF montrer l'evolution des déchets en fonction du
#nombre de semaine de peremption et du stock cible
    minSC,maxSC,pas=100,300,10
    stockCible=np.arange(minSC,maxSC,pas)

    minp,maxp,pasp=2,5,1
    peremption=np.arange(minp,maxp,pasp)
    dechets=np.empty([len(peremption),len(stockCible)])

    for p in peremption:
        stockInit=np.zeros(p)
        for sc in stockCible:
            monStock=Stock(sc,stockInit)
            for s in range(nbSemaineSimulation):
                monStock.nouvelleSemaineRabaiss()
            dechets[(p-minp)//pasp,(sc-minSC)//pas]=monStock.tauxDechet()

    '''plotting to image
    plt.imshow(dechets)
    plt.show()'''

    '''plotting to plot
    hf = plt.figure()
    ha = hf.add_subplot(111, projection='3d')
    x=peremption
    y=stockCible
    X, Y = np.meshgrid(np.array(x,y),np.array(y,x) )  # `plot_surface` expects `x` and `y` data to be 2D
    ha.plot_surface(X, Y, dechets)

    plt.show()'''

    for p in peremption:
        plt.plot(stockCible,dechets[p-minp])
    plt.show()

    return dechets

#dechetsSemaines()
    
def profitsSemaines(nbSemaineSimulation=1000):
#OBJECTIF montrer l'evolution des profits en fonction du
#nombre de semaine de peremption et du stock cible
    minSC,maxSC,pas=0,300,40
    stockCible=np.arange(minSC,maxSC,pas)

    minp,maxp,pasp=2,5,1
    peremption=np.arange(minp,maxp,pasp)
    profit=np.zeros([len(peremption),len(stockCible)])
    profitR=np.zeros([len(peremption),len(stockCible)])

    for p in peremption:
        stockInit=np.zeros(p)
        for sc in stockCible:
            monStock=Stock(sc,stockInit)
            monSRabet=Stock(sc,stockInit,dRabais=0.1)
            for s in range(nbSemaineSimulation):
                monStock.nouvelleSemaineRabaiss()
                monSRabet.nouvelleSemaineRabaiss()
            profit[(p-minp)//pasp,(sc-minSC)//pas]=monStock.profit()
            profitR[(p-minp)//pasp,(sc-minSC)//pas]=monSRabet.profit()
        print(p)
    for p in peremption:
        #mettre les valeurs négaties à zero avec .clip
        #plt.plot(stockCible,profit[p-minp].clip(min=0),color=('#0005'+str(p)+'0'))
        plt.plot(stockCible,profitR[p-minp].clip(min=0),color=('#8989'+str(p)+'0'))
    plt.ylabel("Profit en € pour des valeurs positives sinon 0")
    plt.xlabel("Stock Cible")
    plt.show()

    return profit

profitsSemaines()

