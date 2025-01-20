#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  1 09:16:53 2023

@author: audouino
"""
import os

import numpy as np
from netCDF4 import Dataset

import cartopy.crs as ccrs
#import matplotlib
import matplotlib.pyplot as plt

#from mpl_toolkits.axes_grid1 import make_axes_locatable
#import cartopy.mpl.ticker as cticker

def count_non_zero(masked_array):
    non_zero_count = (np.ma.masked_not_equal(masked_array, 0)).count()
    return non_zero_count

dir_fig = "/home/chapeaul/CARTES/"

name_expe = "GZIO"
date_file = "20240603T0600A"
stage = "Observation"
inst = "conv"

#LFGDEP = True
LOBSVA = True

odb_output_nc = '/home/chapeaul/CARTES/output.nc'
#odb_output_nc = '/cnrm/obs/data1/audouino/NO_SAVE/ODBfiles/arpege/4dvarfr/GZEO/20241205T0000A/screening/GZEO.20241205T0000A.screening.fci.basic.nc'

plot_size=50
        
print('Ouverture du fichier',odb_output_nc)
    
if not os.path.isfile(odb_output_nc):
    print('pas de fichier '+odb_output_nc)
    
if os.path.isfile(odb_output_nc):
    myfile = Dataset(odb_output_nc,'r')
    
    odb_key_val_dic = {}
    for variables in myfile.variables.keys():
        instrument_int = myfile[variables].odb_name[:myfile[variables].odb_name.index('@')]
        odb_key_val_dic[instrument_int] = myfile[variables][:]

    lat = odb_key_val_dic['lat']
    lon = odb_key_val_dic['lon']
    
    chan     = odb_key_val_dic['vertco_reference_1']
    #fg_depar = odb_key_val_dic['fg_depar']
    #cld_fg_depar = odb_key_val_dic['cld_fg_depar']
    #tbclearr = odb_key_val_dic['tbclear']
    obsvalue = odb_key_val_dic['obsvalue']
    #biascorr = odb_key_val_dic['biascorr']
    #satid    = odb_key_val_dic['satellite_identifier']

#print(np.unique(cldne_1))
print(np.unique(lat))
#print(np.unique(chan))
    
    
##############################################################################
### FG DEPAR #################################################################
##############################################################################
    
       
#if LFGDEP:
#    
#    num_canal_list = np.unique(chan)
#        
#    for canal in num_canal_list:
#        #print('############# channel ', canal, file=f)
#        print('############# channel ', canal)
#        ind = np.where(chan == canal)
#        
#        field2print=fg_depar[ind]
#        
#        print('canal',canal,'fgdepar - min=',min(field2print),'max=',max(field2print))#, file=f)
#        fig = plt.figure(figsize =(20,20))
#            
#        vmin=min(field2print)#-50
#        vmax=max(field2print)#50
#        
#        fig = plt.figure(figsize =(30,20))
#        fontsize = 25
#        labelsize = 20
#        cmap = 'jet'#'binary'
#        
#        ax1 = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
#        ax1.coastlines()
#        #stats = quickstats(datum_cld[ind_all])
#        ax1.set_title('CY48 - fgdepar - Channel ' + str(canal), fontsize = 75)
#        plt.scatter(lon[ind], lat[ind], c=field2print, cmap=cmap, vmin = vmin, vmax = vmax, s=plot_size, marker = '.')
#        cbar1 = plt.colorbar(ax = ax1,fraction = 0.020)
#        cbar1.ax.tick_params(labelsize=labelsize)
#        figname=dir_fig+ name_expe + '_' +  date_file + '_' + stage + '_' + inst + '_' + str(canal) + '_fgdepar_All.png'
#        plt.savefig(figname)
#        plt.close()
#        plt.Figure.clear
#        print('Figure',figname,'créée !')
        
if LOBSVA:
    
    #num_canal_list = np.unique(chan)
        
    #for canal in num_canal_list:
    #print('############# channel ', canal, file=f)
    #print('############# channel ', canal)
    #ind = np.where(chan == canal)
     
    #field2print=obsvalue[ind]
    #field2print=obsvalue[1]
    #print('obsvalue ',field2print)
    
    #print('obsvalue - min=',min(field2print),'max=',max(field2print))#, file=f)
    fig = plt.figure(figsize =(20,20))
        
    #vmin=min(field2print)#-50
    #vmax=max(field2print)#50
    vmin=min(obsvalue)#-50
    vmax=max(obsvalue)#50

    print('vmin: ',vmin)
    print('vmax: ',vmax)

    fig = plt.figure(figsize =(30,20))
    fontsize = 25
    labelsize = 20
    cmap = 'jet'#'binary'
    
    ax1 = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    ax1.coastlines()
    #stats = quickstats(datum_cld[ind_all])
    ax1.set_title('CY48 - obsvalue  Channel ', fontsize = 75)
    plt.scatter(lon, lat, c=obsvalue, cmap=cmap, vmin = vmin, vmax = vmax, s=plot_size, marker = '.')
    cbar1 = plt.colorbar(ax = ax1,fraction = 0.020)
    cbar1.ax.tick_params(labelsize=labelsize)
    figname=dir_fig+ name_expe + '_' +  date_file  + '_obsvalue_All.png'
    print('figname: ',figname)
    plt.savefig(figname)
    plt.close()
    plt.Figure.clear
    print('Figure',figname,'créée !')
