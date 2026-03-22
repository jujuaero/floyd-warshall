import os
import re
from copy import deepcopy

class Graphe:
    """
    Structure de données pour représenter un graphe orienté valué.
    Utilise une matrice d'adjacence pour le stockage.
    """
    def __init__(self):
        self.nb_sommet = 0
        self.nb_arrete = 0
        self.matrice = []  # Matrice d'adjacence [i][j] = poids de i à j (inf si pas d'arc)
        self.next_matrice = []  # Matrice de suivi des chemins pour Floyd-Warshall
    
    @staticmethod
    def lire_graphe_depuis_fichier(nom_fichier):
        """
        Charge un graphe depuis un fichier texte.
        
        Format:
        Ligne 1: nombre de sommets
        Ligne 2: nombre d'arcs
        Lignes suivantes: depart arrivee poids
        
        """
        graphe = Graphe()
        chemin_fichier = os.path.join("graphes", nom_fichier)

        with open(chemin_fichier, 'r', encoding='utf-8-sig') as f:
            lignes = [ligne.strip() for ligne in f.readlines() if ligne.strip()]

        graphe.nb_sommet = int(lignes[0])
        graphe.nb_arrete = int(lignes[1])

        # Initialiser matrice avec l'infini partout, 0 sur la diagonale
        graphe.matrice = [[float('inf')] * graphe.nb_sommet for _ in range(graphe.nb_sommet)]
        for i in range(graphe.nb_sommet):
            graphe.matrice[i][i] = 0

        # Remplir la matrice avec les arcs au format: depart arrivee poids
        for ligne in lignes[2:]:
            depart, arrivee, poids = map(int, ligne.split())
            graphe.matrice[depart][arrivee] = poids
        
        return graphe
    
    def afficher_matrice_formatee(self, matrice=None, titre="Matrice d'adjacence"):
        """
        Affiche une matrice de manière lisible avec titres et alignement.
        
        Args:
            matrice: matrice à afficher (None = utilise self.matrice)
            titre: titre à afficher
            
        Returns:
            str: représentation formatée de la matrice
        """
        if matrice is None:
            matrice = self.matrice
        
        resultat = f"\n{titre}\n"
        resultat += "=" * 80 + "\n"
        
        # Trouver la largeur maximale pour l'alignement
        largeur_max = 6  # minimum
        for i in range(len(matrice)):
            for j in range(len(matrice[0])):
                val = matrice[i][j]
                if val == float('inf'):
                    s = "∞"
                elif val == float('-inf'):
                    s = "-∞"
                else:
                    s = str(int(val))
                largeur_max = max(largeur_max, len(s))
        
        largeur = largeur_max + 1
        
        # En-tête avec indices des colonnes
        entete = "  K |"
        for j in range(self.nb_sommet):
            entete += f"{j:>{largeur}}"
        resultat += entete + "\n"
        resultat += "-" * len(entete) + "\n"
        
        # Lignes de la matrice
        for i in range(len(matrice)):
            ligne = f" {i}  |"
            for j in range(len(matrice[0])):
                val = matrice[i][j]
                if val == float('inf'):
                    s = "∞"
                elif val == float('-inf'):
                    s = "-∞"
                else:
                    s = str(int(val))
                ligne += f"{s:>{largeur}}"
            resultat += ligne + "\n"
        
        resultat += "=" * 80
        return resultat
    
    def afficher_matrice_next_formatee(self, matrice_next=None, titre="Matrice Next (chemins)"):
        """
        Affiche la matrice 'next' de manière lisible.
        Contient les indices du prochain sommet sur le chemin optimal.
        
        Args:
            titre: titre à afficher
            
        Returns:
            str: représentation formatée de la matrice next
        """
        if matrice_next is None:
            matrice_next = self.next_matrice

        if not matrice_next:
            return ""
        
        resultat = f"\n{titre}\n"
        resultat += "=" * 80 + "\n"
        
        largeur = 6
        
        # En-tête
        entete = "  K |"
        for j in range(self.nb_sommet):
            entete += f"{j:>{largeur}}"
        resultat += entete + "\n"
        resultat += "-" * len(entete) + "\n"
        
        # Lignes
        for i in range(len(matrice_next)):
            ligne = f" {i}  |"
            for j in range(len(matrice_next[0])):
                val = matrice_next[i][j]
                if val is None:
                    s = "-"
                else:
                    s = str(val)
                ligne += f"{s:>{largeur}}"
            resultat += ligne + "\n"
        
        resultat += "=" * 80
        return resultat


