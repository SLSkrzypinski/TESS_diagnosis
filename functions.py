import lightkurve as lk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import figaspect
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib
from GLS import Gls


#def get_arguments():
#    import argparse
#    parser = argparse.ArgumentParser()
#    parser.add_argument('tic',help='TIC number',action='store',type=str)
#    parser.add_argument('sector',help='TESS source sector',action='store',type=str) 
#    parser.add_argument('--FGratio',help='Save Gaia sources and get main source Gflux fraction', action='store')
#
#    args = parser.parse_args()
#    return args

def download_lc(tic,TESS_sector):
    print('Downloading light curve')
    if TESS_sector == '':
        lc_file = lk.search_lightcurvefile('TIC {0}'.format(tic),mission = 'TESS').download()
    else:
        lc_file = lk.search_lightcurvefile('TIC {0}'.format(tic),mission = 'TESS',sector = int(TESS_sector)).download()
    if lc_file == None:
        return None
    return lc_file

def plot_lc(lc_file,data_type):
    if data_type == 'PDCSAP':
        lc = lc_file.PDCSAP_FLUX.remove_nans()
    elif data_type == 'SAP':
        lc = lc_file.SAP_FLUX.remove_nans()
    flux = lc.flux.value
    time = lc.time.value
    w, h = figaspect(1/2)
    fig = matplotlib.figure.Figure(figsize=(w,h),dpi=75,facecolor='#2B475D')
    ax = fig.add_subplot(111)
    ax.set_xlabel('BJD-2457000',fontsize=14)
    ax.set_ylabel('Flux[$\mathrm{e^{-}\,s^{-1}}$]',fontsize=14)
    ax.scatter(time,flux,s=1.5,c='blue')
    fig.tight_layout()
    return fig

#def get_lc(tic,TESS_sector):
#    print('Downloading and plotting light curve')
#    lc_file = lk.search_lightcurvefile('TIC {0}'.format(tic),mission = 'TESS',sector = TESS_sector).download()
#    lc = lc_file.PDCSAP_FLUX.remove_nans()
#    flux = lc.flux.value
#    time = lc.time.value
#    w, h = figaspect(1/2)
#    fig = plt.figure(figsize=(w,h))
#    ax = fig.add_subplot(111)
#    ax.set_xlabel('BJD-2457000',fontsize=14)
#    ax.set_ylabel('Flux[$\mathrm{e^{-}\,s^{-1}}$]',fontsize=14)
#    ax.scatter(time,flux,s=1.5,c='blue')
#    plt.savefig('TIC_{0}_S_{1}_lc.png'.format(tic,TESS_sector))
#    plt.close()
#    return lc

def get_periodogram(lc,sigma=None,Pbeg=None,Pend=None):
    # Get periodogram
    print('Creating GLS periodogram')
    if sigma is not None:
        lc_period = lc.remove_outliers(sigma=sigma)
    else:
        lc_period = lc
    time = list(lc_period.time.value)
    flux = list(lc_period.flux.value)
    error = list(lc_period.flux_err.value)
    if Pbeg == None:
        Pbeg = 2*(time[1]-time[0])
    if Pend == None:
        Pend = (max(time)-min(time))/2
    periodogram = Gls((time,flux,error),Pbeg=Pbeg,Pend=Pend)
    return periodogram, Pbeg, Pend

def periodogram_peaks(periodogram,offset=0.1,N_peaks=3,relative_height=10):
    from scipy.signal import find_peaks
    x = 1/periodogram.freq
    y = periodogram.power
    P = periodogram.best['P']
    #Find peaks
    max_power = y.max()
    peaks = find_peaks(y,height=max_power/relative_height)
    #print(peaks)
    peak_pos = peaks[0]
    peak_pos=peak_pos[(x[peak_pos] < P-offset) | (x[peak_pos] > P+offset)]
    peak_pos=peak_pos[(x[peak_pos] < P/2-offset) | (x[peak_pos] > P/2+offset)]
    peak_pos=peak_pos[(x[peak_pos] < 2*P-offset) | (x[peak_pos] > 2*P+offset)]
    while len(peak_pos)>N_peaks:
        peak_pos = np.delete(peak_pos,peak_pos.argmin())
    periods = x[peak_pos]
    heights = y[peak_pos]
    return periods, heights#, peak_pos
    
