"""
************COMPAR_EXTRACTIONS****************
LC : 02/04/2025

script permettant la comparaison de listings fournis (par IGA ou via BdmToFile) avec ceux référencés dans le portail soprano
arguments d'entrée:
    - OPER ou DBLE                    : chaine a récupérer sur le portail Soprano
    - ARPEGE, AROME, AEARO ou AROMEPI : application a récupérer sur le portail Soprano
    - assim, production ou court      : obligatoire pour arpège (optionnel pour les aromes qui prennent la valeur 'assim' par defaut

un fichier par date/réseau est généré et contient le décompte des obs extraites: un pour les fichier fournis (source) et un pour le portail soprano (sopra)
un tkdiff pour chaque réseau s'affiche à la fin pour afficher les écarts entre les deux pour chaque réseau

Les extractions Oulan ne sont pas présentes sur le portail soprano
Le portail contient les extractions de surface en plus

"""
import requests
import argparse
import subprocess
import os

date1 = ''
dates = []
mm = ''

def lire_fic(fic):
    print(f"lecture fichier source {fic}")

    # Lire le fichier
    with open(fic, 'r') as f:
        #ouvrir ici le fichier d'ecriture
        tab = ["extractions demandees","extractions erronees","extractions fichier vide","sans fichier","avec fichier","Nombre de concatenations","fichiers resultants"]

        #On teste si le fichier de sortie du reseau existe sinon on le crée
        global date1
         
        #if date1=='':
        fic_sortie = "fic_temp"
        #else:
            #fic_sortie = "fic_source"+date1[:-4]

        with open(fic_sortie, 'a') as fichier:
            fichier.write(f"\n{fic}\n")
            for line in f:
                if "POUR LE" in line:
                    parts = line.split()
                    date1 = parts[3][:-1]
                    print(f"date recuperee: {date1}")
                    fichier.write(f"{parts[3]}\n")
                if "Date demandee" in line:
                    parts = line.split()
                    convert_mois(parts[4])
                    date1 = parts[5]+mm+parts[3]
                if "Reseau demande" in line:
                    parts = line.split()
                    date1 = date1+parts[3]+'0000'
                    print(f"nouvelle date oulan finale: {date1}")
                if "tentative d'extraction" in line:
                    parts = line.split()
                    fichier.write(parts[4])
                if "extraction incorrecte" in line:
                    fichier.write("EXTRACTION INCORRECTE\n")
                if "records read" in line:
                    parts = line.split()
                    fichier.write(f" nb observations {parts[2]}\n")
                if "Date demandee" in line:
                    fichier.write(line)
                if "dans OBSOUL" in line:
                    fichier.write(line)
                for chaine in tab:
                    if  chaine in line:
                        fichier.write(line)
        if date1 not in dates:
            dates.append(date1)

        #if os.path.isfile("fic_temp"):
        ficRen = "fic_source"+date1[:-4]
        if os.path.isfile(ficRen):
            print(f"Ajout contenu lu dans {ficRen}")
            with open (fic_sortie,'r') as source , open(ficRen, 'a') as fichier:
                contenu = source.read()
                fichier.write(contenu)    
                commande = ["rm", fic_sortie]      
                resultat = subprocess.run(commande, text=True, capture_output=True)  
        else:    
            commande = ["mv", "fic_temp",  ficRen]
            resultat = subprocess.run(commande, text=True, capture_output=True)

        
        

def convert_mois(mois):
    global mm
    if mois == "janvier":
        mm = "01"
    if mois == "fevrier":
        mm = '02'
    if mois == "mars":
        mm = "03"
    if mois == "avril":
        mm = "04"
    if mois == "mai":
        mm = "05"
    if mois == "juin":
        mm = "06"
    if mois == "juillet":
        mm = "07"
    if mois == "aout":
        mm = "08"
    if mois == "septembre":
        mm = "09"
    if mois == "octobre":
        mm = "10"
    if mois == "novembre":
        mm = "11"
    if mois == "decembre":
        mm = "12"

