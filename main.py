#!/usr/bin/env python3

# Imports de librairies
import os
from guizero import PushButton, Text, Window, CheckBox, App, Box
import matplotlib.pyplot as plt
from pandas_ods_reader import read_ods


# Imports de fichiers personnels
# from globalisation import *

# Fonction de comparaison de deux matrices
def comparaison_matricielle(to_compare, is_positif):
    # Séléction du comparant
    bit_stop = False
    theme = ""
    op_negatives = [
        ["voiture", "vélo", "velo", "train", "avion", "bateau", "bus", "navette",
         "navigo", "essence", "e10", "e5", "gazole", "b7", "péage", "peage"],
        ["tati"],
        ["courses", "nourriture"],
        ["loyer", "charges"]
    ]
    op_positives = [
        ["virement", "virements"],
        ["cheque", "cheques", "chèque", "chèques"]
    ]

    if (to_compare[1] == "’" and len(to_compare[1]) > 3):
        to_compare = to_compare[2:]
    else:
        pass

    if (is_positif == True):
        for a in range(len(op_positives)):
            for b in range(len(op_positives[a])):
                if (to_compare.lower() == op_positives[a][b].lower()):
                    theme = a + len(op_negatives)
                else:
                    pass
    else:
        for a in range(len(op_negatives)):
            for b in range(len(op_negatives[a])):
                if (to_compare.lower() == op_negatives[a][b].lower()):
                    theme = a
                else:
                    pass

    return theme



# Faire des statistiques sur les types d'opérations
def sujets_proportions(opérations, objet_opérations):
    themes_list = ["mobilités", "vêtements", "alimentaire",
        "logement", "virements", "dépôts", "autre"
    ]
    opérations_list = [0, 0, 0, 0, 0, 0, 0]
    for a in range(len(objet_opérations)):
        tmp = objet_opérations[a].split()
        if (opérations[a] < 0):
            positif = False
        else:
            positif = True

        for b in range(len(tmp)):
            theme = ""
            theme = comparaison_matricielle(tmp[b], positif)
            if (theme != ""):
                break
            else:
                pass
        if (theme == ""):
            opérations_list[len(opérations_list) - 1] += opérations[a]
        else:
            opérations_list[theme] += opérations[a]
    print(f"opérations_list = {opérations_list}")
    x = []
    y = []
    for i in range(len(opérations_list)):
        if (opérations_list[i] != 0):
            x.append(opérations_list[i])
            y.append(themes_list[i])
        else:
            pass

    plt.bar(y, x, width=0.1)
    plt.ylabel("thèmes")
    plt.grid(True)
    plt.show()


# Rapports gain / pertes par jours
def solde_evolution_quotidienne(dates_opérations, opérations):
    evolution_solde = []
    dates = []
    solde_courant = 0
    reference = 0
    for i in range(0, len(opérations)):
        solde_courant = solde_courant + opérations[i]
        if (i == 0):  # Rang n = 1
            evolution_solde.append(solde_courant)
            dates.append(dates_opérations[i])
            reference += 1
        elif (i > 0 and dates_opérations[i] != dates_opérations[i - 1]):  # Rang n > 0 et date différente du rang n - 1
            evolution_solde.append(solde_courant)
            dates.append(dates_opérations[i])
            reference += 1
        elif (i > 0 and dates_opérations[i] == dates_opérations[i - 1]):  # Rang n > 0 et date similaire du rang n - 1
            del evolution_solde[reference - 1]
            evolution_solde.append(solde_courant)
        elif (i == len(opérations)):
            if (dates_opérations[i] == [dates_opérations[i - 1]]):
                del evolution_solde[reference - 1]
                evolution_solde.append(solde_courant)
            else:
                evolution_solde.append(solde_courant)
                dates.append(dates_opérations[i])
                reference += 1
        else:
            print("Mist0")

    if (solde_courant >= 0):
        color = "g"
    else:
        color = "r"

    plt.grid(True, color='black', linewidth=0.5)
    plt.plot(dates, evolution_solde, color, linewidth=0.5, marker="+", label="évolution solde")
    plt.xticks(rotation=45)
    plt.legend()
    plt.show()


