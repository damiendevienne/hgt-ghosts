#!/bin/bash

if [ ! -d echant_5 ];then
echo "Création du dossier echant_5 !";
mkdir echant_5
fi

racine=Bureau/data_rhizo/echant_5
chemin=Bureau/data_rhizo

python3 ~/ZOMBI/SpeciesSampler.py n 93 ./$chemin

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
  cp clean.py ~/$racine/$compte
  cp spe3 ~/$racine/$compte

  cd ~/$chemin/T
  cp CompleteTree.nwk ~/$racine/$compte

  cd ~/$chemin/G/Gene_trees
  cp $compte"_prunedtree.nwk" ~/$racine/$compte

  cd ~/$chemin/G/Gene_families
  cp $compte"_events.tsv" ~/$racine/$compte

  cd ~/$chemin/SAMPLE_4
  cp $compte"_sampledtree.nwk" ~/$racine/$compte
  cp SampledSpeciesTree.nwk ~/$racine/$compte

####### on nettoie les arbres car ALE ne fonctionne pas si il y a le Root

  cd ~/$racine/$compte

  python3 clean.py $compte"_prunedtree.nwk" "Arbre_"$compte"_prunedtree.nwk"
  python3 clean.py CompleteTree.nwk Arbre_complet.nwk
  python3 clean.py $compte"_sampledtree.nwk"  "Arbre_"$compte"_sampledtree.nwk";
  python3 clean.py SampledSpeciesTree.nwk Arbre_sample.nwk

  rm CompleteTree.nwk
  mv Arbre_complet.nwk CompleteTree.nwk
  mv "Arbre_"$compte"_prunedtree.nwk" $compte"_prunedtree.nwk"

  rm SampledSpeciesTree.nwk
  mv Arbre_sample.nwk SampledSpeciesTree.nwk
  mv "Arbre_"$compte"_sampledtree.nwk" $compte"_sampledtree.nwk"


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

  cd ~/$racine
  python3 Prediction_ALE.py *_prunedtree.nwk.ale.uTs *_prunedtree.nwk.ale.spTree *_sampledtree.nwk.ale.spTree $compte

  python3 Correspondance_ALE_ALE.py *_sampledtree.nwk.ale.uTs $compte

  python3 Prediction_zombi.py *_events.tsv CompleteTree.nwk *_sampledtree.nwk.ale.spTree $compte

  python3 Correspondance_ALE_Zombi.py *_sampledtree.nwk.ale.uTs $compte SampledSpeciesTree.nwk *_sampledtree.nwk.ale.spTree

  python3 calcul_matrice_confusion.py *_events.tsv *_sampledtree.nwk.ale.uTs CompleteTree.nwk SampledSpeciesTree.nwk *_sampledtree.nwk.ale.spTree $compte

### on conserve les sortie correspondante au transfert prédits

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
zip -r echant_10.zip echant_10
rm -r echant_10
