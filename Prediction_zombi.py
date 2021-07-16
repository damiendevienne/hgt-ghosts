#!/usr/bin/python3
###############
########### Utilisation
########### Python3 prediction_zombi.py [events zombi] [arbre complet] [arbre prune] [numero de gene]
###########
###############
############################################################################### Importation #########################################################################
from ete3 import Tree
import argparse
import sys

############################################################################### Déclaration #########################################################################

transfert = open(sys.argv[1],"r")
arbre_zombi= Tree(sys.argv[2],format=1) #grand
arbre_vivant = Tree(sys.argv[3],format =1) #petit
num_gene = sys.argv[4]

liste = []

liste_feuille_vivante = [i.name for i in arbre_vivant]
liste_feuille = [i.name for i in arbre_zombi]
liste_morte = list(set(liste_feuille)-set(liste_feuille_vivante))

transfert_donneur = []
transfert_receveur = []

for line in transfert:
	temp = line.split('\t')
	if (temp[1]=='T'):
		events = temp[2].split(";")
		transfert_donneur.append(events[2])
		transfert_receveur.append(events[4])

############################################################################### Prediction #########################################################################
######## Pour prédire ce que vont devenir les transferts après échantillonnage nous cherchons si les donneurs disparus ont un ascendant vivant et différent du receveur. 
######## Pour les cas des receveurs nous cherchons si ils ont un descendant vivant et différent du donneur.

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

transfert_new = []

transfert_disparu = []

for k in range(len(new_transfert_donneur)):
	if (new_transfert_receveur[k]!="none"):
		transfert_new.append(new_transfert_donneur[k] + " - " + new_transfert_receveur[k]+ " - "+ "1")
	elif(new_transfert_receveur[k]=="none"):
		transfert_disparu.append( transfert_donneur[k] + " - " + transfert_receveur[k] + ";" + "null" + ";" + "1" + ";" + "0")

############################################################################### Elimination des doublons #########################################################################
############# On conserve un seule copie de chaque transfert

mes_transferts = []

for i in range(len(transfert_new)):
	for j in range(len(transfert_new)):
		if(i!=j):
			transfert_1 = transfert_new[i].split("-")
			transfert_2 = transfert_new[j].split("-")

			if (str(transfert_1[0]) == str(transfert_2[0]) and str(transfert_1[1])==str(transfert_2[1])):
				if (float(transfert_1[2])>float(transfert_2[2])):
					mes_transferts.append(transfert_new[i])
					liste.append(j)
					liste.append(i)
				elif(float(transfert_1[2])<float(transfert_2[2])):
					mes_transferts.append(transfert_new[j])
					liste.append(j)
					liste.append(i)



for i in range(len(transfert_new)):
	if i not in liste:
		mes_transferts.append(transfert_new[i])
		liste.append(i)


############################################################################### Ecriture #########################################################################
nouveau_transfert = open("new_transfert_2.txt","a")


transfert_new_final = list(set(mes_transferts))

for i in range(len(transfert_new_final)):
	nouveau_transfert.write(str(transfert_new_final[i])+"\n")

sortie =  open("sortie_2.txt", "a") 

for i in range(len(transfert_disparu)):
	sortie.write(num_gene+ ";" +str(transfert_disparu[i])+"\n")