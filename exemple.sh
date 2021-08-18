#!/bin/bash

#### Mes gènes sont rangés dans le dossier data_rhizo
#### Mes résulats seront placé dans le dossier dossier_resulats

if [ ! -d dossier_resultats ];then
echo "Création du dossier dossier_resulats !";
mkdir dossier_resulats
fi

racine=Bureau/data_rhizo/dossier_resulats
chemin=Bureau/data_rhizo

##### Fonctionne seulement si un arbre a déja été simulé grace à zombi
##### Si ce n'est pas le cas il faut utiliser les deux ligne ci dessous avec spe_tree l'arbre d'espece a partir du quel les arbre de gènes doivent etre simulé
####python3 ~/ZOMBI/Zombi.py Ti ~/$racine/spe_tree ./$racine
###python3 ~/ZOMBI/Zombi.py G ./ZOMBI/Parameters/GenomeParameters.tsv ./$racine

python3 ~/ZOMBI/SpeciesSampler.py n 93 ./$chemin ### le chiffre placé après le n correspond au nombre de feuille que l'on veut conserver après échantillonnage

cd ~/$chemin

compte=1
while (($compte !=101)) #### j'ai 100 gènes à analyser et ces dernier sont désigné par un nombre
do

  cd ~/$racine
  if [ ! -d $compte ];then
  echo "Création du dossier $compte !";
  mkdir $compte
  fi

  cd ~/$chemin

#### On copie tout les fichiers python ainsi que les fichier utile à leur utilisation vers le dossier contenant le gene d'interet

  cp Prediction_ALE.py ~/$racine
  cp Correspondance_ALE_ALE.py ~/$racine
  cp Prediction_zombi.py ~/$racine
  cp Correspondance_ALE_Zombi.py ~/$racine
  cp calcul_matrice_confusion.py ~/$racine
  cp spe3 ~/$racine/$compte

  cd ~/$chemin/T
  cp CompleteTree.nwk ~/$racine/$compte

  cd ~/$chemin/G/Gene_trees
  cp $compte"_prunedtree.nwk" ~/$racine/$compte

  cd ~/$chemin/G/Gene_families
  cp $compte"_events.tsv" ~/$racine/$compte

  cd ~/$chemin/SAMPLE_1 ## ici il s'agit du premier dossier obtenu avec la commande sample de zombi. il faut changer le numéro de dossier si on lance ce script plusieurs fois
  cp $compte"_sampledtree.nwk" ~/$racine/$compte
  cp SampledSpeciesTree.nwk ~/$racine/$compte

####### Il faut vérifier qu'il n'y a pas de noeud Root dans les arbres sinon ALE retournera une erreur

###### on lance ALE
  ALEobserve *_prunedtree.nwk
  ALEobserve *_sampledtree.nwk

  ALEml_undated CompleteTree.nwk $compte"_prunedtree.nwk.ale" sample=500 separator="_" output_species_tree=y ;

  ALEml_undated SampledSpeciesTree.nwk $compte"_sampledtree.nwk.ale"  sample=500 separator="_" output_species_tree=y;

### on récupère les sorties ALE qui nous interesse

  cp *_prunedtree.nwk.ale.uTs ~/$racine
  cp *_prunedtree.nwk.ale.spTree ~/$racine
  cp *_sampledtree.nwk.ale.spTree ~/$racine
  cp *_sampledtree.nwk.ale.uTs ~/$racine
  cp CompleteTree.nwk ~/$racine
  cp SampledSpeciesTree.nwk ~/$racine
  cp *_events.tsv ~/$racine

#### On lance les codes python. il faut tous les lancer dans un meme répertoire afin d'avoir les résultats de tout les genes dans un meme fichier

  cd ~/$racine ## il faut lancer les scripts python dans un même dossier car les résultats s'ecrivent sur un même fichier pour tout les gènes
  ### on replacera les fichiers propre à chaque gène dans le dossier avec le bon numero par la suite
  
  python3 Prediction_ALE.py *_prunedtree.nwk.ale.uTs *_prunedtree.nwk.ale.spTree *_sampledtree.nwk.ale.spTree $compte

  python3 Correspondance_ALE_ALE.py *_sampledtree.nwk.ale.uTs $compte

  python3 Prediction_zombi.py *_events.tsv CompleteTree.nwk *_sampledtree.nwk.ale.spTree $compte

  python3 Correspondance_ALE_Zombi.py *_sampledtree.nwk.ale.uTs $compte SampledSpeciesTree.nwk *_sampledtree.nwk.ale.spTree

  python3 calcul_matrice_confusion.py *_events.tsv *_sampledtree.nwk.ale.uTs CompleteTree.nwk SampledSpeciesTree.nwk *_sampledtree.nwk.ale.spTree $compte

### on conserve les sorties correspondantes aux transfert prédits

  cp new_transfert.txt ~/$racine/$compte
  cp new_transfert_2.txt ~/$racine/$compte

#### on supprime les fichiers qui sont propre au gènes afin de ne pas avoir de confusion pour le gène suivant
  rm new_transfert.txt
  rm *_prunedtree.nwk.ale.uTs
  rm *_prunedtree.nwk.ale.spTree
  rm *_sampledtree.nwk.ale.spTree
  rm *_sampledtree.nwk.ale.uTs
  rm CompleteTree.nwk
  rm SampledSpeciesTree.nwk
  rm *_events.tsv
  rm new_transfert_2.txt

  compte=`expr $compte + 1`
done

cd ~/$chemin
zip -r dossier_resulats.zip dossier_resulats
rm -r dossier_resulats
