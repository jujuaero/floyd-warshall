import os

class Graphe:
    def __init__(self,):
        """structure de nos graphes en matrice -> nb_sommet : nombre de sommets; nb_arrete : nombre d'arrete; arrete : def arrete"""
        self.nb_sommet = 0
        self.nb_arrete = 0
        self.arrete = []
        self.matrice = []
    def lire_graphe_depuis_fichier(nom_fichier):
        graphe = Graphe()
        chemin_fichier = os.path.join("graphes", nom_fichier)
        with open(chemin_fichier, 'r') as f:
            lignes = [ligne.strip() for ligne in f.readlines()]
        if lignes[0] !='':
            graphe.nb_sommet = int(lignes[0])  # nombre de sommets
        if lignes[1] != '':
            graphe.nb_arrete = int(lignes[1])  # nombre d'arretes
        for ligne in lignes[2:]:  # Lire les arretes
            depart, arrivee, poids = ligne.split(' ')
            graphe.arrete.append((depart,arrivee,poids))
        return graphe
    def afficher_tableau_graphe(graphe):
        """je veux que vous et dossier bleu sur une centaine de tableau tres clairs je clair luc ne pas je tellement sur vous"""
        graphe.matrice=[]
        for i in graphe.nb_sommet :
            for j in graphe.nb_sommet :
                graphe.matrice[i,j]='inf'
"""
        result = []
        header = "in/out |  Etat   |" + "".join([largeur * espace + elt + largeur * espace + "  |" for elt in automate.alphabet])
        result.append(header)

        for etat in automate.etats:
            ligne = ""
            words = get_transition_etat(automate, etat)

            if etat in automate.initiaux:
                ligne = " E"
            if etat in automate.terminaux:
                ligne += " S"
            ligne += espace * (n_ES - len(ligne) - 1) + "|" + etat
            ligne += espace * (n_ES + n_etat - len(ligne) - 1) + "|"

            for word in automate.alphabet:
                change = " "
                for elt in words[word]:
                    change += elt + ','
                ligne += change + espace * (n_alpha - len(change) - 1) + '|'
            result.append(ligne)
        return "\n".join(result)"""