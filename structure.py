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

def get_transition_etat(automate,etat):
    """ récupère chaque transitions possible d'un état en fonction des mots
    pour l utiliser dans l'affichage sous la forme d'un tableau"""
    alpha = {}
    for word in automate.alphabet:
        alpha[word]=[]
    for transition in automate.transitions:

        if transition[0]==etat:
            alpha[transition[1]].append(transition[2])
    return alpha

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

def est_deterministe(automate):
    """
    Vérifie si l'automate est déterministe :
    - Un automate est déterministe si chaque état a au plus une transition par symbole.
    """
    if len(automate.initiaux) != 1:
        return False
    
    dict_transitions = {}
    for depart, symbole, arrivee in automate.transitions:
        if (depart, symbole) in dict_transitions:
            return False
        dict_transitions[(depart, symbole)] = arrivee
    return True

def est_complet(automate):
    """
    Vérifie si l'automate est complet :
    - Un automate est complet si chaque état a une transition pour chaque symbole de l'alphabet.
    """
    for etat in automate.etats:
        for symbole in automate.alphabet:
            transition_trouvee = False
            for depart, sym, arrivee in automate.transitions:
                if depart == etat and sym == symbole:
                    transition_trouvee = True
                    break
            if not transition_trouvee:
                return False
    return True


def est_standard(automate):
    """
    Vérifie si l'automate est standard :
    - Un automate est standard s'il a un unique état initial.
    - Il ne doit y avoir aucune transition aboutissant à cet état initial.
    """
    if len(automate.initiaux) != 1:
        return False
    
    etat_initial = automate.initiaux[0]
    for depart, symbole, arrivee in automate.transitions:
        if arrivee == etat_initial:
            return False
    return True

def est_reconnu(automate, mot):
    """
    Vérifie si un mot est reconnu par l'automate.
    """
    etat_courant = automate.initiaux[0]
    if len(automate.transitions) < 1:
        return True
    for lettre in mot:
        trouve = False
        for depart, symbole, arrivee in automate.transitions:
            if depart == etat_courant and symbole == lettre:
                etat_courant = arrivee
                trouve = True
                break
        if not trouve:
            return False  # Aucune transition valide, le mot est rejeté

    return etat_courant in automate.terminaux  # Vérifie si on termine dans un état final


def standardiser(automate):
    """
    Standardise l'automate si il ne l'est pas déjà:
    - Ajoute un état initial unique "I" et une transition epsilon de "I" vers chaque état initial auparavant.
    """
    if est_standard(automate)==False:
        if est_complet(automate)==False:
            if "&" not in automate.alphabet:
                automate.alphabet.append("&")
            for etat in automate.initiaux:
                automate.transitions.append(("I","&",etat))
            automate.initiaux = ["I"]
            automate.etats.insert(0,"I")
        else:
            if "&" not in automate.alphabet:
                automate.alphabet.append("&")
            for etat in automate.initiaux:
                automate.transitions.append(("I","&",etat))
            automate.initiaux = ["I"]
            automate.etats.insert(0,"I")
            complet(automate)
        cloture_epsilone(automate)

def complet(automate):
    """Complète un automate si il ne l'est pas:
    rajoute des états poubelles dans les transitions vides"""
    if est_complet(automate)==False:
        for etat in automate.etats:
            for word in automate.alphabet:
                if get_transition_etat(automate,etat)[word]==[]:
                    automate.transitions.append((etat,word,"P"))
        if "P" not in automate.etats:
            automate.etats.append("P")
            for word in automate.alphabet:
                automate.transitions.append(("P",word,"P"))
        cloture_epsilone(automate)

def new_name(list):
    """Génére le nom d'un nouvel état en fonction
    des états qui le constitue
    cela sert pour renommer les états suite à la déterminisation"""
    s = ""
    for l in list:
        s+=l+" "
    return s

def meme_etat(etats_in,new_etat):
    """renvoie si le nouvel état est consitué des mêmes états précédemment créer avec la détermination
    """
    for etat in etats_in.keys():
        if set(etats_in[etat])==set(new_etat):
            return True
    return False

