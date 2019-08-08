Simulation de Stock
===================

Introduction
------------

Pour notre simulation de stock nous avons choisi de coder dans le
langage python.

Nous avons créé une classe stock que nous allons invoquer et manipuler.

Pour l’invoquer (ou la construire) on peut simplement spécifier le stock
cible et le nombre des produits dans les semaines du stock initialement.
Par exemple pour un stock de deux semaines avec 2 produits à la première
semaine et 3 produits à la deuxième, on passera en paramètre la liste
suivante : \[2,3\].

On peut aussi construire un stock avec des paramètres optionnels. D’une
part, le prix initial de vente du produit peut être changé alors qu’il
est à 100 par défaut. D’autre part, le rabais à la dernière semaine de
stock est par défaut à 0 ainsi qu’à l’avant dernière semaine.

Nous allons principalement manipuler la class Stock avec la méthode de
changement de semaine. La méthode de changement de semaine calcule
l’état du stock à de la semaine k en fonction des l’état du stock à la
semaine k-1. D’ailleurs, le nombre de changement de semaine est compté à
travers la variable self.age.

Voici les attributs de cette classe : cela vous permet d’avoir un aperçu
des paramètres que nous allons mettre à jour à chaque nouvel appel de la
méthode de changement de semaine.

  ----------------------------------------------------------------------------------------------------------
  class Stock:\
  \#représente l'état du stock sur les semaines\
  \
      def \_\_init\_\_(self,stockCible,ListeSemainesDeStock,prixInit=100,dRabais=0,aDrabais=0):\
         self.semaines=ListeSemainesDeStock\#liste des stocks qui vont évoluer de semaine en semaine\
         self.dechet=0.0\
         self.volumeSemaine=np.zeros(len(ListeSemainesDeStock))\
         \#fait le cumul des produit vendu par semaine dans le stock\
  \
         self.nbNonSatifait = 0.0\#nombre cumulé des semaines ou la demande n'a pas ete satisfaite\
         self.produitNonLivre=0.0\#nombre cumulé des demandes non satisfaites\
       \
         self.fournis= stockCible \#nombre de produits que l'on a acheté au fournisseur\
         self.stockCible = float(stockCible) \#stock avant de répondre à la demande\
  \
         self.prixInit = prixInit \#prix du produit que l'on veut vendre avec la marge maximale\
         self.mu=prixToDemandeMoyenne(self.prixInit) \#demande moyenne selon l'elasticité de nos produits\
         self.age=0 \#nombre de changement de semaine\
  \
         self.dRabais=dRabais\#le pourcent de rabais sur le dernier produit\
         self.aDrabais=aDrabais\#le pourcentage de rabais pour l'avant derniere semaine
  ----------------------------------------------------------------------------------------------------------

Service cible et Stock cible
----------------------------

Pour le moment nous traitons le cas où le stock fait en 4 semaines. On a
donc quatre semaines pour vendre un produit ensuite il atteindra sa date
d’expiration et nous le jetterons.

On veut visualiser Figure 1 la relation entre le nombre de produits
disponibles dans nos quatre semaines de stock (stock cible) et la part
des clients satisfaits (service cible).

![](/media/image1.png){width="6.317708880139983in"
height="4.75196741032371in"}