def recuperer_et_lire_fichier(url):
    #print(f"lecture fichier source {url}")
    try:
        # Récupérer le fichier
        response = requests.get(url)
        
        # Vérifier si la requête a réussi
        response.raise_for_status()  # Cela lèvera une exception pour les codes d'erreur HTTP

        # Enregistrer le fichier localement
        nom_fichier = 'fichier_telecharge.txt'
        with open(nom_fichier, 'wb') as f:
            f.write(response.content)
        
        print(f"date1 avant def fic_sopra: {date1[-14:-4]}")
        fic_sortie_sopra = "fic_sopra"+date1[-14:-4]

        # Lire le fichier
        with open(nom_fichier, 'r') as f:
            #ouvrir ici le fichier d'ecriture
            tab = ["extractions demandees","extractions erronees","extractions fichier vide","sans fichier","avec fichier","Nombre de concatenations","fichiers resultants"]
            
            with open(fic_sortie_sopra, 'a') as fichier:
                fichier.write(f"\n{url}\n")
                for line in f:
                    if "POUR LE" in line:
                        parts = line.split()
                        fichier.write(f"{parts[3]}\n")
                    if "tentative d'extraction" in line:
                        parts = line.split()
                        #print(parts[4])
                        fichier.write(f"{parts[4]}")
                    if "extraction incorrecte" in line:
                        fichier.write(f"EXTRACTION INCORRECTE\n")
                    if "records read" in line:
                        parts = line.split()
                        fichier.write(f" nb observations {parts[2]}\n")
                    if "dans OBSOUL" in line:
                        fichier.write(line)
                    for chaine in tab:
                        if  chaine in line:
                            fichier.write(line)

    except requests.exceptions.RequestException as e:
        print(f"Erreur lors du téléchargement du fichier : {e}")
    except Exception as e:
        print(f"Une erreur est survenue : {e}")

#Programme principal
if __name__ == "__main__":
    # Créer un parseur d'arguments
    parser = argparse.ArgumentParser(description="Script pour récupérer des listings d'extraction soprano.\n")

    # Ajouter des arguments
    parser.add_argument("arg1", help="Le premier argument, la chaine: OPER ou DBLE")
    parser.add_argument("arg2", help="Le deuxième argument, l'application: ARPEGE, AROME, AEARO ou AROMEPI")
    parser.add_argument("arg3", help="Le cinquieme argument, le cutt-off pour ( valable uniquement pour ARPEGE : 'assim', 'production' ou 'court' (non utilisé par les AROMES qui prennent la valeur 'assim par defaut)")

    # Analyser les arguments
    args = parser.parse_args()

    #Nettoyage des fichiers
    commande = "rm fic_source*; rm fic_sopra*"
    resultat = subprocess.run(commande, shell=True, text=True, capture_output=True)

