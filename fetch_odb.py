#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Librairies système de base
import os
import sys
import subprocess


# Librairies pour vortex
#import usevortex as vtx
#import vortex

# Librairies personnelles
#sys.path.append("/cnrm/obs/data1/audouino/SCRIPTS/00_PYTHON_ODB_STUFF/odb_stuff")
#import odb_stuff.retrieve_odb as osret
#import odb_stuff.miscellanea as osmis
#import odb_stuff.sql_stuff as oss

print("Tout va bien ! Les libraires ont bien été chargées")



# Caractéristiques des données à récupérer
i_exp           = 'GZIO'
instru          = 'conv'
i_date          = '202410230600'
model           = 'arpege'
block           = 'Observation'
cutoff          = 'assim' #'production'
#inst_id         = osmis.get_inst_id(instru)

# Répertoires sur lustre pour la sauvegarde des données
#dir_name_tar    = '/cnrm/obs/data1/chapeaul/NO_SAVE/cache'
dir_name_tar    = '~/CARTES/'
#dir_name_vortex = '/cnrm/obs/data1/chapeaul/NO_SAVE/vortex'
dir_name_vortex = '~/CARTES/vortex'
#dir_name_netcdf = '/cnrm/obs/data1/chapeaul/NO_SAVE/ODBfiles'
dir_name_netcdf = '~/CARTES/ODBfiles'


# Mise de la date + réseau au format vortex (e.g. 20240101T1200A)
#date_vortex = osmis.format_date_vortex(i_date,cutoff)

# Nom de l'archive .tgz qui sera créée sur lustre
#file_name_tar = osret.create_tar_odb_name(dir_name_vortex,model,i_exp,date_vortex,block,instru)
# Nom de la base odb une fois que l'archive aura été dézippée
#base_odb = osret.create_base_odb_name(dir_name_vortex,model,i_exp,date_vortex,block,instru)
base_odb = '/home/chapeaul/CARTES/ODBfiles/odb-ecma.build.conv'

#print('Archive à extraire',file_name_tar)
#print('Base odb', base_odb)

# Test de l'existence de la base et extraction depuis hendrix si besoin
#if os.path.exists(base_odb):
#    print('La base ODB '+base_odb+' a déjà été extraite !')
#else:
#    if os.path.exists(file_name_tar):
#        print('le fichier',file_name_tar,'existe déjà !')
#    else:
#        # Récupération de la base sous la forme d'une archive .tgz depuis Hendrix
#        osret.retrieve_odb_from_hendrix(i_exp,i_date,model,block,cutoff,instru,dir_name_tar)
#        print('Archive extraite depuis hendrix!')
#    #Détarrage de l'archive .tgz    
#    osret.untar_odb_tgz(dir_name_vortex,i_exp,date_vortex,model,block,instru)

# Création d'un fichier netcdf à partir d'une requête SQL sur la base odb
sql_request = 'SELECT lat,lon,obsvalue,vertco_reference_1 from hdr,body' 
#sql_request = oss.sql_allsky_complete(inst_id) 

print('Exploration de la base'+base_odb)

# Nom du fichier .nc issu de la requête
#odb_output_nc = osret.create_netcdf_name(dir_name_netcdf,model,i_exp,date_vortex,block,instru,'basic')
odb_output_nc = '/home/chapeaul/CARTES/output.nc'

#if os.path.exists(odb_output_nc):
#    print('le fichier '+odb_output_nc+' existe déjà')
#else:
#    print('le fichier '+odb_output_nc+' sera créé')
#subprocess.call(['/home/martinezs/apps/public/bin/odbsql', '-q', sql_request,'-i',base_odb, '-f', 'unetcdf', '-o',odb_output_nc ])
subprocess.call(['/home/martinezs/apps/public/bin/odbsql', '-q', sql_request,'-i',base_odb, '-f', 'unetcdf','-o', odb_output_nc ])

#sql_request = oss.sql_desroziers(inst_id) 

# Nom du fichier .nc issu de la requête
#odb_output_nc = osret.create_netcdf_name(dir_name_netcdf,model,i_exp,date_vortex,block,instru,'desroziers')
#print('le fichier '+odb_output_nc+' sera créé')

#subprocess.call(["odbsql", '-q', sql_request,'-i',base_odb, '-f', 'unetcdf', '-o',odb_output_nc ])

#sql_request = oss.sql_allsky_iasi_surface(16) 

# Nom du fichier .nc issu de la requête
#odb_output_nc = osret.create_netcdf_name(dir_name_netcdf,model,i_exp,date_vortex,block,instru,'allsky')
#print('le fichier '+odb_output_nc+' sera créé')

#subprocess.call(["odbsql", '-q', sql_request,'-i',base_odb, '-f', 'unetcdf', '-o',odb_output_nc ])
print('étonnant non ?')

