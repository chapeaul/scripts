#!/bin/bash
# ./compar_listingObs.sh -a all -b GTXB -c GTX5 -d arpege -e 20240603T0600A

oldIFS=IFS
IFS=$'\n'

echo
echo "Récupération des listings par défaut sous scratch/mtool/cache/vortex"
if [ "$#" -le "5" ] 
then
	echo "Le nombre d'arguments attendus n'est pas respecté: renseigner au minimum les noms des dux fichiers"
	echo "arg1 : sensor de référence"
	echo "arg2 : xp1"
	echo "arg3 : xp2"
	echo "arg4 : modele"
	echo "arg5 : réseau (AAAAMMJJHHTHHmmA)"
	exit
fi

usage() {
    echo "Usage: $0 -a sensor  -b xp1 -c xp2 -d modele"
    exit 1
}

repertoire1=""
repertoire2=""
chem="/scratch/mtool/chapeaul/cache/vortex"
fichier1=""
xp1=""
xp2=""
obs1=0
data1=0
obs2=0
data2=0
modele="arpege"
reseau=""
sensor="all"
files=()

# Lire les options
while getopts ":a:b:c:d:e:" opt; do
    case ${opt} in
        a )
            sensor=$OPTARG
            ;;
        b )
	    xp1=$OPTARG
            ;;
	c )
	    xp2=$OPTARG	
	    ;;
	d )
            modele=$OPTARG
	    ;;
	e )
            reseau=$OPTARG
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
shift $((OPTIND -1))

#########################
#Definition du répertoire
#########################

if [ $modele = "arpege" ]; then
   repertoire1=$chem"/"$modele"/4dvarfr/"$xp1"/"$reseau"/stacks/flow_logs.filespack/observations"
   repertoire2=$chem"/"$modele"/4dvarfr/"$xp2"/"$reseau"/stacks/flow_logs.filespack/observations"
else
   repertoire1=$chem"/"$modele"/3dvarfr/"$xp1"/"$reseau"/stacks/flow_logs.filespack/observations"
   repertoire2=$chem"/"$modele"/3dvarfr/"$xp2"/"$reseau"/stacks/flow_logs.filespack/observations"
fi

