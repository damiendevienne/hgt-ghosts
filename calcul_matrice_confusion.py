#!/usr/bin/python3
###############
########### Utilisation
########### Python3 calcul_matrice_confusion [events zombi] [uts echantillonnée] [arbre complet zombi] [arbre échantillonnée zombi] [arbre échantillonnée ale] [numero de gene]
###########
###############
############################################################################### Importation #########################################################################

from ete3 import Tree
import argparse
import sys

############################################################################### Déclaration #########################################################################
zombi = open(sys.argv[1],"r")
ale = open(sys.argv[2],"r")
arbre_zombi= Tree(sys.argv[3] ,format=1)
arbre_vivant = Tree(sys.argv[4],format =1) #petit
arbre_ale = Tree(sys.argv[5] ,format=1)
nom_gene = sys.argv[6]

score = []
vp = 0
fn = 0
fp = 0

transfert_zombi_donneur = []
transfert_zombi_receveur = []

transfert_ale_donneur = []
transfert_ale_receveur = []

dico_zombi = dict() ## permet le mapping entre l'arbre de Zombi et l'arbre de ALE
dico_infere = dict() ## permet de conserver la correspondance entre un transfert ALE et un transfert Zombi
occurence = dict() ## pour noter le nombre d'occurence de chaque transfert suite aux prédictions

############################################################################### Fonction #########################################################################
def recherche_inverse(dico, valeur):
    for k in dico:
        if dico[k] == valeur:
            return k

############################################################################### Prédiction #########################################################################
liste_feuille_vivante = [i.name for i in arbre_vivant]
liste_feuille = [i.name for i in arbre_zombi]
liste_morte = list(set(liste_feuille)-set(liste_feuille_vivante))

transfert = open(sys.argv[1],"r")

transfert_donneur = []
transfert_receveur = []

for line in transfert:
	temp = line.split('\t')
	if (temp[1]=='T'):
		events = temp[2].split(";")
		transfert_donneur.append(events[2])
		transfert_receveur.append(events[4])


############################### transformer ces deux listes (donneur receveur) en donneur-receveur dans l'arbre réduit
new_transfert_donneur = []

for d in transfert_donneur:
	node = arbre_zombi&d
	leaves = [i.name for i in node]
	descornot = len(list(set(liste_feuille_vivante) & set(leaves)))
	while (descornot==0 and node.is_root()!=True):
		node=node.up
		leaves = [i.name for i in node]
		descornot = len(list(set(liste_feuille_vivante) & set(leaves)))
	if (descornot==1):
		new_transfert_donneur.append(list(set(liste_feuille_vivante) & set(leaves))[0])
	else:
		new_transfert_donneur.append(arbre_vivant.get_common_ancestor(list(set(liste_feuille_vivante) & set(leaves))).name)

new_transfert_receveur = []

for d in transfert_receveur:
	node = arbre_zombi&d
	leaves = [i.name for i in node]
	descornot = len(list(set(liste_feuille_vivante) & set(leaves)))
	if (descornot==0):
		new_transfert_receveur.append("none")
	elif (descornot==1):
		new_transfert_receveur.append(list(set(liste_feuille_vivante) & set(leaves))[0])
	else:
		new_transfert_receveur.append(arbre_vivant.get_common_ancestor(list(set(liste_feuille_vivante) & set(leaves))).name)

for k in range(len(new_transfert_donneur)):
    if (new_transfert_receveur[k]!="none"):
        transfert_zombi_donneur.append(new_transfert_donneur[k])
        transfert_zombi_receveur.append(new_transfert_receveur[k])

############################################################################### Correspondance des arbres #########################################################################

################## Remplissage du Dico ##################
for node_zombi in arbre_vivant.traverse("postorder"):
    if not node_zombi.is_leaf():
        dico_zombi[node_zombi.name] = sorted(node_zombi.get_leaf_names())

################## Mapping grace au Dico ##################
for node_ale in arbre_ale.traverse("postorder"):
    if not node_ale.is_leaf():
        name_zombi = recherche_inverse(dico_zombi,sorted(node_ale.get_leaf_names()))
        node_ale.add_feature( "name_zombi",name_zombi)
    else:
        node_ale.add_feature("name_zombi",node_ale.name)

############################################################################### Correspondance des transferts #########################################################################
################## lecture du fichier transfert de ALE ##################

lignes_ale = ale.readlines()

try:
    info = lignes_ale[1].split()

except:
    ################## fichier transfert ALE vide ##################
    VP_et_compagnie = open("VP_et_compagnie.txt", "a")
    ################## écriture résultats ##################
    VP_et_compagnie.write("numero du gene = " + str(nom_gene)+ " ; " +" VP = 0 " + " ; " + "FP = 0 " + " ; " + "FN = 0 " + "\n")
    exit()

################## Si fichier transfert Ale non vide ##################
del lignes_ale[0]
for i in lignes_ale:
    info = i.split()
    donneur_a = info[0].split("(")
    donneur_a = donneur_a[0]
    receveur_a = info[1].split("(")
    receveur_a = receveur_a[0]
    score.append(info[2])

    ################## vérification donneur ##################
    donneur_a = arbre_ale.search_nodes (name = donneur_a)[0]
    if(donneur_a.name_zombi):
        transfert_ale_donneur.append(donneur_a.name_zombi)
    else:
        transfert_ale_donneur.append(donneur_a.name)

    ################## vérification receveur ##################
    receveur_a = arbre_ale.search_nodes (name = receveur_a)[0]
    if (receveur_a.name_zombi):
        transfert_ale_receveur.append(receveur_a.name_zombi)
    else:
        transfert_ale_receveur.append(receveur_a.name)


################## compte du nombre d'occurence des prédictions sur les transferts zombi ##################
for i in range(len(transfert_zombi_donneur)):
    cle = str(transfert_zombi_donneur[i]) + "-" + str(transfert_zombi_receveur[i] )
    if (cle in occurence):
        occurence[cle]+=1
    else:
        occurence[cle]=1

################## vérification bon ou mauvais transfert ##################

for i in range(len(transfert_zombi_donneur)):
    for j in range(len(transfert_ale_donneur)):
        if (transfert_zombi_donneur[i] == transfert_ale_donneur[j] and transfert_zombi_receveur[i] == transfert_ale_receveur[j]) :
            cle = str(transfert_zombi_donneur[i]) + "-" + str(transfert_zombi_receveur[i])
            dico_infere[j] = occurence[cle]


################## Calcul des VP, FN et FP ##################

for k in range(len(score)):

    if (k in dico_infere) :
        vp = vp + float(score[k])

        fn = fn + (float(dico_infere[k]) - float(score[k]))
    else:
        fp = fp + float(score[k])


################## écriture résultats ##################

VP_et_compagnie = open("VP_et_compagnie.txt", "a")

VP_et_compagnie.write("numero du gene = " + str(nom_gene)+ " ; " +" VP = " + str(vp)  + " ; " + "FP = "+ str(fp) + " ; " + "FN =  " + str(fn) + "\n")