def floyd_warshall(graphe):
    """
    Exécute l'algorithme de Floyd-Warshall sur le graphe.
    
    Args:
        graphe: objet Graphe à traiter
        
    Returns:
        tuple: (matrice_finale, liste_matrices_L_intermediaires, liste_matrices_P_intermediaires, liste_k_valides)
        - matrice_finale: matrice L finale après l'algorithme
        - liste_matrices_L_intermediaires: [L_0, L_1, ..., L_{n-1}] avant/après itérations
        - liste_matrices_P_intermediaires: [P_0, P_1, ..., P_{n-1}] avant/après itérations
        - liste_k_valides: indices k pour lesquels les matrices ont été sauvegardées
    """
    n = graphe.nb_sommet
    
    # Initialiser L et next
    L = deepcopy(graphe.matrice)
    next_matrice = [[None] * n for _ in range(n)]
    
    # Initialiser la matrice next: si arc direct, le prochain sommet est j
    for i in range(n):
        for j in range(n):
            if i != j and L[i][j] != float('inf'):
                next_matrice[i][j] = j
    
    # Sauvegarder matrices intermédiaires
    matrices_l_intermediaires = []
    matrices_p_intermediaires = []
    k_valides = []
    
    # L_0: avant la première itération
    matrices_l_intermediaires.append(deepcopy(L))
    matrices_p_intermediaires.append(deepcopy(next_matrice))
    k_valides.append(-1)  # -1 pour L_0 (avant toute itération)
    
    # Boucles de Floyd-Warshall
    for k in range(n):
        for i in range(n):
            for j in range(n):
                # Vérifier si passer par k améliore le chemin i->j
                if L[i][k] != float('inf') and L[k][j] != float('inf'):
                    nouveau_poids = L[i][k] + L[k][j]
                    if nouveau_poids < L[i][j]:
                        L[i][j] = nouveau_poids
                        next_matrice[i][j] = next_matrice[i][k]
        
        # Sauvegarder L_k après l'itération k
        matrices_l_intermediaires.append(deepcopy(L))
        matrices_p_intermediaires.append(deepcopy(next_matrice))
        k_valides.append(k)
    
    # Sauvegarder les matrices finales dans le graphe
    graphe.matrice = L  # Mettre à jour la matrice du graphe avec les distances minimales
    graphe.next_matrice = next_matrice
    
    return L, matrices_l_intermediaires, matrices_p_intermediaires, k_valides


def contient_circuit_absorbant(matrice_l):
    """
    Vérifie si le graphe contient au moins un circuit absorbant.
    Un circuit absorbant est un cycle de poids négatif.
    
    Args:
        matrice_l: matrice L après Floyd-Warshall
        
    Returns:
        bool: True si circuit absorbant détecté, False sinon
    """
    n = len(matrice_l)
    for i in range(n):
        if matrice_l[i][i] < 0:
            return True
    return False


def extraire_chemin(graphe, source, destination):
    """
    Extrait le chemin de poids minimal de source à destination.
    
    Args:
        graphe: objet Graphe (doit avoir next_matrice remplie par Floyd-Warshall)
        source: index du sommet source
        destination: index du sommet destination
        
    Returns:
        tuple: (chemin, distance)
        - chemin: liste des sommets du chemin (ex: [0, 2, 4, 5])
        - distance: poids total du chemin (inf si pas de chemin)
    """
    if not graphe.next_matrice:
        return None, float('inf')
    
    # Récupérer la matrice L finale
    L_final = graphe.matrice  # Supposé déjà mise à jour par Floyd-Warshall
    
    # Vérifier si chemin existe
    if L_final[source][destination] == float('inf'):
        return [], float('inf')
    
    chemin = [source]
    courant = source
    
    # Suivre les indices next jusqu'à destination
    while courant != destination:
        prochain = graphe.next_matrice[courant][destination]
        if prochain is None:
            return [], float('inf')  # Pas de chemin
        chemin.append(prochain)
        courant = prochain
    
    distance = L_final[source][destination]
    return chemin, distance


def formater_chemin(chemin, distance):
    """
    Formate l'affichage d'un chemin de manière lisible.
    
    Args:
        chemin: liste des sommets
        distance: poids du chemin
        
    Returns:
        str: représentation formatée du chemin
    """
    if not chemin or distance == float('inf'):
        return "Pas de chemin entre ces deux sommets."
    
    chemin_str = " → ".join(str(s) for s in chemin)
    return f"Chemin: {chemin_str}\nDistance: {distance}"