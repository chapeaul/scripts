#!/bin/bash

oldIFS=IFS
IFS=$'\n'

var=`pwd`
i=1
num=""
jour=""
heure=""

echo $var
rm bufr.txt


for file in "$var"/*; do
	if [ -d "$file" ];then  	 
         cd $file
	 echo `pwd`
         #echo `ls`
	 var2=`pwd`
	 for file2 in *;do
		 if [ -f "$file2" ];then
			 echo $file2
			 if [ "$file2" = "bufr.synop" ];then
				 DecodBufr -i $file2 >> $var/bufr.txt
	                 fi
         	  fi
	  done
        fi
done

cd $var
echo `pwd`

for fic in *; do
if [ -f "$fic" ];then
        while IFS= read -r ligne || [ -n "$ligne" ]
        do
	           if  echo "$ligne" | grep -q "*********** BUFR file"

                   then
                      num=$(echo "$ligne" | awk -F"° " '{print $2}')
	           fi
		   if echo "$ligne" | grep -q "       Day"
		   then
			   jour=$(echo "$ligne" | awk -F"=" '{print $2}')
		   fi
		   if echo "$ligne" | grep -q "       Hour"
		   then
			   heure=$(echo "$ligne" | awk -F"=" '{print $2}')
			   echo "le $jour a $heure bufr num: $num"
			   let i+=1
		   fi
	
	done < $fic
	echo "Nombre du BUFR sur la periode : $i"
fi
done