#def peak_errs(periodogram):
#    p = periodogram.power
#    N = periodogram.


  
def plot_periodogram(periodogram,tic,TESS_sector,Pbeg=None,Pend=None,off=0.1,N=3):
    print('Plotting periodogram')
    color = plt.cm.tab20c(np.linspace(0, 1, 8))
    best_period = periodogram.best['P']
    period_error = periodogram.best['e_P']
    fap = periodogram.FAP()
    FAP_levels = [0.1,0.01,0.001]
    linestyles = [':','dotted','solid']
    w, h = figaspect(1/1.5)
    fig = plt.figure(figsize=(w,h),dpi=75,facecolor='#2B475D')
    ax = fig.add_subplot(111)
    ax.set_ylabel('Power (ZK)',fontsize=14)
    ax.set_xlabel('P [ d ]',fontsize=14)
    ax.set_xlim(Pbeg,Pend)
    period = 1/periodogram.freq
    power = periodogram.power
    max_power = power.max()
    power_levels = [[periodogram.powerLevel(i)]*len(period) for i in FAP_levels]
    peaks, heights = periodogram_peaks(periodogram, offset=off,N_peaks=N)
    ax.plot(period,power,'b-',linewidth=.8)
    for i in range(len(FAP_levels)):
        plt.plot(period,power_levels[i],linestyle=linestyles[i],linewidth=.8,c='red')
    plt.scatter(best_period,max_power,c='r',s=4,label='P={0} d'.format(round(best_period,4)))
    for i,c in zip(range(len(peaks)),color):
        plt.scatter(peaks[i],heights[i],c=c,s=4,label=r'P$_{0}$={1} d'.format(i+1,round(peaks[i],4)))
    plt.legend(loc='best')
    ax.minorticks_on()
    #plt.savefig('TIC_{0}_S_{1}_periodogram.png'.format(tic,TESS_sector))
    fig.tight_layout()
    plt.close()
    return fig,best_period,period_error,fap
  
def fold_lc(lc,best_period,tic=None,TESS_sector=None,sig=None):
    print('Plotting phased LC')
    # Fold lightcurve  
    lc_clean = lc.remove_outliers(sigma=10)
    lc_folded = lc_clean.fold(period=best_period,normalize_phase=True)#.remove_outliers(sigma = 10)
    flux = lc_folded.flux.value
    phase = lc_folded.phase.value#/(max(lc_folded.phase.value)-min(lc_folded.phase.value))
    lc_5sig = lc.remove_outliers(sigma=5)
    folded_5sig = lc_5sig.fold(period=best_period,normalize_phase=True)
    sig5_lim = (max(folded_5sig.flux.value),min(folded_5sig.flux.value))
    w, h = figaspect(1/2)
    fig = plt.figure(figsize=(w,h),dpi=75,facecolor='#2B475D')
    ax = fig.add_subplot(111)
    ax.set_xlabel('Phase',fontsize=14)
    ax.set_ylabel('Flux [$\mathrm{e^{-}\,s^{-1}}$]',fontsize=14)
    #ax.set_ylabel('Normalized Flux',fontsize=14)
    plt.scatter(phase,flux,s=2,c='red')
    ax.set_xlim(-1,1)
    ax.set_ylim(bottom=min(flux),top=max(flux))
    len_phase = len(phase)
    lim = int(len_phase/2)
    phase1 = phase[0:lim]
    phase1_shift = [p-phase[0]+phase[-1] for p in phase1]
    flux1 = flux[0:lim]
    phase2 = phase[lim:]
    phase2_shift = [p+phase[0]-phase[-1] for p in phase2]
    flux2 = flux[lim:]
    plt.scatter(phase2_shift,flux2,s=2,c='lightgrey')
    plt.scatter(phase1_shift,flux1,s=2,c='lightgrey')
    phase_shift = phase2_shift+phase1_shift
    for i in range(2):
        plt.plot(phase_shift,[sig5_lim[i]]*len(phase_shift),linewidth=.85,linestyle='dashed',color = 'lightgrey')
        plt.plot(phase,[sig5_lim[i]]*len(phase),linewidth=.85,linestyle='dashed',color='darkblue')
    #plt.savefig('TIC_{0}_S_{1}_lcfolded.png'.format(tic,TESS_sector))
    fig.tight_layout()
    plt.close()
    return fig
  
