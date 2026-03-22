## Nature du jeu de donnees
Le fichier `graphes/graphe15.txt` est une modelisation topologique du metro parisien, construit a partir de l'ordre reel des stations sur trois lignes :
- Metro ligne 1 (troncon Ouest-Centre-Est)
- Metro ligne 4 (troncon Nord-Centre-Sud)
- Metro ligne 14 (troncon Nord-Centre-Sud-Est)

Ce jeu de donnees est volontairement **topologique** :
- un arc = deux stations consecutives sur une ligne,
- poids = 1 (nombre de "sauts" de station),
- sens bidirectionnel (un arc par sens).

## Sources publiques
- Plan du reseau metro RATP / IDFM (topologie des lignes et ordre des stations)
- Open data IDFM (referentiels lignes/arrets) :
  - https://data.iledefrance-mobilites.fr/explore/dataset/referentiel-des-lignes/
  - https://data.iledefrance-mobilites.fr/explore/dataset/arrets-lignes/

## Hypotheses de modelisation
- Les stations de correspondance communes sont fusionnees en un seul sommet :
  - Chatelet (sommet 7)
  - Gare de Lyon (sommet 10)
- Les poids ne representent pas des minutes, mais un nombre de troncons.

## Table des sommets
0  La Defense
1  Charles de Gaulle - Etoile
2  George V
3  Franklin D. Roosevelt
4  Concorde
5  Tuileries
6  Palais Royal - Musee du Louvre
7  Chatelet
8  Hotel de Ville
9  Bastille
10 Gare de Lyon
11 Porte de Clignancourt
12 Simplon
13 Marcadet-Poissonniers
14 Gare du Nord
15 Strasbourg-Saint-Denis
16 Reaumur-Sebastopol
17 Cite
18 Saint-Michel
19 Saint-Denis Pleyel
20 Mairie de Saint-Ouen
21 Porte de Clichy
22 Saint-Lazare
23 Madeleine
24 Pyramides
25 Bercy
26 Olympiades
