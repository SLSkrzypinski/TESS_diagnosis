import lightkurve as lk
import matplotlib.pyplot as plt
from matplotlib.figure import figaspect
import GLS


def get_arguments():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('tic',help='TIC number',action='store',type=str)
    parser.add_argument('sector',help='TESS source sector',action='store',type=str) 

    args = parser.parse_args()
    return args

def get_lc(tic,TESS_sector):
    print('Downloading and plotting light curve')
    lc_file = lk.search_lightcurvefile('TIC {0}'.format(tic),mission = 'TESS',sector = TESS_sector).download()
    lc = lc_file.PDCSAP_FLUX.remove_nans()
    flux = lc.flux
    time = lc.time
    w, h = figaspect(1/2)
    fig = plt.figure(figsize=(w,h))
    ax = fig.add_subplot(111)
    ax.set_xlabel('BJD-2457000',fontsize=14)
    ax.set_ylabel('Flux[$\mathrm{e^{-}\,s^{-1}}$]',fontsize=14)
    ax.scatter(time,flux,s=1.5,c='blue')
    plt.savefig('TIC_{0}_S_{1}_lc.png'.format(tic,TESS_sector))
    plt.close()
    return lc

def get_periodogram(lc):
    # Get periodogram
    print('Creating GLS periodogram')
    lc_period = lc.remove_outliers(sigma=5.0)
    time = list(lc_period.time)
    flux = list(lc_period.flux)
    error = list(lc_period.flux_err)
    Pbeg = 2*(time[1]-time[0])
    Pend = (max(time)-min(time))/2
    periodogram = GLS.Gls((time,flux,error),Pbeg=Pbeg,Pend=Pend)
    return periodogram, Pbeg, Pend
  
def draw_periodogram(periodogram,tic,TESS_sector,Pbeg=None,Pend=None):
    print('Plotting periodogram')
    best_period = periodogram.best['P']
    period_error = periodogram.best['e_P']
    fap = periodogram.FAP()
    FAP_levels = [0.1,0.01,0.001]
    linestyles = [':','dotted','solid']
    w, h = figaspect(1/1.5)
    fig = plt.figure(figsize=(w,h))
    ax = fig.add_subplot(111)
    ax.set_ylabel('Power (ZK)',fontsize=14)
    ax.set_xlabel('P [ d ]',fontsize=14)
    ax.set_xlim(Pbeg,Pend)
    period = 1/periodogram.freq
    power = periodogram.power
    max_power = power.max()
    power_levels = [[periodogram.powerLevel(i)]*len(period) for i in FAP_levels]
    ax.plot(period,power,'b-',linewidth=.8)
    for i in range(len(FAP_levels)):
        plt.plot(period,power_levels[i],linestyle=linestyles[i],linewidth=.8,c='red')
    plt.scatter(best_period,max_power,c='r',s=4,label='P={0} d'.format(round(best_period,4)))
    plt.legend(loc='best')
    ax.minorticks_on()
    plt.savefig('TIC_{0}_S_{1}_periodogram.png'.format(tic,TESS_sector))
    plt.close()

    return best_period,period_error,fap
  
def fold_lc(lc,best_period,tic,TESS_sector):
    print('Plotting phased LC')
    # Fold lightcurve               
    lc_folded = lc.fold(period=best_period).remove_outliers(sigma = 10)
    flux = lc_folded.flux
    phase = lc_folded.phase
    folded_5sig = lc_folded.remove_outliers(sigma = 5)
    sig5_lim = (max(folded_5sig.flux),min(folded_5sig.flux))
    w, h = figaspect(1/2)
    fig = plt.figure(figsize=(w,h))
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
    plt.savefig('TIC_{0}_S_{1}_lcfolded.png'.format(tic,TESS_sector))
    plt.close()
  
                      
def summary_pdf(tic,TESS_sector,best_period,period_error,fap):
    from fpdf import FPDF
    pdf = FPDF('L','mm','A4')
    pdf.set_font('Arial','B',16)
    pdf.set_text_color(125,125,125)
    pdf.add_page()
    pdf.cell(w=300,txt='TIC {0} sector {1} P_rot = ({2}'.format(tic,
             TESS_sector,round(best_period,4))+u'\u00b1'+'{0})d with FAP = {1}'.format(round(period_error,4),round(fap,4)))
    pdf.image('TIC_{0}_S_{1}_tpf.png'.format(tic,TESS_sector),w=100,h=85,x=20,y=20)
    pdf.image('TIC_{0}_S_{1}_lc.png'.format(tic,TESS_sector),w=165,h=85,x=120,y=20)
    pdf.image('TIC_{0}_S_{1}_periodogram.png'.format(tic,TESS_sector),w=110,h=85,x=20,y=110)
    pdf.image('TIC_{0}_S_{1}_lcfolded.png'.format(tic,TESS_sector),w=165,h=85,x=120,y=110)
    pdf.output('TIC_{0}_S_{1}_summary.pdf'.format(tic,TESS_sector))
