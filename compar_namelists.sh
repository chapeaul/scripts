#!/bin/bash

oldIFS=IFS
IFS=$'\n'

echo "comparaison des cles entre deux namelistes"

if [ "$#" -le "1" ]
then
    echo "Le nombre d'arguments attendus n'est pas respecte: deux namelistes necessaires"
fi

usage() {
    echo "Usage: $0 -a namel1  -b namel2"
    exit 1
}

namel1=""
namel2=""
cle=""
val=""
cle2=""
val2=""

# Lire les options
while getopts ":a:b:" opt; do
    case ${opt} in
        a )
            namel1=$OPTARG
            ;;
        b )
            namel2=$OPTARG
            ;;
        \? )
            echo "Invalid option: -$OPTARG" 1>&2
            usage
            ;;
        : )
            echo "Invalid option: -$OPTARG requires an argument" 1>&2
            usage
            ;;
    esac
done
echo "fichier nameliste ref: $namel1"
echo "Fichier nameliste 2: $namel2"

# On supprime le fichier de sortie si il existe deja
if [ -f "$namel2.out" ]; then
  rm $namel2.out
fi


if [ -f "$namel1" ]; then
      echo "Lecture du fichier $namel1"
      
      while IFS= read -r ligne || [ -n "$ligne" ]
       do
         if echo "$ligne" | grep -q "="
         then
           cle=$(echo "$ligne" | awk -F "=" '{print $1}' | sed -e " s/\ //g")
           val=$(echo "$ligne" | awk -F "=" '{print $2}' | sed -e " s/\ //g")
           
           #Boucle sur la seconde nameliste
           while IFS= read -r ligne2 || [ -n "$ligne2" ]
           do
             if echo "$ligne2" | grep -q "="
             then
               cle2=$(echo "$ligne2" | awk -F "=" '{print $1}' | sed -e " s/\ //g")
               val2=$(echo "$ligne2" | awk -F "=" '{print $2}' | sed -e " s/\ //g")
               if [[ "$cle" == "$cle2" ]]
               then
                 if [[ "$val" != "$val2" ]]
                 then
                    echo "$cle présente mais valeur différente dans seconde nameliste $namel2"
                    echo "   $cle=$val2 ? choix à faire" >> $namel2.out
                    continue 2
                   else
                    echo "   $cle=$val" >> $namel2.out
                    continue 2  
                 fi
               continue 2
               fi
             fi
           done < $namel2
           echo "$cle absente dans la seconde nameliste $namel2"
           echo "   $cle= RAJOUTEE! a verifier" >> $namel2.out
         else 
         echo "$ligne" >> $namel2.out
         fi
        done < $namel1
fi 

