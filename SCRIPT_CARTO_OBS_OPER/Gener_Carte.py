#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  1 09:16:53 2023
"""
import os
import sys
import subprocess
import numpy as np
from netCDF4 import Dataset
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import argparse
from datetime import datetime

# Initialise le parser d'arguments
parser = argparse.ArgumentParser(description="Script d'exemple pour traiter des arguments.")
# Analyser les arguments
parser.add_argument('where', type=str, help='complement requete where.')
# Analyse les arguments fournis
args = parser.parse_args()
base_odb = 'odb-ecma.build.conv'
sql_request = "SELECT lat,lon,obsvalue,vertco_reference_1 from hdr,body "+ " ".join({args.where})
odb_output_nc='output.nc'

subprocess.call(['/home/martinezs/apps/public/bin/odbsql', '-q', sql_request,'-i',base_odb, '-f', 'unetcdf','-o', odb_output_nc ])

date_file = str(datetime.now().year)+str(datetime.now().month)+str(datetime.now().day)+"0000"

plot_size=1
#if not os.path.isfile(odb_output_nc):

if os.path.isfile(odb_output_nc):
    myfile = Dataset(odb_output_nc,'r')

    odb_key_val_dic = {}

    for variables in myfile.variables.keys():
        instrument_int = myfile[variables].odb_name[:myfile[variables].odb_name.index('@')]
        odb_key_val_dic[instrument_int] = myfile[variables][:]

    lat = odb_key_val_dic['lat']
    lon = odb_key_val_dic['lon']

    chan     = odb_key_val_dic['vertco_reference_1']

    obsvalue = odb_key_val_dic['obsvalue']

    fig = plt.figure(figsize =(20,20))
    vmin=min(obsvalue)#-50
    vmax=max(obsvalue)#50

    fig = plt.figure(figsize =(30,20))
    fontsize = 25
    labelsize = 20
    cmap = 'jet'#'binary'

    ax1 = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    ax1.coastlines()
    #stats = quickstats(datum_cld[ind_all])
    ax1.set_title('conv oper ', fontsize = 75)
    #plt.scatter(lon2print, lat2print, c=obs2print, cmap=cmap, vmin = vmin, vmax = vmax, s=plot_size, marker = '.')
    plt.scatter(lon, lat, c=obsvalue, cmap=cmap, vmin = vmin, vmax = vmax, s=plot_size, marker = '.')
    cbar1 = plt.colorbar(ax = ax1,fraction = 0.020)
    cbar1.ax.tick_params(labelsize=labelsize)
    figname=date_file  + '_OPER_conv_'+ "_".join({args.where})+'.png'
    plt.savefig(figname)
    plt.close()
    plt.Figure.clear
