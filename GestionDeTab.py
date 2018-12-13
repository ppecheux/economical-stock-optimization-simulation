# coding: utf-8 


import numpy as np
import matplotlib.pyplot as plt
sigma=1

def decalCaseTab(tab):
    #retoune le tableau avec les valeurs décallées mais avec la premiere case <- derniere nouvelle case
    '''for i in range (len(tab)):
        tab[len(tab)-1-i]=tab[len(tab)-2-i]'''

    tab[1:]=tab[:-1]
    tab[0]=0
    return tab

def testdecalCaseTab():
    tab=np.arange(1,6,1)
    print(tab)
    print(decalCaseTab(tab))

#testdecalCaseTab()

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
def tabApresRabetDemandeRestante(tabStock,demande):

    if tabStock[len(tabStock)-1]>demande:
        #l'offre répond à toute la demande
        tabStock[len(tabStock)-1]-=demande
        demande=0

    else:
        demande-=tabStock[len(tabStock)-1]
        tabStock[len(tabStock)-1]=0

    print("tabApresRabetDemandeRestante:",tabStock)
    print(demande)
    return tabStock,demande

def testTabRabet():
    arr=np.ones(3)

    tabStock,demande=tabApresRabetDemandeRestante(arr[:-1],4)
    tabStock=np.append(tabStock,[0])
    print(tabStock)
    print(demande)
    #on valide la fonction

#testTabRabet()


def tabProduitMoinsDemandeEtCADerniereSemaine(tabStock,prixInit,dernierRabet=0,premierRabet=0):
    #on veut simuler l'achat des articles selon leur prix dans le tableau
    stockIniDernier=tabStock[len(tabStock)-1]
    caDernier=0
    nbVendu=0

    #if dernierRabet>0:#le gens vont commencer à acheter plus 
        #tant qu'il y a des produits moins chers
    prixDernier=prixInit*(1-dernierRabet)

    demande = np.random.normal(prixToDemandeMoyenne(prixDernier),sigma)
    demande=max(0,demande)
    print(tabStock)
    print(demande)
    tabStock,demande=tabApresRabetDemandeRestante(tabStock,demande)

    nbVendu=stockIniDernier-tabStock[len(tabStock)-1]
    caDernier=prixDernier*nbVendu
    if demande == 0:
        return tabStock,demande,caDernier

    
    if len(tabStock)>2 and premierRabet>0:#le gens vont commencer à acheter plus 
        #tant qu'il y a des produits moins chers
        prixADernier=prixInit*(1-premierRabet)
        #on genere la demande en retirant la demande satisfaite par le premier stock
        demande = np.random.normal(prixToDemandeMoyenne(prixADernier),sigma)-nbVendu
        demande=max(0,demande)
        if demande>0:
            stockIniADernier=tabStock[len(tabStock)-2]
            tabStock,demande=tabApresRabetDemandeRestante(tabStock[:-1],demande) #on considère le sous stock
            tabStock=np.append(tabStock,[0])
            nbVendu+=stockIniADernier-tabStock[len(tabStock)-2]

            if demande == 0:
                return tabStock,demande,caDernier
    
    #finalement les autres semaines sont achetées
    if np.sum(tabStock)>0:
        print("nbvendu=",nbVendu)
        demande=np.random.normal(prixToDemandeMoyenne(prixInit),sigma)-nbVendu
        demande=max(0,demande)
        print(tabStock)
        print(demande)
        tabStock,demande = tabProduitMoinsDemande(tabStock,demande)
    else:
        print ('tabProduitMoinsDemandeEtCADerniereSemaine')
        #exit('Failure')
    return tabStock,demande,caDernier

def testProdDemCADer():

    tab=np.array([100,100,100,100])
    prixInit=50
    rabet=0.1
    rabet2=0.05
    '''sans rabet
    tab,demande,cad=tabProduitMoinsDemandeEtCADerniereSemaine(tab,prixInit)
    '''
    '''avec un premier rabet
    tab,demande,cad=tabProduitMoinsDemandeEtCADerniereSemaine(tab,prixInit,dernierRabet=rabet)
    '''

    tab,demande,cad=tabProduitMoinsDemandeEtCADerniereSemaine(tab,prixInit,dernierRabet=rabet,premierRabet=rabet2)
    print(tab)
    print(demande)
    print(cad)

#testProdDemCADer()

'''
mu, sigma = 155, 60 # demande moyenne et equart type de la demande moyenne

nbsemaine=1000
mesDemandes = np.random.normal(mu, sigma, nbsemaine)
plt.hist(mesDemandes)
plt.show()
'''