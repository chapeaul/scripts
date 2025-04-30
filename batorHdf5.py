import h5py
import argparse

def structure(fic):
    with h5py.File(fic, 'r') as file:
        # Lister les noms des groupes et des datasets dans le fichier
        print("Contenu du fichier HDF5 :")
        file.visit(print)

def dataset(fic,dset):
    with h5py.File(fic, 'r') as file:
        
        for nom in file:
            print(nom)
 
        print(dset)
        if dset in file:
            data = file[dset]
            print(f"Données non nulles du dataset '{dset}':")
        
            data_filtrees = data[data != -9999.9]
            print(data_filtrees)
        else:
            print(f"Le dataset '{dataset_name}' n'existe pas dans le fichier.")

def main():
    # Configurer l'analyseur d'arguments
    parser = argparse.ArgumentParser(description='Affiche le squelette Hdf5.Récupérer la première valeur de la quatrième dimension d\'un dataset HDF5.')
    parser.add_argument('arguments', nargs='*', help='Liste d\'arguments à traiter')
    parser.add_argument('--o', type=str, help='Option de traitement: S(squelette)')
    parser.add_argument('--n', type=str, help='nom du dataset à récupérer pour l\'option D')
    parser.add_argument('--f', type=str, help='Chemin vers le fichier HDF5')
    parser.add_argument('--g', type=str, help='Nom du groupe dans le fichier HDF5')
    parser.add_argument('--d', type=str, help='Nom du dataset dans le groupe')

    # Analyser les arguments
    try:
        args = parser.parse_args()

        # Afficher les arguments récupérés
        print("Arguments récupérés :")
        for arg in args.arguments:
            print(arg)
  
        if args.o not in ['S','D']:
            print("L'argument --o manquant (S: squelette)")
        else:
            
            #CAS1 : Affichage du squelette du fichier hdf5i
            if args.o == 'S':
                structure(args.f)

            elif args.o == 'D':
                print(args.n)
                dataset(args.f,args.n)
                print("Option de traitement de récupération de dataxset D")
            else:
                print("Option de traitement --o non reconnue")

            # Appeler la fonction et récupérer la première valeur de la quatrième dimension
            #valeur = recuperer_premiere_valeur(args.fichier_hdf5, args.nom_groupe, args.nom_dataset)

            #print("Première valeur de la quatrième dimension :")
            #print(valeur)

    except SystemExit:
        # Cela se produit si aucun argument n'est fourni ou si l'utilisateur demande de l'aide
        print("Aucun argument fourni ou erreur dans les arguments. Voici les options :")
        parser.print_help()

    except AttributeError:
        print("Erreur dans le fichier fourni :")
        parser.print_help()

    except NameError:
        print("Dataset non fourni ou inexistant")


if __name__ == '__main__':
    main()
