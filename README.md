# hgt-ghosts
Stage Syrine Benali 

Dans ce git est présent les scripts que j'ai implémenté et utilisé durant mon stage.
Afin de correctement les utiliser il faut savoir que correspondance_ALE_ALE est dépendant de prediction_ALE, il en va de meme pour Correspondance_ALE_zombi et prediction_zombi. Il faut impérativement lancer le premier si l'on veux que le second fonctionne. Calcul_matrice_score est quant à lui indépendant.

Calcul_matrice_score permet d'obtenir les VP, FP et FN suite a une simulation zombi et une inférence de ALE. Il donne en sortie les valeurs de chacun pour le gene complet.

Correspondance_ALE_zombi et prediction_zombi permettent de prédire ce que vont devenir les transferts zombi suite a un échantillonnage et indique en fichier de sortie quel sont les transferts zombi qui ont été inféré par ALE, ceux qui ont disparu et ceux que ALE a inféré mais qui n'ont pas été simulé.

Correspondance_ALE_ALE et prédiction_ALE permettent, quand il y a eu deux inférence ALE (une avant et l'autre après échantillonnage), de savoir quel sont les transferts conservé d'un inférence a l'autre. Pour cela il prend les premier résultats d'inférence et fait un prédiction de ce qu'il vont devenir suite a un échantillonnage. Puis il compare ces prédictions aux résultats de la seconde inférence. il donne en sortie les transfert qui se correspondent ainsi que leur score respectif, les transfert qui ont disparu et les transferrts qui sont apparu avec la seconde inférence.

Les fichiers necessaire au bon fonctionnement des scripts sont indiqué en début de chacun d'eux. 

J'ai également implémenter un script bash qui montre la facon dont je les ai utilisé. il peut servir d'exemple pour leur bon fonctionnement.
