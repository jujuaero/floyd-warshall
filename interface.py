import tkinter as tk
from tkinter import messagebox, scrolledtext
from structure import *

# Variable globale pour stocker le graphe actuel
graphe_actuel = None
matrice_L_finale = None
matrices_L_intermediaires = None
matrices_P_intermediaires = None

def charger_graphe():
    """Charge un graphe depuis un fichier numéroté"""
    global graphe_actuel, matrice_L_finale, matrices_L_intermediaires, matrices_P_intermediaires
    
    try:
        numero = int(entry_numero.get())
        if numero < 1 or numero > 13:
            raise ValueError("Le numéro doit être compris entre 1 et 13.")
        
        nom_fichier = f"graphe{numero}.txt"
        graphe_actuel = Graphe.lire_graphe_depuis_fichier(nom_fichier)
        matrice_L_finale = None
        matrices_L_intermediaires = None
        matrices_P_intermediaires = None
        
        # Afficher le graphe chargé
        affichage = f"  Graphe {numero} chargé avec succès !\n"
        affichage += f"  Sommets: {graphe_actuel.nb_sommet}\n"
        affichage += f"  Arcs: {graphe_actuel.nb_arrete}\n"
        affichage += graphe_actuel.afficher_matrice_formatee(titre="Matrice d'adjacence du graphe")
        
        text_output.config(state=tk.NORMAL)
        text_output.delete(1.0, tk.END)
        text_output.insert(tk.END, affichage)
        text_output.config(state=tk.DISABLED)
        
        # Activer les boutons suivants
        button_fw.config(state=tk.NORMAL)
        button_nouveau.config(state=tk.NORMAL)
        
    except FileNotFoundError:
        messagebox.showerror("Erreur", f"Fichier 'graphe{numero}.txt' non trouvé dans le dossier 'graphes/'")
    except ValueError as e:
        messagebox.showerror("Erreur", f"Entrée invalide: {e}")
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors du chargement: {e}")


def executer_floyd_warshall():
    """Exécute l'algorithme de Floyd-Warshall"""
    global graphe_actuel, matrice_L_finale, matrices_L_intermediaires, matrices_P_intermediaires
    
    if graphe_actuel is None:
        messagebox.showwarning("Attention", "Veuillez d'abord charger un graphe.")
        return
    
    try:
        # Exécuter l'algorithme
        matrice_L_finale, matrices_L_intermediaires, matrices_P_intermediaires, k_valides = floyd_warshall(graphe_actuel)
        
        # Affichage des résultats
        affichage = "EXÉCUTION DE FLOYD-WARSHALL\n"
        affichage += "=" * 80 + "\n\n"
        
        # Afficher toutes les matrices intermédiaires
        for k, matrice_l, matrice_p in zip(k_valides, matrices_L_intermediaires, matrices_P_intermediaires):
            if k == -1:
                affichage += graphe_actuel.afficher_matrice_formatee(matrice_l, titre="L_0 (Initialisation)")
                affichage += "\n\n"
                affichage += graphe_actuel.afficher_matrice_next_formatee(matrice_p, titre="P_0 (Initialisation des chemins)")
            else:
                affichage += graphe_actuel.afficher_matrice_formatee(matrice_l, titre=f"L_{k} (Après itération k={k})")
                affichage += "\n\n"
                affichage += graphe_actuel.afficher_matrice_next_formatee(matrice_p, titre=f"P_{k} (Après itération k={k})")
            affichage += "\n\n"
        
        # Détection circuit absorbant
        affichage += "=" * 80 + "\n"
        circuits = contient_circuit_absorbant(matrice_L_finale)
        if circuits:
            affichage += "CIRCUIT ABSORBANT DÉTECTÉ !\n"
            affichage += "La matrice contient au moins une valeur négative sur la diagonale.\n"
            affichage += "Traitement ARRÊTÉ. Pas d'affichage de chemins.\n"
        else:
            affichage += "Pas de circuit absorbant détecté.\n"
            affichage += "Les chemins de valeur minimale peuvent être affichés.\n"
        
        text_output.config(state=tk.NORMAL)
        text_output.delete(1.0, tk.END)
        text_output.insert(tk.END, affichage)
        text_output.config(state=tk.DISABLED)
        
        # Activer boutons chemins
        if not circuits:
            button_chemin.config(state=tk.NORMAL)
        else:
            button_chemin.config(state=tk.DISABLED)
        
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors de l'exécution: {e}")


