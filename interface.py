import tkinter as tk
from tkinter import messagebox
from structure import *

# Variable globale pour stocker l'automate actuel
automate_actuel = None

def voir_automate():
    global automate_actuel
    try:
        automate_actuel = quel_automate()        
        deterministe = est_deterministe(automate_actuel)
        standard = est_standard(automate_actuel)
        complet = est_complet(automate_actuel)
        
        if deterministe:
            resultats = "Deterministe ? Oui\n"
            button_determiniser.pack_forget()
        else:
            resultats = "Deterministe ? Non\n"
            button_determiniser.pack(side=tk.LEFT, padx=5)

        if standard:
            resultats += "Standard ? Oui\n"
            button_completer.pack_forget()
        else:
            resultats += "Standard ? Non\n"
            button_standardiser.pack(side=tk.LEFT, padx=5)

        if complet:
            resultats += "Complet ? Oui\n"
            button_standardiser.pack_forget()
        else:
            resultats += "Complet ? Non\n"
            button_completer.pack(side=tk.LEFT, padx=5)       

        if est_minimal(automate_actuel):
            button_minimiser.pack_forget()
        else:
            button_minimiser.pack(side=tk.LEFT, padx=5) 

        resultats += "\n" + afficher_tableau_automate(automate_actuel)
        text_result.delete(1.0, tk.END)
        text_result.insert(tk.END, resultats)

        button_complementaire.pack(side=tk.LEFT, padx=5)
        entry_word.pack(pady=1)
        button_estreconnu.pack(side=tk.LEFT, padx=1)
    except ValueError as e:
        messagebox.showerror("Erreur", str(e))

def quel_automate():
    try:
        numero = int(entry.get())
        if numero < 1 or numero > 44:
            raise ValueError("Le numéro doit être entre 1 et 44.")
        nom_fichier = f"automate_{numero}.txt"
        automate = lire_automate_depuis_fichier(nom_fichier)
        return automate
    except ValueError:
        raise ValueError("Le numéro doit être un entier entre 1 et 44.")

def determinisation():
    global automate_actuel
    if est_deterministe(automate_actuel):
        return
    determiniser(automate_actuel)
    afficher_resultats(automate_actuel)

def completer():
    global automate_actuel
    complet(automate_actuel)
    afficher_resultats(automate_actuel)

def standardiser_automate():
    global automate_actuel
    standardiser(automate_actuel)
    afficher_resultats(automate_actuel)

def complementariser():
    global automate_actuel
    complementaire(automate_actuel)
    afficher_resultats(automate_actuel)

def verifier_mot():
    global automate_actuel
    mot = entry_word.get()
    if est_reconnu(automate_actuel, mot):
        messagebox.showinfo("Mot reconnu", "Le mot est reconnu par l'automate.")
    else:
        messagebox.showinfo("Mot non reconnu", "Le mot n'est pas reconnu par l'automate.")

def minimisation():
    global automate_actuel
    if est_minimal(automate_actuel):
        return
    minimiser(automate_actuel)
    afficher_resultats(automate_actuel)

def afficher_resultats(automate):
    deterministe = est_deterministe(automate)
    standard = est_standard(automate)
    complet = est_complet(automate)
    
    resultats = "Deterministe ? " + ("Oui" if deterministe else "Non") + "\n"
    resultats += "Standard ? " + ("Oui" if standard else "Non") + "\n"
    resultats += "Complet ? " + ("Oui" if complet else "Non") + "\n"

    resultats += "\n" + afficher_tableau_automate(automate)
    text_result.delete(1.0, tk.END)
    text_result.insert(tk.END, resultats)

        # Gestion de l'affichage des boutons
    if deterministe:
        button_determiniser.pack_forget()
    else:
        button_determiniser.pack(side=tk.LEFT, padx=5)
    
    if standard:
        button_standardiser.pack_forget()
    else:
        button_standardiser.pack(side=tk.LEFT, padx=5)
    
    if complet:
        button_completer.pack_forget()
    else:
        button_completer.pack(side=tk.LEFT, padx=5)
    
    if est_minimal(automate):
        button_minimiser.pack_forget()
    else:
        button_minimiser.pack(side=tk.LEFT, padx=5)

# Création de la fenêtre principale
root = tk.Tk()
root.title("Vérification d'Automate")

# Création des widgets
label = tk.Label(root, text="Entrez le numéro de l'automate (1-44) :")
label.pack(pady=10)

entry = tk.Entry(root)
entry.pack(pady=5)

button_verifier = tk.Button(root, text="Vérifier", command=voir_automate)
button_verifier.pack(pady=20)
entry.bind('<Return>', lambda event: voir_automate())

entry_word = tk.Entry(root, width=50)
entry_word.pack_forget()
button_estreconnu = tk.Button(root, text="Est reconnu?", command=verifier_mot)
button_estreconnu.pack_forget()

text_result = tk.Text(root, height=30, width=190)
text_result.pack(pady=10)

# Création d'un frame pour les boutons
frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=20)

button_determiniser = tk.Button(frame_buttons, text="Déterminiser", command=determinisation)
button_completer = tk.Button(frame_buttons, text="Compléter", command=completer)
button_standardiser = tk.Button(frame_buttons, text="Standardiser", command=standardiser_automate)
button_complementaire = tk.Button(frame_buttons, text="Complémentaire", command=complementariser)
button_minimiser = tk.Button(frame_buttons, text="Minimiser", command=minimisation)
valeur=100
# Lancement de la boucle principale
root.mainloop()