# Importation des modules nécessaires
from os import path, mkdir
from pickle import dump, load
from requests import get
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from tqdm import tqdm

# Création de fonctions utilitaires pour la gestion des fichiers pickle
creer_dossier = lambda lien:mkdir(lien) if not path.exists(lien) else None # créer un dossier s'il n'existe pas.
verif_var = lambda nom: path.isfile("data/"+nom+".pickle") # vérifier si une variable pickle existe.
def creer_var(nom:str, donnee)->None:
    """
    Crée une variable pickle avec le nom et les données fournies.

    Arguments
    ---------
    nom : str
        Le nom de la variable pickle à créer (sans chemin ni extension).
    donnee : ...
        Les données à stocker dans la variable pickle.

    Retourne
    --------
    None
        Cette fonction ne retourne rien, mais crée un fichier pickle dans le dossier "data".
    """
    creer_dossier("data")
    with open(f"data/{nom}.pickle","wb") as fichier_donnee:
        dump(donnee, fichier_donnee)
lire_var = lambda nom: load(open(f"data/{nom}.pickle", "rb")) if verif_var(nom) else None # lire une variable pickle si elle existe.

# Création de fonctions utilitaires pour la gestion des fichiers HTML
télécharger_html = lambda lien, destination="data.html":open(destination,"w").write(get(lien).text)
def extraire_classement(source:str="data.html")->dict:
    """
    Extrait le classement des équipes à partir d'un fichier HTML.

    Arguments
    ---------
    source : str (optionnel)
        Le chemin du fichier HTML à partir duquel extraire le classement. Par défaut, il s'agit de "data.html".
    
    Retourne
    --------
    dict
        Un dictionnaire contenant les noms des équipes comme clés et leurs points comme valeurs.
    """
    classement = BeautifulSoup(open(source, "r"), "html.parser").find_all("div", class_="table-line table-line--ranking-full table-line--ranking-scrollable")
    dico = {}
    for equipe in classement:
        nom = equipe.find("div", class_="table-line__cell-wrapper table-line__cell-wrapper--full table-line__cell-wrapper--club-name").find("a").string
        points = int(equipe.find("div", class_="table-line__cell--small").string)
        dico[nom[1:]] = points
    return dico
transfo_division = lambda var: "top14" if var == "1" else "prod2" if var == "2" else None # transforme le numéro de division en nom de division.

# Fonctions principales
def charger_saison(division:str, saison:str, dernière_journee:int)->list:
    """
    Charge les données de la saison pour une division et une journée spécifiques.

    Arguments
    ---------
    division : str
        La division à charger (par exemple, "top14" ou "prod2").
    saison : str
        La saison à charger au format "20XX-20XX".
    dernière_journee : int
        Le numéro de la dernière journée à prendre en compte.

    Retourne
    --------
    list
        Une liste contenant les données de la saison pour chaque équipe.
    """
    liste_dico = []
    for journee in tqdm(range(1, dernière_journee + 1)):
        if not verif_var(f"{division}{saison}{journee}"):
            télécharger_html(f"https://{division}.lnr.fr/classement/{saison}/j{journee}")
            creer_var(f"{division}{saison}{journee}", extraire_classement())
        liste_dico.append(lire_var(f"{division}{saison}{journee}"))
    return liste_dico

if __name__ == "__main__":
    division = transfo_division(input("Quelle est la division étudiée ? (1 ou 2) : "))
    assert division in ["top14", "prod2"], "Division invalide. Veuillez entrer 1 pour Top 14 ou 2 pour Pro D2."
    saison = input("Quelle est la saison étudiée ? (attention au format : 20XX-20XX) : ")
    assert len(saison) == 9 and saison[4] == '-', "Format de saison invalide. Veuillez utiliser le format 20XX-20XX."
    if division == "top14" and verif_var(f"top14{saison}26"):
        dernière_journee = 26
    elif division == "prod2" and verif_var(f"prod2{saison}30"):
        dernière_journee = 30
    else:
        dernière_journee = int(input("Quelle est la derniere journee à prendre en compte ? : "))
        assert dernière_journee > 0, "La dernière journée doit être un nombre positif."
    liste_dico = charger_saison(division, saison, dernière_journee)
    
    couleurs=[(0,0,0),(1,0,0),(1,1,0),(0,1,0),(0,1,1),(0,0,1),(1,0,1),(0.5,0,0),(0.5,0.5,0),(0,0.5,0),(0,0.5,0.5),(0,0,0.5),(0.5,0,0.5),(0.5,0.5,0.5),(1,0.5,0.5),(0.5,1,0.5),(0.5,0.5,1)]
    liste_équipes = list(liste_dico[-1].keys())
    for i in range(len(liste_équipes)):
        liste_points = [dico[liste_équipes[i]] for dico in liste_dico]
        plt.plot(range(1, dernière_journee + 1), liste_points, color=couleurs[i], label=liste_équipes[i])
    plt.title(f"Evolution des points des equipes de {division} (saison {saison})")
    plt.legend(fontsize="7")
    creer_dossier("exportations")
    plt.savefig(f"exportations/{division+saison}.svg", format='svg', dpi=1200)
    plt.show()