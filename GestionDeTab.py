# coding: utf-8 


import numpy as np

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

