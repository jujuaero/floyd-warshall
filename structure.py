import os

class Automate:
    def __init__(self,):
        #liste de tous les mots possibles de l'automate
        self.alphabet = []
        #liste de tous les états présents dans l'automate
        self.etats = []
        #liste des états initiaux de l'automate
        self.initiaux = []
        #liste des états terminaux de l'automate
        self.terminaux = []
        # liste de tuples à 3 index pour indiquer l'état de départ-> le mot ->et l'état de sortie
        self.transitions = []
        #
        self.cloture = {}

def lire_automate_depuis_fichier(nom_fichier):
    """
    1ère ligne: liste des lettres de l'alphabet
    2ème ligne: liste des états
    3ème ligne: état initial
    4ème ligne: état terminal
    5ème ligne: transitions jusqu'a la fin du fichier
    """
    automate = Automate()
    chemin_fichier = os.path.join("automates", nom_fichier)
    with open(chemin_fichier, 'r') as f:
        lignes = [ligne.strip() for ligne in f.readlines()]
    if lignes[0]!='':
        automate.alphabet = list(map(str, lignes[0].split(',')))  # Alphabet sous forme de liste de lettres
    if lignes[1] != '':
        automate.etats = list(map(str, lignes[1].split(',')))  # Liste des états
    if lignes[2] != '':
        automate.initiaux = list(map(str, lignes[2].split(',')))  # Liste des états initiaux
    if lignes[3] != '':
        automate.terminaux = list(map(str, lignes[3].split(',')))  # Liste des états terminaux
    automate.transitions = []
    for ligne in lignes[4:]:  # Lire les transitions
        depart, symbole, arrivee = ligne.split(',')
        automate.transitions.append((str(depart), symbole, str(arrivee)))
    cloture_epsilone(automate)
    return automate

def afficher_automate(automate):
    """
    Affiche les informations de l'automate :
    - États
    - Alphabet
    - États initiaux et terminaux
    - Table des transitions
    """
    print("Etats:", automate.etats)
    print("Alphabet:", automate.alphabet)
    print("Etats initiaux:", automate.initiaux)
    print("Etats terminaux:", automate.terminaux)
    print("Transitions:")
    for depart, symbole, arrivee in automate.transitions:
        print(f"  {depart} --{symbole}--> {arrivee}")

def afficher_tableau_automate(automate):
    """Affiche sous la forme d'un tableau claire
    les transitions en fonction de chaque mots et les cardinalités de chaque état"""
    largeur = 14
    espace = ' '
    n_ES = 8
    n_etat = 10
    n_alpha = largeur * 2 * len(espace) + 4

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
    return "\n".join(result)