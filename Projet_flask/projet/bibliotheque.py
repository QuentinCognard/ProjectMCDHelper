import os
import os.path
from .app import *
from .models import *

def mkpath(p):
    return os.path.normpath(
        os.path.join(
            os.path.dirname(__file__),
            p))

def recup_entite_attribut_textuel(mcd_textuel):
    debut = mcd_textuel.index("<entite>");
    fin = mcd_textuel.index("</entite>");
    entite_textuel = mcd_textuel[debut:fin].split("<entite>")[1]
    liste_entite = []
    lines = entite_textuel.split("\n");
    for ligne in lines:
        if ligne != '':
            liste_entite.append(ligne)
    dict_entite = {}
    for table in liste_entite:
        liste_attribut = []
        debut = table.index("<attribut>");
        fin = table.index("</attribut>");
        attribut_textuel = table[debut:fin].split("<attribut>")[1].split(";")
        nomEntite = table.split("<attribut>")[0]
        for a in attribut_textuel:
            if a != '':
                liste_attribut.append(a)
        dict_entite[nomEntite] = liste_attribut
    return dict_entite

def recup_relation_textuel(mcd_textuel):
    debut = mcd_textuel.index("<relation>");
    fin = mcd_textuel.index("</relation>");
    relation_textuel = mcd_textuel[debut:fin].split("<relation>")[1]
    liste_entite = []
    lines = relation_textuel.split("\n");
    for ligne in lines:
        if ligne != '':
            liste_entite.append(ligne)
    dict_entite = {}
    for table in liste_entite:
        liste_attribut = []
        debut = table.index("<concerne>");
        fin = table.index("</concerne>");
        attribut_textuel = table[debut:fin].split("<concerne>")
        nomEntite = table.split("<concerne>")[0]
        for a in attribut_textuel:
            if a != '':
                liste_attribut.append(a)
        dict_entite[nomEntite] = liste_attribut
    return dict_entite


def ajouter_entite(dictionnaire_entite_attribut):
    for (entite,attribut) in dictionnaire_entite_attribut.items():
        print("- Ajout de l'entite :", entite)
        for a in attribut:
            nom = a.split('(')[0]
            debut = a.index("(") + 1
            fin = a.index(")")
            genre = a[debut:fin].split(",")[0]
            typea = a[debut:fin].split(",")[1]
            print("     - Ajout de l'attribut :", "(nomA : " + nom + " / " + "genreA : " + genre + " / " + "typeA : " + typea + ")")

def ajouter_relation(dictionnaire_relation):
    for (relation,entite) in dictionnaire_relation.items():
        print("- Ajout de la relation :", relation)
        entite_txt = entite[0]
        entite1 = entite_txt.split(';')[0].split("(")[0]
        entite2 = entite_txt.split(';')[1].split("(")[0]
        cardinalite_e1 = entite_txt.split(';')[0].split("(")[1].replace(")","")
        cardinalite_e2 = entite_txt.split(';')[1].split("(")[1].replace(")","")
        print("     - Entite 1 :", entite1 + " / card :" + cardinalite_e1)
        print("     - Entite 2 :", entite2 + " / card :" + cardinalite_e2)

def importer_donnees(filename):
    fichier = open(os.path.join(mkpath('static/MCD/Lucas/'), filename), "r")
    mcd_textuel = fichier.read()
    dictionnaire_entite_attribut = recup_entite_attribut_textuel(mcd_textuel)
    dictionnaire_relation = recup_relation_textuel(mcd_textuel)
    print("############################    Entites    ############################")
    ajouter_entite(dictionnaire_entite_attribut)
    print("\n############################    Relations    ############################")
    ajouter_relation(dictionnaire_relation)
    print(get_all_login())
    # print("Dictionnaire entite : ", dictionnaire_entite_attribut)
    # print("Dictionnaire relation : ", dictionnaire_relation)

importer_donnees("test.txt")
