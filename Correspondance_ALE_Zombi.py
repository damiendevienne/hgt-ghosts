#!/usr/bin/python3
###############
########### Utilisation
########### Python3 Correspondance_ALE_Zombi.py [uts prune] [arbre zombi prune] [arbre ale prune] [numero de gene]
########### a besoin pour fonctionner du fichier new_transfert obtenu l'aide de prediction_zombi.py
###############
############################################################################### Importation #########################################################################

from ete3 import Tree
import argparse
import sys


############################################################################### Déclaration #########################################################################
score_1 = []
score_2 = []

transfert_zombi = []
transfert_ale = []
resume = []

donneur_ale = []
receveur_ale = []
new_transfert_ale = []

sortie =  open("sortie_2.txt", "a") 

dico_zombi = dict()
ale = open(sys.argv[1],"r")
arbre_zombi= Tree(sys.argv[2] ,format=1)
arbre_ale = Tree(sys.argv[3] ,format=1)
num_gene = sys.argv[4]

zombi = open("new_transfert_2.txt","r")


############################################################################### Fonction #########################################################################

def recherche_inverse(dico, valeur):
    for k in dico:
        if dico[k] == valeur:
            return k
    raise LookupError()


############################################################################### Correspondance des arbres #########################################################################

################## Remplissage du Dico ##################
for node_zombi in arbre_zombi.traverse("postorder"):
    if not node_zombi.is_leaf():
        dico_zombi[node_zombi.name] = sorted(node_zombi.get_leaf_names())

################## Mapping grace au Dico ##################
for node_ale in arbre_ale.traverse("postorder"):
    if not node_ale.is_leaf():
        name_zombi = recherche_inverse(dico_zombi,sorted(node_ale.get_leaf_names()))
        node_ale.add_feature( "name_zombi",name_zombi)
    else:
        node_ale.add_feature("name_zombi",node_ale.name)


############################################################################### Lecture fichier ALE et transferts prédits ##############################################

ligne_zombi = zombi.readlines()
lignes_ale = ale.readlines()
try:
    info = ligne_zombi[1].split(" ")

except: #### si le fichier de transferts prédits est vide
    
    try:
        info = lignes_ale[1].split()
    
    except: ###### Si les deux fichier sont vide, il n'y a aucun transfert
        sortie.write(num_gene+";"+"null"+";"+"null"+";"+"0"+";"+"0"+"\n")
        exit()
    
    del lignes_ale[0]
    for i in lignes_ale:
        info = i.split()
        donneur_a = info[0].split("(")
        receveur_a = info[1].split("(")
        transfert_ale.append(donneur_a[0] + " - " + receveur_a[0])
        score = info[2].split()
        score_2.append(score[0])
    
    for j in range(len(transfert_ale)):
        sortie.write(num_gene+";"+"null"+";"+str(transfert_ale[j])+";"+"0"+";"+str(score_2[j])+"\n")
    
    exit()

#### Si le fichier contenant les transferts prédits n'est pas vide
for i in ligne_zombi:
    info = i.split(" ")
    transfert_zombi.append(info[0]+" - "+info[2])
    score = info[4].split()
    score_1.append(score[0])


del lignes_ale[0]
for i in lignes_ale:
    info = i.split()
    donneur_a = info[0].split("(")
    receveur_a = info[1].split("(")
    donneur_ale.append(donneur_a[0])
    receveur_ale.append(receveur_a[0])
    score = info[2].split()
    score_2.append(score[0])

############################################################################### Mapping des transferts #########################################################################


########### On récupère les noms zombi de nos transferts ALE #################
for i in range(len(donneur_ale)):

    new_donneur = arbre_ale.search_nodes(name = donneur_ale[i])[0]

    new_receveur = arbre_ale.search_nodes(name = receveur_ale[i])[0]

    new_transfert_ale.append(new_donneur.name_zombi + " - " + new_receveur.name_zombi)


        
################## vérification correspondance transfert ##################
for i in range(len(transfert_zombi)):
    for j in range(len(new_transfert_ale)):
        if transfert_zombi[i]==new_transfert_ale[j]:
            resume.append(transfert_zombi[i] + ";" + new_transfert_ale[j]+";"+score_1[i]+";"+score_2[j])

for i in range(len(transfert_zombi)):
    if transfert_zombi[i] not in new_transfert_ale:
        resume.append(transfert_zombi[i]+";"+"null"+";"+score_1[i]+";"+"0")

for i in range(len(new_transfert_ale)):
    if new_transfert_ale[i] not in transfert_zombi:
        resume.append("null"+";"+new_transfert_ale[i]+";"+"0"+";"+score_2[i])



############################################################################### Ecriture #########################################################################
for i in range(len(resume)):
	sortie.write(num_gene+";"+str(resume[i])+"\n")