# Faire une analyse statistique sur une année complète
def analyse_année():
    pass


def window_analyse_mensuelle():
    def window_get_out():
        window.hide()


    # Production de statistiques sur le fichier csv choisi
    def analyse_statistique(nom_fichier, feuille_analyse):
        window.destroy()
        fichier = "/home/<username>/Documents/informatique/py/comptable/main/" + str(nom_fichier)  # MODIFIER
        # array_ods = read_ods(fichier)
        contenu = read_ods(fichier, feuille_analyse)
        dates_opérations = []
        opérations = []
        objet_opérations = []
        for i in range(0, len(contenu.values)):
            dates_opérations.append(contenu.values[i][0])
            opérations.append(contenu.values[i][1])
            objet_opérations.append(contenu.values[i][2])

        solde_evolution_quotidienne(dates_opérations, opérations)
        sujets_proportions(opérations, objet_opérations)


    def selection_feuille(fichier_sélectionné):
        # Mois disponibles
        bouton_1.disable()
        bouton_2.disable()
        Text(window, text="Choix d'un mois à analyser :")
        # Automatiser cette partie
        mois_1 = PushButton(window, text="Janvier", command=lambda: analyse_statistique(fichier_sélectionné, 1))
        mois_2 = PushButton(window, text="Février", command=lambda: analyse_statistique(fichier_sélectionné, 2))
        mois_3 = PushButton(window, text="Mars", command=lambda: analyse_statistique(fichier_sélectionné, 3))
        mois_4 = PushButton(window, text="Avril", command=lambda: analyse_statistique(fichier_sélectionné, 4))
        mois_5 = PushButton(window, text="Mai", command=lambda: analyse_statistique(fichier_sélectionné, 5))
        mois_6 = PushButton(window, text="Juin", command=lambda: analyse_statistique(fichier_sélectionné, 6))
        mois_7 = PushButton(window, text="Juillet", command=lambda: analyse_statistique(fichier_sélectionné, 7))
        mois_8 = PushButton(window, text="Août", command=lambda: analyse_statistique(fichier_sélectionné, 8))
        mois_9 = PushButton(window, text="Septembre", command=lambda: analyse_statistique(fichier_sélectionné, 9))
        mois_10 = PushButton(window, text="Octobre", command=lambda: analyse_statistique(fichier_sélectionné, 10))
        mois_11 = PushButton(window, text="Novembre", command=lambda: analyse_statistique(fichier_sélectionné, 11))
        mois_12 = PushButton(window, text="Décembre", command=lambda: analyse_statistique(fichier_sélectionné, 12))


    window = Window(app, title="Choix paramètres")
    # Automatiser cette partie
    Text(window, text="Choix d'une année à analyser :")
    bouton_1 = PushButton(window, text="2021.ods", command=lambda: selection_feuille("2021.ods"))
    bouton_2 = PushButton(window, text="2022.ods", command=lambda: selection_feuille("2022.ods"))


# Création de l'IG des analyses anuelles
def window_analyse_anuelle():
    pass
    # Renvoie vers la fonction de sélection du fichier ods à analyser


# [GUI] Triggered lorsque l'utilisateur clique sur la croix de fermeture
def fermer_programme_question():
    if app.yesno("Quitter ?", "Êtes vous sûr de vouloir quitter le programme ?"):
        app.destroy()
    else:
        pass

# [GUI] Triggered lorsque l'utilisateur clique sur le bouton quitter
def fermer_programme_decision():
    app.info(title="Information !", text="Fermeture du programme")
    app.destroy()


app = App(title="Programme")
titre = Text(app, text="Logiciel d'analyse statistique de comptes bancaires.", size="14")
menu_indication = Text(app, text="Menu de sélection :")
box_menu = Box(app, layout="grid")
bouton_analyse_mois = PushButton(box_menu, text="Analyse mensuelle", command=window_analyse_mensuelle, grid=[0, 0])
bouton_analyse_année = PushButton(box_menu, text="Analyse anuelle", command=window_analyse_anuelle, grid=[1, 0])
bouton_quitter = PushButton(app, text="Quitter le programme", command=fermer_programme_decision,)
app.when_closed = fermer_programme_question

app.display()

os.system("clear")

