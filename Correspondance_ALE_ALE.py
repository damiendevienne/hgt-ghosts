#!/usr/bin/python3
###############
########### Utilisation
########### Python3 Correspondance_ALE_ALE.py [uts prune] [numero de gene]
########### a besoin pour fonctionner du fichier new_transfert obtenua l'aide de prediction_ale.py
###############
############################################################################### Importation #########################################################################

from ete3 import Tree
import argparse
import sys


############################################################################### Déclaration #########################################################################

ale_1 = open("new_transfert.txt","r")
ale_2 = open(sys.argv[1],"r")
sortie =  open("sortie.txt", "a") 
num_gene = sys.argv[2]

score_1 = []
score_2 = []

transfert_ale_1 = []
transfert_ale_2 = []
resume = []

############################################################################### Fonction #########################################################################

def recherche_inverse(dico, valeur):
    for k in dico:
        if dico[k] == valeur:
            return k
    raise LookupError()


############################################################################### Isolement donneur / receveur ######################################################
ligne_ale_1 = ale_1.readlines()
lignes_ale_2 = ale_2.readlines()
try:
    info = ligne_ale_1[1].split(" ")

except:
    
    try:
        info = lignes_ale_2[1].split()
    
    except:
        sortie.write(num_gene+";"+"null"+";"+"null"+";"+"0"+";"+"0"+"\n")
        exit()
    
    del lignes_ale_2[0]
    for i in lignes_ale_2:
        info = i.split()
        donneur_a = info[0].split("(")
        receveur_a = info[1].split("(")
        transfert_ale_2.append(donneur_a[0] + " - " + receveur_a[0])
        score = info[2].split()
        score_2.append(score[0])
    
    for j in range(len(transfert_ale_2)):
        sortie.write(num_gene+";"+"null"+";"+str(transfert_ale_2[j])+";"+"0"+";"+str(score_2[j])+"\n")
    
    exit()

for i in ligne_ale_1:
    info = i.split(" ")
    transfert_ale_1.append(info[0]+" - "+info[2])
    score = info[4].split()
    score_1.append(score[0])
       
############################################################################### Lecture fichier ALE #########################################################################
try: 
    info = lignes_ale_2[1].split()

except: 
    for i in range(len(transfert_ale_1)):
        sortie.write(num_gene+";"+str(transfert_ale_1[i])+";"+"null"+";"+str(score_1[i])+";"+"0"+"\n")
    exit()

################## Si fichier transfert Ale non vide ##################
del lignes_ale_2[0]
for i in lignes_ale_2:
    info = i.split()
    donneur_a = info[0].split("(")
    receveur_a = info[1].split("(")
    transfert_ale_2.append(donneur_a[0] + " - " + receveur_a[0])
    score = info[2].split()
    score_2.append(score[0])
        
################## vérification correspondance transfert ##################
for i in range(len(transfert_ale_1)):
    for j in range(len(transfert_ale_2)):
        if transfert_ale_1[i]==transfert_ale_2[j]:
            resume.append(transfert_ale_1[i] + ";" + transfert_ale_2[j]+";"+score_1[i]+";"+score_2[j])

for i in range(len(transfert_ale_1)):
    if transfert_ale_1[i] not in transfert_ale_2:
        resume.append(transfert_ale_1[i]+";"+"null"+";"+score_1[i]+";"+"0")

for i in range(len(transfert_ale_2)):
    if transfert_ale_2[i] not in transfert_ale_1:
        resume.append("null"+";"+transfert_ale_2[i]+";"+"0"+";"+score_2[i])

############################################################################### Ecriture #########################################################################
for i in range(len(resume)):
	sortie.write(num_gene+";"+str(resume[i])+"\n")
