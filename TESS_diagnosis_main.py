
import functions as func
import pandas as pd
import os
import numpy as np

args = func.get_arguments()
TIC_list = np.array([args.tic])
TESS_sector_list = np.array([args.sector])

period_data = pd.DataFrame(columns=['TIC','TESS_sector','Period','error','FAP'])
# LC download and draw loop:
for i in range(len(TIC_list)):
    # The lightcurve file will be stored in a cache. 
    tic = int(TIC_list[i])
    TESS_sector = int(TESS_sector_list[i])
    print('Working on TIC {0}, sector {1}'.format(tic,TESS_sector))
    # Get light curve
    lc = func.get_lc(tic,TESS_sector)
    # Get periodogram
    periodogram, Pbeg, Pend = func.get_periodogram(lc)
    best_period, period_error, fap = func.draw_periodogram(periodogram,tic,TESS_sector,Pbeg=Pbeg,Pend=Pend)
    data = {'TIC':int(tic), 'TESS_sector':int(TESS_sector), 'Period':best_period,'error':period_error,'FAP':fap}
    period_data = period_data.append(data,ignore_index=True)
    # Fold lightcurve               
    func.fold_lc(lc,best_period,tic,TESS_sector)
    # Get TPF using Lillo's script
    print('Working on TPF')
    SAVE = '--SAVEGAIA' if args.FGratio else ''
    os.system('python3 tpfplotter_py3.py {0} --sector {1} --maglim 6 {2}'.format(tic,TESS_sector,SAVE))
    # Create summary pdf file
    if args.FGratio:
        GFrat = func.get_poll(tic)
        func.summary_pdf(tic,TESS_sector,best_period,period_error,fap,GFrat)
    else:
        func.summary_pdf(tic,TESS_sector,best_period,period_error,fap)
   
    os.remove('TIC_{0}_S_{1}_lc.png'.format(tic,TESS_sector))
    os.remove('TIC_{0}_S_{1}_periodogram.png'.format(tic,TESS_sector))
    os.remove('TIC_{0}_S_{1}_lcfolded.png'.format(tic,TESS_sector))
    os.remove('TIC_{0}_S_{1}_tpf.png'.format(tic,TESS_sector))
             
             
period_data.to_csv('Period_data_file.csv')
