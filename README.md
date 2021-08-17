# hgt-ghosts
Stage Syrine Benali 

Dans ce git est présent les scripts que j'ai implémentés et utilisés durant mon stage.
Afin de correctement les utiliser il faut savoir que correspondance_ALE_ALE est dépendant de prediction_ALE, il en va de même pour Correspondance_ALE_zombi et prediction_zombi. Il faut impérativement lancer le premier si l'on veut que le second fonctionne. Calcul_matrice_score est quant à lui indépendant.

Calcul_matrice_score permet d'obtenir les Vrais Positifs (VP), Faux Positifs (FP) et Faux Négatifs (FN) suite à une simulation zombi et une inférence de ALE. Il donne en sortie les valeurs de chacun pour le gène complet.

Correspondance_ALE_zombi et prediction_zombi permettent de prédire ce que vont devenir les transferts zombi suite à un échantillonnage et indique en fichier de sortie quels sont les transferts zombi qui ont été inférés par ALE, ceux qui ont disparu et ceux que ALE a inféré mais qui n'ont pas été simulés.

Correspondance_ALE_ALE et prédiction_ALE permettent, quand il y a eu deux inférence ALE (une avant et l'autre après échantillonnage), de savoir quel sont les transferts conservés d'une inférence à l'autre. Pour cela il prend les premiers résultats d'inférence et fait une prédiction de ce qu'ils vont devenir suite à un échantillonnage. Puis il compare ces prédictions aux résultats de la seconde inférence. Il donne en sortie les transferts qui se correspondent ainsi que leurs scores respectifs, les transferts qui ont disparu et les transferts qui sont apparus avec la seconde inférence.

Les fichiers necessaire au bon fonctionnement des scripts sont indiqués en début de chacun d'eux. 

J'ai également implémenté un script bash qui montre la façon dont je les ai utilisés. Il peut servir d'exemple pour leur bon fonctionnement.
