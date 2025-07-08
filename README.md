# Web Scraping de classement de Top 14 et de Pro D2
Ce projet codé avec Python, majoritairement pendant l'été 2024, permet de scraper le [site Web de la LNR](https://top14.lnr.fr/) afin de faire des statistiques sur l'évolution des classements au fil des journées.
## Ethique
Pour éviter de surmener les serveurs de la ligue, toutes les pages déjà scrapées sont enregistrées et ne sont plus re-scrapées.
## Prérequis
Pour utiliser ce projet, il faut avoir Python et installer (via pip) les bibliothèques ci-dessous :
- tqdm
- matplotlib
- beautifulsoup4
- requests
## Installation et configuration
Pour installer et configurer le projet, il faut tout d'abord télécharger le code source de celui-ci.

Ensuite, il faut installer les dépendances dans Python 3 (celles-ci sont détaillées dans **requirements.txt** et ci-dessus).

Aucune configuration supplémentaire est nécessaire pour ce projet.
## Utilisation
L'utilisation de ce projet se fait exclusivement via le terminal, voici les étapes à suivre :
1. Exécutez le fichier main.py
2. Entrez le numéro de la division que vous souhaitez scraper (1 pour Top 14 et 2 pour Pro D2)
3. Si on vous le demande, entrez le numéro de la dernière journée terminée (A noter que vous pouvez retrouver cette information directement sur le [site Web de la LNR](https://top14.lnr.fr/)).
4. Attendre. Le temps d'attente peut varier et dure maximum quelques courtes minutes (selon si vous avez déjà scrapé cette saison de rugby).