########################################
## si on recupere tous les fichiers logs
########################################
if [ $sensor = "all" ];then
 declare -A mappingFic1Obs
 declare -A mappingFic1Data
 declare -A mappingFic2Obs
 declare -A mappingFic2Data
 i=0
 j=0
 nbfic=$(find "$repertoire1" -type f | wc -l)
 for file in "$repertoire1"/*; do
   if [ -f "$file" ]; then
        i=$((i+1))
        echo "Traitement $i / $nbfic $xp1 $(echo "$file" | awk -F"." '{print $4}') ..."
        # Ajouter le nom du fichier au tableau
        files+=("$file")
        while IFS= read -r ligne || [ -n "$ligne" ]
         do
           if  echo "$ligne" | grep -q "Total selected Obs"
           then
           j=$((j+1))
           rest=$(echo "$ligne" | awk -F"=" '{print $2}')
           obs1=$(echo "$rest" | awk -F"-->" '{print $1}')
           rest1=$(echo "$rest" | awk -F"-->" '{print $2}')
           data1=$(echo "$rest1" | awk -F"datas" '{print $1}')
           mappingFic1Obs["$(echo "$file" | awk -F"." '{print $4}')"]=$obs1
           mappingFic1Data["$(echo "$file" | awk -F"." '{print $4}')"]=$data1
           #cas des abi
           elif echo "$ligne" | grep -q "Total number of observations" 
           then
           j=$((j+1))
           obs1=$(echo "$ligne" | awk -F":" '{print $3}')
           mappingFic1Obs["$(echo "$file" | awk -F"." '{print $4}')"]=$obs1
           elif echo "$ligne" | grep -q "Total number of wagon in ODB arrays"
           then
           data1=$(echo "$ligne" | awk -F":" '{print $3}')
           mappingFic1Data["$(echo "$file" | awk -F"." '{print $4}')"]=$data1
           fi
         done < $file
        if [ "$j" -eq 0 ];then
           echo " Erreur sur le fichier $file : pas d'Obs trouvees"
        fi
    fi
   j=0
 done

 i=0
 j=0
 for file in "$repertoire2"/*; do
   if [ -f "$file" ]; then
        i=$((i+1))
        echo "Traitement $i / $nbfic $xp2 $(echo "$file" | awk -F"." '{print $4}') ..."
        files+=("$file")
        while IFS= read -r ligne || [ -n "$ligne" ]
        do
          if  echo "$ligne" | grep -q "Total selected Obs"
          then
           j=$((j+1))
           rest=$(echo "$ligne" | awk -F"=" '{print $2}')
           obs2=$(echo "$rest" | awk -F"-->" '{print $1}')
           rest2=$(echo "$rest" | awk -F"-->" '{print $2}')
           data2=$(echo "$rest2" | awk -F"datas" '{print $1}')
           mappingFic2Obs["$(echo "$file" | awk -F"." '{print $4}')"]=$obs2
           mappingFic2Data["$(echo "$file" | awk -F"." '{print $4}')"]=$data2

           #cas des abi
           elif echo "$ligne" | grep -q "Total number of observations"
           then
           j=$((j+1))
           obs2=$(echo "$ligne" | awk -F":" '{print $3}')
           mappingFic2Obs["$(echo "$file" | awk -F"." '{print $4}')"]=$obs2
           elif echo "$ligne" | grep -q "Total number of wagon in ODB arrays"
           then
           data2=$(echo "$ligne" | awk -F":" '{print $3}')
           mappingFic2Data["$(echo "$file" | awk -F"." '{print $4}')"]=$data2
           fi
         done < $file
         if [ "$j" -eq 0 ];then
           echo " Erreur sur le fichier $file : pas d'Obs trouvees"
         fi
    fi
  j=0
 done

echo
echo
echo "************************************************************"
echo "********  COMPARAISON OBS / DATA entre les 2 XP  ***********"
echo "************************************************************"
echo
echo "                SENSOR              $xp1                   $xp2"

#Faire une boucle de lecture sur les mapping pour afficher les données de chaque sensor
for key in "${!mappingFic2Obs[@]}";do
	echo "           $key      |   ${mappingFic1Obs[$key]}    |   ${mappingFic2Obs[$key]}        $(if [ "${mappingFic1Obs[$key]}" != "${mappingFic2Obs[$key]}" ];then echo "DIFFERENT";else echo "OK";fi ) "
        echo "           $key      |           ${mappingFic1Data[$key]}   |          ${mappingFic2Data[$key]}        $(if [ "${mappingFic1Data[$key]}" != "${mappingFic2Data[$key]}" ];then echo "DIFFERENT";else echo "OK";fi ) "

        echo ---------------------------------------------------------------
done

##############################
## Cas d'un sensor particulier
##############################
else

   fichier1=$repertoire1"/listing.batodb-batodb_misc."$sensor
   fichier2=$repertoire2"/listing.batodb-batodb_misc."$sensor


while IFS= read -r ligne || [ -n "$ligne" ]
do
  if  echo "$ligne" | grep -q "Total selected Obs"
  then
	  rest=$(echo "$ligne" | awk -F"=" '{print $2}')
	  obs1=$(echo "$rest" | awk -F"-->" '{print $1}')
          rest1=$(echo "$rest" | awk -F"-->" '{print $2}')
	  data1=$(echo "$rest1" | awk -F"datas" '{print $1}')
  fi
done < $fichier1

while IFS= read -r ligne || [ -n "$ligne" ]
do
  if  echo "$ligne" | grep -q "Total selected Obs"
  then
          rest=$(echo "$ligne" | awk -F"=" '{print $2}')
          obs2=$(echo "$rest" | awk -F"-->" '{print $1}')
          rest2=$(echo "$rest" | awk -F"-->" '{print $2}')
          data2=$(echo "$rest2" | awk -F"datas" '{print $1}')
  fi
done < $fichier2
echo
#echo "listing des sensors : $(if [ "$sensor" != "all" ];then for capt in "${files[@]}";do echo "$capt";else echo "$sensor";fi ) "
echo
echo
echo "************************************************************"
echo "********  COMPARAISON OBS / DATA entre les 2 XP  ***********"
echo "************************************************************"
echo
echo "                SENSOR              $xp1                   $xp2"
echo "  --------------------------------------------------------------------------"
echo "  Nb Obs  |    $sensor     |       $obs1     |       $obs2          $(if [ "$obs1" != "$obs2" ];then echo "DIFFERENT";else echo "OK";fi ) "
echo "  Nb data |    $sensor     |    $data1      |    $data2           $(if [ "$data1" != "$data2" ];then echo "DIFFERENT";else echo "OK";fi ) "

fi
