# coding: utf-8 


import numpy as np
import matplotlib.pyplot as plt
sigma=60

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
    tab,demande=np.arange(0.0,2.0,1),10
    tab=np.ones(10)
    tab,demande=tabProduitMoinsDemande(tab,demande)
    print(tab)
    print(demande)

#def approvisonnement()

#testtabProduitMoinsDemande()

def prixToDemandeMoyenne(prix):
    '''Prix=17719*volume**-0.579'''
    a=17719
    p=-0.579
    volume=(prix/a)**(-1/0.579)#on a le volume par an
    #donc on divise par 52 pour l'avoir en semaine
    return volume/52

#print(prixToDemandeMoyenne(100))#test de fonction
def tabApresRabetDemandeEtProduitRestant(tabStock,demande):
    stockIniDernier=tabStock[len(tabStock)-1]
    if tabStock[len(tabStock)-1]>demande:
        #l'offre répond à toute la demande
        tabStock[len(tabStock-1)]-=demande
        demande=0

    else:
        demande-=tabStock[len(tabStock)-1]
        tabStock[len(tabStock)-1]=0

    nbVendu=stockIniDernier-tabStock[len(tabStock)-1]
    return tabStock,demande,nbVendu

def testTabRabet():
    tabStock,demande,nbVendu=tabApresRabetDemandeEtProduitRestant(np.ones(10),4)
    print(tabStock)
    print(demande)
    print(nbVendu)#on valide la fonction

testTabRabet()


def tabProduitMoinsDemandeEtCADerniereSemaine(tabStock,prixInit,dernierRabet=0,premierRabet=0):
    #on veut simuler l'achat des articles selon leur prix dans le tableau
    stockIniDernier=tabStock[len(tabStock-1)]

    if len(tabStock)>1 and dernierRabet>0:#le gens vont commencer à acheter plus 
        #tant qu'il y a des produits moins chers
        prixDernier=prixInit*(1-dernierRabet)
        demande = np.normal(prixToDemandeMoyenne(prixDernier,sigma))
        if tabStock[len(tabStock-1)]>demande:
            tabStock[len(tabStock-1)]-=demande
            caDernier=prixDernier*(stockIniDernier-tabStock[len(tabStock-1)])
            return tabStock,caDernier

        else:
            demande-=tabStock[len(tabStock-1)]
            tabStock[len(tabStock-1)]=0
    
    if len(tabStock)>2 and premierRabet>0:#le gens vont commencer à acheter plus 
        #tant qu'il y a des produits moins chers
        prixDernier=prixInit*(1-dernierRabet)
        demande = np.normal(prixToDemandeMoyenne(prixDernier,sigma))
        if tabStock[len(tabStock-1)]>demande:
            tabStock[len(tabStock-1)]-=demande
            caDernier=prixDernier*(stockIniDernier-tabStock[len(tabStock-1)])
            return tabStock,caDernier

        else:
            demande-=tabStock[len(tabStock-1)]
            tabStock[len(tabStock-1)]=0       

        return 




'''
mu, sigma = 155, 60 # demande moyenne et equart type de la demande moyenne

nbsemaine=1000
mesDemandes = np.random.normal(mu, sigma, nbsemaine)
plt.hist(mesDemandes)
plt.show()
'''