def get_poll(tic):
    import pandas as pd
    data_table = pd.read_table('Gaia_TIC{0}.dat'.format(tic),sep=' ')
    Gmag_principal = data_table.Gmag[0]
    mag = []
    for i in range(1,len(data_table)):
        if data_table.InAper[i] == 1:
            mag.append(data_table.Gmag[i])
    flux = [10**((Gmag_principal-m)/2.5) for m in mag]
    flux_fraction = 1/(sum(flux)+1)
    return flux_fraction

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

#def summary_pdf(tic,TESS_sector,best_period,period_error,fap,Gflux=None):
#    from fpdf import FPDF
#    pdf = FPDF('L','mm','A4')
#    pdf.set_font('Arial','B',16)
#    pdf.set_text_color(125,125,125)
#    pdf.add_page()
#    Gflux_frac = ' FG_ratio = {0}'.format(Gflux) if Gflux else ''
#    if round(fap,4) == 0.0:
#        pdf.cell(w=300,txt='TIC {0} sector {1} P_rot = ({2}'.format(tic,
#             TESS_sector,round(best_period,4))+u'\u00b1'+'{0})d with FAP < 0.0001 {1}'.format(round(period_error,4),
#             Gflux_frac))
#    else:                                                                                   
#        pdf.cell(w=300,txt='TIC {0} sector {1} P_rot = ({2}'.format(tic,
#             TESS_sector,round(best_period,4))+u'\u00b1'+'{0})d with FAP = {1}'.format(round(period_error,4),
#             round(fap,4))+Gflux_frac)
#    pdf.image('TIC_{0}_S_{1}_tpf.png'.format(tic,TESS_sector),w=100,h=85,x=20,y=20)
#    pdf.image('TIC_{0}_S_{1}_lc.png'.format(tic,TESS_sector),w=165,h=85,x=120,y=20)
#    pdf.image('TIC_{0}_S_{1}_periodogram.png'.format(tic,TESS_sector),w=110,h=85,x=20,y=110)
#    pdf.image('TIC_{0}_S_{1}_lcfolded.png'.format(tic,TESS_sector),w=165,h=85,x=120,y=110)
#    pdf.output('TIC_{0}_S_{1}_summary.pdf'.format(tic,TESS_sector))


def draw_figure_w_toolbar(canvas, fig, canvas_toolbar):
    if canvas.children:
        for child in canvas.winfo_children():
            child.destroy()
    if canvas_toolbar.children:
        for child in canvas_toolbar.winfo_children():
            child.destroy()
    figure_canvas_agg = FigureCanvasTkAgg(fig, master=canvas)
    figure_canvas_agg.draw()
    toolbar = Toolbar(figure_canvas_agg, canvas_toolbar)
    toolbar.update()
    figure_canvas_agg.get_tk_widget().pack(side='right', fill='both', expand=1)


class Toolbar(NavigationToolbar2Tk):
    def __init__(self, *args, **kwargs):
        super(Toolbar, self).__init__(*args, **kwargs)