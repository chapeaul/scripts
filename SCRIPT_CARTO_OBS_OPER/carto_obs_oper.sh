#!/bin/sh

# constantes
HOST=hendrix.meteo.fr
LOGIN=chapeaul
PASSWORD=Tesateba2029!
PORT=21
DESTINATAIRE="laurent.chapeau@meteo.fr"
SUJET="Carto obs OPER"
MESSAGE="La carte des obs OPER est disponible sur sxobs1 /SCRIPT_CARTO_OBS_OPER"

# le transfert lui même
# aller dans le répertoire OPER du jour
# Récupérer la base conv
# utiliser les scripts de carto existants pour tracer le positionnement des obs (avec des options selon ce qu'on veut tracer

#definition de la date
var=$(date +%Y)+$(date +%m)+$(date +%d)+T0000A
HOST=taranis.meteo.fr 
lftp -u $LOGIN,$PASSWORD $HOST $PORT << END_SCRIPT
quote USER $LOGIN
quote PASS $PASSWORD
cd /chaine/mxpt001/vortex/mtool/cache/vortex/arpege/4dvarfr/OPER/$(date +%Y)$(date +%m)$(date +%d)T0000A/observations
mirror --verbose odb-ecma.build.conv
quit
END_SCRIPT

echo "Argument fourni : $1"


python3 Gener_Carte.py "$@"

if [ -d "odb-ecma.build.conv" ]; then
	rm -rf odb-ecma.build.conv
fi
# Envoi de l'e-mail
    echo "$MESSAGE" | mail -s "$SUJET" "$DESTINATAIRE"

#ftp -i -n $HOST $PORT << END_SCRIPT
#quote USER $LOGIN
#quote PASS $PASSWORD
#pwd
#cd /home/m/marp/marp999/vortex/O/P/E/R/
#quit


#END_SCRIPT