[[]{#_Ref533525523 .anchor}]{#_Ref533524840 .anchor}Figure 1:
[]{#_Ref533524953 .anchor}Mettre en exergue l'évolution croissante du
taux de déchet (en noir) et le taux de service cible (en bleu) pour un
stock sur 4 semaines

Etude du profit
---------------

Le profit est positif pour des valeurs de stock cible inférieur à 400,
Figure 2 pour le stock dispersé sur 4 semaines. On considère que quand
le profit est négatif, l’entreprise perd de l’argent. C’est pourquoi on
va plutôt s’intéresser aux valeurs de notre stock Cible avant 400 car
ensuite le profit tend de plus en plus rapidement vers moins l’infini.

On calcule chaque profit à la fin d’une simulation pour un stock cible.
A la fin de toutes les simulations donc une liste de profit en en
fonction du stock cible. Cette liste a un maximum. On divise chaque
valeur de la liste par ce maximum. Donc on obtient une liste avec des
taux de profit (ce qui est assez pratique pour comparer les simulations
entre elles).

![](/media/image2.png){width="6.270138888888889in"
height="4.7027777777777775in"}

[]{#_Ref533525582 .anchor}Figure 2: influence du stock cible sur les
taux pour un stock de 4 semaines

On peut aussi visualiser l’évolution du profit en fonction du nombre de
semaine de notre stock Figure 3 (longueur de la liste
ListeSemainesDeStock). On remarque que plus on a de semaines de stock,
plus on fait de profit et mieux on répond à la demande.

![](/media/image3.png){width="6.270138888888889in"
height="4.336111111111111in"}

[]{#_Ref533525641 .anchor}Figure 3: profits comparés à la durée de stock
maximum

Etude des déchets pour un service cible de 95%
----------------------------------------------

On souhaite connaitre le stock cible qui correspond à un service cible
de 95%.

On considère que l’on vend des produits de manière discrète. En
réduisant l’étude autour d’un stock cible de 240 à 250 et une simulation
pour 100000 semaines (presque 2000 ans) on voit que 245 est le premier
stock cible pour lequel cela correspond:

![](/media/image4.png){width="6.270833333333333in"
height="4.708333333333333in"}

Figure 4: Service cible proche de 95%

C’est donc à partir de ce stock cible de 245 que l’on lance une
simulation Figure 5 pour étudier la répartition du taux de déchet pour
un service cible de 95% et sur 1000 simulations. Sachant que le taux de
déchet est calculé en fonction du nombre de produits fournis et du
nombre de produits non vendus à la dernière semaine, on peut calculer le
taux de déchet.

![](/media/image5.png){width="6.270833333333333in"
height="4.708333333333333in"}

[]{#_Ref533525975 .anchor}Figure 5: taux de déchets (en abscisse) pour
milles simulations d'un stock avec 4 semaines avant le rejet. On voit
donc que pour 1000 simulations 100 obtiennent 0.05% de déchet pour un
stock cible de 245

On remarque que ce taux de déchet est très bas ce qui est normal pour un
stock étalé sur 4 semaines. On ne sait pas la loi statistique que suit
le taux.

Pour deux semaines on trouve une autre forme de répartition centrée sur
des valeurs plus élevées.

![](/media/image6.png){width="6.270833333333333in"
height="4.708333333333333in"}

Figure 6: taux de déchets (en abscisse) pour milles simulations d'un
stock avec 2 semaines avant le rejet. On voit donc que pour 1000
simulations 60 obtiennent environ 7.2% de déchet pour un stock cible de
245

Pour deux semaines on a en moyenne 0.065 taux de déchet. Ce qui
correspond à une perte de 0.065\*97=6,5 € par produit vendu. En effet,
on ne peut pas répondre à une telle part de client avec si peu de
semaine de stock.

![](/media/image7.png){width="6.270138888888889in"
height="4.7027777777777775in"}

Figure 7: comparaison des taux de déchet en fonction des semaines de
stock

Elasticité du prix
------------------

On utilise les données sur les volumes (nombre de produit vendu) et du
prix de vente des produits du tableau de l’exercice 1 pour établir une
relation entre le prix et le volume de vente d’un produit.

[\[CHART\]]{.chart}

Figure 8:Prix de vente en fonction du volume

Dans Excel on peut chercher un modèle de fonction qui pourrait être
utilisé comme modèle de prédiction et qui corresponde à nos données
empiriques. On a testé différents types de fonctions et c’est la
fonction puissance qui obtient un coefficient de corrélation de Pearson
le plus haut avec r²=0,9995.

[\[CHART\]]{.chart}

Figure 9:Prix de vente par rapport au volume des ventes avec échelles
logarithmiques

Nous avons un modèle qui lie le prix *P* et le volume de vente *V* la
relation : $P_{i} = aV_{i}^{b} = 17719V_{i}^{- 0,579}$ d’où
$\ln P_{i} = 9,7824 - 0,5785\ln V_{i}$.

Avec la formule liant le prix et le volume vendu, l’évolution du stock
ne sera plus basée sur une demande moyenne mais sur le prix du produit
qui va être vendu.

Dans notre code on a une minuscule fonction pour convertir les prix en
volume :

  ------------------------------------------------------------------------------------------------------------------------------
  def prixToDemandeMoyenne(prix):\
      '''Prix=17719\*volume\*\*-0.579'''\
      if prix&gt;0 :\
           volume=(prix/17719)\*\*(-1.727) \#aller plus vite?\
           \#volume=-1.727\*(100/17719)\*\*(-1.727-1)\*(prix-100) + (100/17719)\*\*(-1.727) \#tangente pour un prix à 100    \
      else:\
           volume=1\
      \#donc on divise par 52 pour l'avoir en semaine\
      return volume/52
  ------------------------------------------------------------------------------------------------------------------------------
  ------------------------------------------------------------------------------------------------------------------------------

Recherche du dernier rabais optimal
-----------------------------------

Ensuite on peut essayer de faire varier une promotion sur le produit qui
va bientôt être jeté.

Dans la simulation, la dernière semaine propose un produit moins cher.
Ainsi on génère une demande aléatoire associée au prix du produit de la
dernière semaine. On répond donc à la demande générée aléatoirement avec
les produits de la dernière semaine. Pour les semaines restantes on
génère une nouvelle demande associée au prix initial du produit mais on
soustrait le nombre de produit déjà vendus à la dernière semaine.

On décide tout d’abord de visualiser le profit généré en faisant varier
la promotion de 0 à 100% du prix initial pour un stock de 4 semaines et
pour un prix initial de 100€ et un service cible de 95%. On remarque que
le profit admet un maximum pour une valeur de rabais proche de 0.2 ce
qui correspond à une remise de 20% sur les produits de la dernière
semaine.![](/media/image8.png){width="6.270138888888889in"
height="4.7027777777777775in"}

Figure 10:profit en fonction du rabais sur la dernière semaine

Chiffre d’affaire par semaines
------------------------------

On peut calculer le chiffre d’affaire cumulé réalisé par les différentes
semaines de du stock de 4 semaine. On remarque que les deux premières
semaines en significativement plus de Chiffre d’affaire que les deux
dernières. Cependant, appliquer un rabais sur la dernière semaine ne
fait pas varier significativement la répartition du chiffre d’affaire.

![](/media/image9.png){width="6.270138888888889in"
height="4.7027777777777775in"}

Figure 11: Chiffre d'affaire par semaine (la première a l'indice 0)

Impacts sur les déchets
-----------------------

Pour un service cible de 95% on a donc diminué notre proportion de
déchet.

![](/media/image10.png){width="6.270138888888889in"
height="4.663194444444445in"}

Figure 12: Répartition pour 4 semaines avec un rabais sur la dernière
semaine

![](/media/image11.png){width="5.259722222222222in"
height="3.9449376640419946in"}

Figure 13:impact d'un rabais de 20% sur la dernière semaine sur les taux
de déche

Un Avant Dernier rabais
-----------------------

Nous avons testé l’implémentation d’un rabais sur l’avant dernière
semaine de notre stock. Malheureusement les résultats sont décevants en
termes d’analyse. En effet on ne trouve pas de maximum pour le profit en
faisant varier le rabais de l’avant dernier rabais. On obtient une
droite décroissante en fonction du rabais. Autrement dit : on a
seulement une augmentation du profit quand on augmente le prix de
l’avant dernière semaine. Nous pensons que c’est probablement une erreur
de notre part car nous aurions pensé que le profit se comporterait comme
lors de la variation du rabais de la dernière semaine.

Conclusion
----------

Cette simulation peut paraitre difficile à aborder mais finalement le
code n’est pas si compliqué.

Nous pouvons réfléchir à améliorer la lisibilité du code ainsi que sa
rapidité. En effet, il est possible de réduire le temps de calcul des
simulations en réécrivant quelques fonctions (par exemple la fonction
pour produire la Figure 2 fait trois simulations alors qu’on ne pourrait
en faire qu’une seule).

Pour continuer le travail nous pourrions ajouter le coût d’une semaine
de stock ou le cout des traitement des déchets afin de voir l’utilité
réelle d’ajouter les semaines de stock sachant que le chiffre d’affaire
diminue avec l’âge des produits…