def determiniser(automate):
    """
    déterminise l'automate si il ne l'est pas que ce soit avec ou sans epsilone:
    -#1 Initialise des nouveaux états vide
    -#2 à partir de l'état initiale déterminisé, établie tous les états possibles en fonction de chaque mot
    et réalise la même tache pour les états futurs possibles d'où la boucle while
    -#3 Pour chaque état présent dans le nouvel état créér, établie des liens vers des nouveaux états
    -#4 Recherche dans les états équivalent à chaque cloture epsilone pour établir des liens vers des nouveaux états
    (Rq: la cloture epsilone est équivalent à chaques états possibles si il n'y a pas de lien epsilone entre les états)
    -#5 regarde si la nouvelle transition à partir des clotures epsilones est présent dans les états terminaux d'avant,
    pour définir cet état futur comme terminaux ou non
    -#6 à la fin des transitions établie par l'état précédent, établie un nouvelle état à partir des transitions effectués sinon établie un état Poubelle
    -#7 Accorde les nouveaux états à l'automate actuel

    """
    #1
    new_etats = []
    etats_in = {}
    new_transitions = []
    new_terminaux = []
    new_etats.append(new_name(automate.initiaux))
    etats_in[new_etats[0]] = automate.initiaux
    #enlève le mot epsilone car il n'a pas d'intéret dans l'execution du programme
    if "&"in automate.alphabet:
        automate.alphabet.remove("&")
    i = 0
    #2
    while i < len(new_etats) or i == 0:
        for word in automate.alphabet:
            new = []
            est_terminal = False
            #3
            for etat in etats_in[new_etats[i]]:
                #4
                for etat2 in automate.cloture[etat]:
                    for transition in automate.transitions:
                        if transition[0]==etat2 and transition[1]==word and transition[2]not in new and transition[2]!="P":
                            new.append(transition[2])
                            #5
                            for etat3 in automate.cloture[transition[2]]:
                                if etat3 in automate.terminaux:
                                    est_terminal = True
            #6
            if new!=[]:
                id = new_name(new)
                if meme_etat(etats_in,new)==False:
                    new_etats.append(id)
                    etats_in[id] = new
                    if est_terminal:
                        new_terminaux.append(id)

            else:
                id="P"
                if id not in etats_in.keys():
                    new_etats.append(id)
                    etats_in["P"]=["P"]
                    automate.cloture["P"]=["P"]


            new_transitions.append((new_etats[i], word, id))
        i+=1
    #7
    automate.etats = new_etats
    automate.transitions = new_transitions
    automate.initiaux = [new_etats[0]]
    automate.terminaux = new_terminaux
    cloture_epsilone(automate)


def complementaire(automate):
    """Permet de rendre un automate complémentaire
    -il le déterminise si ce n'est pas fait
    -POur chaque états si ils sont terminaux ils sont retirés de la liste des états terminaux
    à l'inverse ils sont rajoutés dans la liste des états terminaux"""
    if est_deterministe(automate)==False:
        determiniser(automate)
    for etat in automate.etats:
        if etat in automate.terminaux:
            automate.terminaux.remove(etat)
        elif etat not in automate.terminaux:
            automate.terminaux.append(etat)


def cloture_epsilone(automate):
    """Etablie les clotures epsilones d'un automate:
    -#1 intialise le dictionnaire où sera stocké les états initiaux en tant que clé avec des dictionnaires vides
    -#2 initialise les autres clés du dictionnaire si elles sont reliés par un mot différent d'epsilones
    -#3 initialise tous les états auquel à accès la clé cloture si ils sont reliés par epsilone "&"
    """
    #1
    automate.cloture = {}
    for input in automate.initiaux:
        automate.cloture[input] = [input]
    #2
    for etat in automate.etats:
        for transition in automate.transitions:
            if transition[2]==etat and transition[1]!="&" :
                automate.cloture[etat]=[etat]
                break
    #3
    for etat in automate.cloture.keys():
        for transition in automate.transitions:
            if transition[0]==etat and transition[1]=="&":
                automate.cloture[etat].append(transition[2])
        for transition in automate.transitions:
            for etat2 in automate.cloture[etat]:
                if transition[0]==etat2 and transition[1]=="&" and transition[2]not in automate.cloture[etat]:
                    automate.cloture[etat].append(transition[2])