def afficher_chemin():
    """Affiche le chemin entre deux sommets"""
    global graphe_actuel, matrice_L_finale
    
    if graphe_actuel is None or matrice_L_finale is None:
        messagebox.showwarning("Attention", "Veuillez d'abord exécuter Floyd-Warshall.")
        return
    
    try:
        source = int(entry_source.get())
        destination = int(entry_destination.get())
        
        if not (0 <= source < graphe_actuel.nb_sommet):
            raise ValueError(f"Sommet source doit être entre 0 et {graphe_actuel.nb_sommet - 1}")
        if not (0 <= destination < graphe_actuel.nb_sommet):
            raise ValueError(f"Sommet destination doit être entre 0 et {graphe_actuel.nb_sommet - 1}")
        
        chemin, distance = extraire_chemin(graphe_actuel, source, destination)
        message = formater_chemin(chemin, distance)
        
        # Ajouter au texte existant
        texte_actuel = text_output.get(1.0, tk.END)
        nouvel_affichage = f"\n{'=' * 80}\nChemin de {source} à {destination}:\n{message}\n"
        
        text_output.config(state=tk.NORMAL)
        text_output.insert(tk.END, nouvel_affichage)
        text_output.config(state=tk.DISABLED)
        text_output.see(tk.END)
        
    except ValueError as e:
        messagebox.showerror("Erreur", f"Entrée invalide: {e}")
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur: {e}")


def nouveau_graphe():
    """Réinitialise pour charger un nouveau graphe"""
    global graphe_actuel, matrice_L_finale, matrices_L_intermediaires, matrices_P_intermediaires
    
    graphe_actuel = None
    matrice_L_finale = None
    matrices_L_intermediaires = None
    matrices_P_intermediaires = None
    
    entry_numero.delete(0, tk.END)
    entry_source.delete(0, tk.END)
    entry_destination.delete(0, tk.END)
    
    text_output.config(state=tk.NORMAL)
    text_output.delete(1.0, tk.END)
    text_output.insert(tk.END, "Prêt à charger un nouveau graphe.\nEntrez le numéro du graphe (ex: 1, 2, 3...)")
    text_output.config(state=tk.DISABLED)
    
    button_fw.config(state=tk.DISABLED)
    button_chemin.config(state=tk.DISABLED)
    button_numero.config(state=tk.NORMAL)


# ========== CRÉATION FENÊTRE PRINCIPALE ==========
root = tk.Tk()
root.title("Floyd-Warshall - Chemins minimaux")
root.geometry("1000x800")

# ========== FRAME CONTRÔLES ==========
frame_controls = tk.Frame(root, bg="#f0f0f0", pady=10)
frame_controls.pack(side=tk.TOP, fill=tk.X)

# Chargement de graphe
label_numero = tk.Label(frame_controls, text="Numéro graphe:", bg="#f0f0f0")
label_numero.pack(side=tk.LEFT, padx=5)

entry_numero = tk.Entry(frame_controls, width=10)
entry_numero.pack(side=tk.LEFT, padx=5)
entry_numero.bind('<Return>', lambda e: charger_graphe())

button_numero = tk.Button(frame_controls, text="Charger graphe", command=charger_graphe)
button_numero.pack(side=tk.LEFT, padx=5)

button_fw = tk.Button(frame_controls, text="Exécuter Floyd-Warshall", command=executer_floyd_warshall, state=tk.DISABLED)
button_fw.pack(side=tk.LEFT, padx=5)

button_nouveau = tk.Button(frame_controls, text="Nouveau graphe", command=nouveau_graphe, state=tk.DISABLED)
button_nouveau.pack(side=tk.LEFT, padx=5)

# ========== FRAME CHEMINS ==========
frame_chemin = tk.Frame(root, bg="#f0f0f0", pady=10)
frame_chemin.pack(side=tk.TOP, fill=tk.X)

label_src = tk.Label(frame_chemin, text="Chemin de:", bg="#f0f0f0")
label_src.pack(side=tk.LEFT, padx=5)

entry_source = tk.Entry(frame_chemin, width=5)
entry_source.pack(side=tk.LEFT, padx=5)

label_dst = tk.Label(frame_chemin, text="à:", bg="#f0f0f0")
label_dst.pack(side=tk.LEFT, padx=5)

entry_destination = tk.Entry(frame_chemin, width=5)
entry_destination.pack(side=tk.LEFT, padx=5)
entry_destination.bind('<Return>', lambda e: afficher_chemin())

button_chemin = tk.Button(frame_chemin, text="Afficher chemin", command=afficher_chemin, state=tk.DISABLED)
button_chemin.pack(side=tk.LEFT, padx=5)

# ========== TEXT OUTPUT ==========
text_output = scrolledtext.ScrolledText(root, height=30, width=120, font=("Courier", 9))
text_output.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
text_output.config(state=tk.DISABLED)

text_output.insert(tk.END, "Bienvenue dans le programme Floyd-Warshall !\n\nÉtapes:\n1. Entrez le numéro d'un graphe\n2. Cliquez sur 'Charger graphe'\n3. Cliquez sur 'Exécuter Floyd-Warshall'\n4. Affichage optionnel des chemins minimaux\n5. Chargez un nouveau graphe ou quittez")
text_output.config(state=tk.DISABLED)

# ========== LANCEMENT ==========
root.mainloop()