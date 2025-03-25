import json
import pandas as pd
import matplotlib.pyplot as plt
import argparse

def afficher_graphique_json(fichier_json):
    # Lire le contenu du fichier JSON
    with open(fichier_json, 'r', encoding='utf-8') as f:
        contenu = json.load(f)

    # Extraire les données
    labels = list(contenu.keys())
    time_real_values = [contenu[key]['time_real'] for key in labels]

    # Ajouter des titres et des labels
    bars=plt.bar(labels, time_real_values, color=['blue', 'orange'])
    plt.xlabel('Sections')
    plt.ylabel('Temps réel (s)')
    plt.title('Temps réel par section')
    plt.ylim(0, max(time_real_values) + 1)  # Ajuster l'axe y pour plus de clarté
    plt.grid(axis='y')
    plt.title(fichier_json)  # Utiliser le titre du fichier ici

    # Afficher le graphique
    plt.tight_layout()
    # Afficher les valeurs au-dessus des barres
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 2), ha='center', va='bottom')

    plt.show()

def main():
    # Créer un parseur d'arguments
    parser = argparse.ArgumentParser(description='Afficher un graphique à partir d\'un fichier JSON.')
    parser.add_argument('fichier_json', type=str, help='Le chemin vers le fichier JSON à afficher')

    # Analyser les arguments
    args = parser.parse_args()

    # Afficher le graphique du fichier JSON
    afficher_graphique_json(args.fichier_json)

if __name__ == '__main__':
    main()

