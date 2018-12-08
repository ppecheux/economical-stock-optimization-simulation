# coding: utf-8 


import numpy as np
import matplotlib.pyplot as plt
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

print(prixToDemandeMoyenne(100))

print(52*7)


'''
mu, sigma = 155, 60 # demande moyenne et equart type de la demande moyenne

nbsemaine=1000
mesDemandes = np.random.normal(mu, sigma, nbsemaine)
plt.hist(mesDemandes)
plt.show()
'''