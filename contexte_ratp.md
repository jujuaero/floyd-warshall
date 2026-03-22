# Contexte d'application reelle : Reseau RATP / IDFM

## Problematique
L'objectif est de calculer les temps minimaux de trajet entre tous les couples de stations d'un sous-reseau du metro parisien, avec prise en compte des correspondances.

Dans un contexte d'aide au voyageur, cela permet de :
- repondre rapidement a toute requete origine-destination,
- identifier les zones les plus eloignees en temps,
- evaluer l'impact des correspondances sur les temps de trajet.

## Source de donnees ouverte (existante)
Donnees publiques Ile-de-France Mobilites :
- Horaires GTFS IDFM : https://data.iledefrance-mobilites.fr/explore/dataset/offre-horaires-tc-gtfs-idfm/
- Arrets et lignes associees : https://data.iledefrance-mobilites.fr/explore/dataset/arrets-lignes/
- Referentiel des lignes : https://data.iledefrance-mobilites.fr/explore/dataset/referentiel-des-lignes/

Le graphe fourni dans ce projet est une extraction pedagogique de ce contexte reel.

## Modelisation du graphe
- Sommet : une station
- Arc oriente : possibilite de deplacement d'une station vers une autre
- Poids : temps de trajet en minutes
- Correspondance : arc supplementaire de cout fixe (temps de marche + attente)

## Jeu de donnees fourni
Fichier : graphes/graphe14.txt
- 30 sommets
- 72 arcs orientes
- Lignes representees :
  - Axe type ligne 1
  - Axe type ligne 4
  - Axe type ligne 14
  - Arcs de correspondance entre hubs

## Table d'index des stations
0  La Defense
1  Charles de Gaulle - Etoile
2  George V
3  Franklin D. Roosevelt
4  Champs-Elysees Clemenceau
5  Concorde
6  Tuileries
7  Palais Royal - Musee du Louvre
8  Chatelet (L1)
9  Hotel de Ville
10 Bastille
11 Porte de Clignancourt
12 Simplon
13 Marcadet-Poissonniers
14 Gare du Nord
15 Strasbourg-Saint-Denis
16 Reaumur-Sebastopol
17 Chatelet (L4)
18 Cite
19 Saint-Michel
20 Saint-Denis Pleyel
21 Mairie de Saint-Ouen
22 Porte de Clichy
23 Saint-Lazare
24 Madeleine
25 Pyramides
26 Chatelet (L14)
27 Gare de Lyon
28 Bercy
29 Olympiades

## Interpretation attendue des resultats
- Matrices L : temps minimaux entre toutes les paires de stations
- Matrices P : structure des chemins minimaux (predecesseurs)
- Verification des circuits absorbants : non attendus ici
- Exemples de lectures metier :
  - temps minimal Bastille -> Saint-Lazare,
  - impact du hub Chatelet sur les plus courts chemins,
  - comparaison trajet direct vs trajet avec correspondance.