# Demande du fichier (et chemin) à comparer avec les fichiers du portail soprano"
    chem_source = input("Veuillez entrer le chemin complet du fichier a comparer avec le portail soprano : ")

    #Boucle sur les fichier du repertoire

    # Lister les fichiers et répertoires
    fichiers = os.listdir(chem_source)

    # Filtrer pour ne garder que les fichiers OULOUTPUT
    fichiers = [fichier for fichier in fichiers if fichier.startswith("OULOUTPUT") and not (fichier.endswith("AM") or fichier.endswith("CM") or fichier.endswith("DH") or fichier.endswith("PM") or fichier.endswith("SX")) and os.path.isfile(os.path.join(chem_source, fichier))]
    fichiers.sort()
    for fich in fichiers:
        print(fich)
    # Afficher les fichiers
    for fichier in fichiers:
        print(chem_source+"/"+fichier)
        date1 = ''
        lire_fic(chem_source+"/"+fichier)
    
        # Validation des arguments
        if args.arg1 not in ['OPER', 'DBLE']:
            print(f"Erreur : '{args.arg1}' n'est pas un choix valide pour arg1. Choisissez 'OPER' ou 'DBLE'.")
            sys.exit(1)  # Sortir avec un code d'erreur

        if args.arg2 not in ['ARPEGE', 'AROME', 'AEARO', 'AROMEPI']:
            print(f"Erreur : '{args.arg2}' n'est pas un choix valide pour arg2. Choisissez 'ARPEGE', 'AROME', 'AEARO' ou 'AROMEPI'.")
            sys.exit(1)  # Sortir avec un code d'erreur

        if args.arg1 == 'OPER':
            chaine = 'PNT_oper'
        elif args.arg1 == 'DBLE':
            chaine = 'PNT_double'
        else:
            chaine = ''

        ##Verifie si le fichier de sortie soprano du reseau existe deja
        if not os.path.isfile("fic_sopra"+date1[-14:-4]): 
            print(f"Creation du fichier fic_sopra{date1[-14:-4]}")

            print("Recuperation des fichiers associés sur soprano:")
            ### CAS ARPEGE 
            tab = ['_surf','_b1', '_b2', '_b3', '_b4','']
            if args.arg2 == 'ARPEGE':
                appli = 'arpege'
                fic1 = 'arp'
                for val in tab:
                    if args.arg3 == 'assim':
                        url = "http://dev-soprano.meteo.fr/logs/oper8/" + str(chaine) + "/"+ str(appli) + "/france/" + str(args.arg3) + "/obs/extobs" + str(val) + "_" + str(args.arg3) + "/extobs" + str(val) + "_" + str(args.arg3) + "_" + str(date1) + "_000000_1"
                        print(f"requete  extobs{str(val)}_{str(args.arg3)}_{str(date1)}_000000_1 ")
                        recuperer_et_lire_fichier(url)
                    elif args.arg3 == 'production':
                        url = "http://dev-soprano.meteo.fr/logs/oper8/" + str(chaine) + "/"+ str(appli) + "/france/" + str(args.arg3) + "/obs/extobs" + str(val) + "_prod/extobs" + str(val) + "_prod_" + str(date1) + "_000000_1"
                        print(f"requete _prod/extobs{str(val)}_prod_{str(date1)}_000000_1")
                        recuperer_et_lire_fichier(url)
                    elif args.arg3 == 'court':
                        url = "http://dev-soprano.meteo.fr/logs/oper8/" + str(chaine) + "/"+ str(appli) + "/france/" + str(args.arg3) + "/obs/extobs" + str(val) + "_court/extobs" + str(val) + "_court_" + str(date1) + "_000000_1"
                        print(f"requete extobs{str(val)}_court_{str(date1)}_000000_1")
                        recuperer_et_lire_fichier(url)

            ### CAS AROME

            elif args.arg2 == "AROME": # France, il n'y a que des extractions en cut-off assim
                appli = 'arome'
                tab = ['', '_surf' ]
               # print(f"date1 avant creation url: {date1}")
                for val in tab:
                    url = "http://dev-soprano.meteo.fr/logs/oper8/" + str(chaine) + "/"+ str(appli) + "/france/assim/obs/extobs"+ str(val)+"_aro_assim/extobs"+  str(val) + "_aro_assim_" + str(date1) + "_000000_1"
                    print(url)
                    recuperer_et_lire_fichier(url)

            ### CAS AEARO

            elif args.arg2 == "AEARO": # France, il n'y a que des extractions en cut-off assim
                appli = 'arome'
                #tab = ['', '_surf' ]
                for val in tab:
                    url = "http://dev-soprano.meteo.fr/logs/oper8/" + str(chaine) + "/"+ str(appli) + "/aefrance/obs/extobs_aearo" + str(val) + "/extobs_aearo" + str(val) + "_" + str(date1) + "_000000_1"
                    print(url)
                    recuperer_et_lire_fichier(url)

            ### CAS AROMEPI

            elif args.arg2 == 'AROMEPI':

                url = "http://dev-soprano.meteo.fr/logs/oper8/" + str(chaine) + "/arome/pifrance/extobs_api/extobs_api_" + str(date1) + "_000000_1"
                recuperer_et_lire_fichier(url)

            

    for dat in dates:
        fic1 = "fic_sopra"+dat[-14:-4]
        fic2 = "fic_source"+dat[:-4]    
        commande = ["tkdiff", fic1, fic2]
        resultat = subprocess.run(commande, text=True, capture_output=True)