def get_terminal(etat,word,automate):
    """Etudie les transitions d'un automate
    afin de savoir si la sortie en fonction de l'état et du mot choisi est terminal(T) ou non (N)
    pour établir par la suite l'archétype de l'état"""
    for transition in automate.transitions:
        if transition[0]==etat and transition[1]==word and transition[2] in automate.terminaux:
            return "T "
    return "N "

def est_minimal(automate):
    if est_deterministe(automate):
        return False
    etats_t = {}
    etats_n = {}

    for etat in automate.cloture.keys():
        statement = ""

        for word in automate.alphabet:
            statement += (get_terminal(etat, word, automate))

        if etat in automate.terminaux:
            if statement in etats_t.keys():
                return False
            else:
                etats_t[statement] = [etat]
        else:
            if statement in etats_n.keys():
                return False
            else:
                etats_n[statement] = [etat]
    return True

def minimiser(automate):
    """
    Minimise un automate si il n'est pas minimisé
    -#1 déterminise l'automate et initialise 2 dictionnaires terminal/non terminal
    -#2 donne l'archétype de chaque sortie en fonction de chaque mot possible pour chaque état terminal et non terminal distinct
    -#3 si l'archétype de l'état est similaire il ajoute l'état actuel à la liste d'état de la clé correspondante à l'archétype
    sinon il crée une nouvelle clé avec cet archétype (pour les états terminaux et non terminaux séparément)
    -#4 défini les nouveaux états par des nouveaux index à partir de 0 et montant de 1 en 1 en fonction des états mis en correspondance
    avec les archétypes vu avant (pour les états terminaux et non terminaux séparément)
    -#5 Avec les nouveaux états établis, regarde si ils sont terminaux ou non à partir de la composition de leur états d'avants
    -#6 Réalise les nouvelles transitions entre les nouveaux états à partir de la composition et des relations de leur états d'avants
    -#7 établie les nouvelles valeurs à l'automate actuel
    """
    #1
    determiniser(automate)
    etats_t = {}
    etats_n = {}

    for etat in automate.cloture.keys():
        statement = ""
        #2
        for word in automate.alphabet:
            statement += (get_terminal(etat, word, automate))
        #3
        if etat in automate.terminaux:
            if statement in etats_t.keys():
                etats_t[statement].append(etat)
            else:
                etats_t[statement] = [etat]
        else:
            if statement in etats_n.keys():
                etats_n[statement].append(etat)
            else:
                etats_n[statement] = [etat]

    #print(etats_t, "---", etats_n)



    etats_in = {}
    new_initiaux = []
    new_terminaux = []
    new_transitions = []
    #4
    i=0
    for key in etats_t.keys():
        etats_in[str(i)]=etats_t[key]
        for etat in etats_t[key]:
            if etat in automate.initiaux:
                new_initiaux.append(str(i))
            if etat in automate.terminaux:
                new_terminaux.append(str(i))
        i+=1
    #5
    for key in etats_n.keys():
        etats_in[str(i)]=etats_n[key]
        for etat in etats_n[key]:
            if etat in automate.initiaux:
                new_initiaux.append(str(i))
            if etat in automate.terminaux:
                new_terminaux.append(str(i))
        i+=1
    #6
    for transition in automate.transitions:
        for etat in etats_in.keys():
            for etat2 in etats_in.keys():
                if transition[0]in etats_in[etat] and transition[2] in etats_in[etat2]and (etat,transition[1],etat2) not in new_transitions:

                    new_transitions.append((etat,transition[1],etat2))
    #7
    automate.transitions = new_transitions
    automate.etats = etats_in.keys()
    automate.initiaux = new_initiaux
    automate.terminaux = new_terminaux
    cloture_epsilone(automate)