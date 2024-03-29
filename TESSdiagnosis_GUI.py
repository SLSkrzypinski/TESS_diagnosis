"""
MIT License

Copyright (c) 2022 Sebastián López Skrzypinski and Daniel Revilla

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""

import PySimpleGUI as sg
import functions as fn
import tpfplotter
import warnings

# ----------------------------- Window setup ---------------------------------#

theme_dict = {'BACKGROUND': '#323431',
                'TEXT': '#FFFFFF',
                'INPUT': '#F2EFE8',
                'TEXT_INPUT': '#000000',
                'SCROLL': '#F2EFE8',
                'BUTTON': ('#000000', '#C2D4D8'),
                'PROGRESS': ('#FFFFFF', '#C7D5E0'),
                'BORDER': 2,'SLIDER_DEPTH': 0, 'PROGRESS_DEPTH': 0}

# sg.theme_add_new('Dashboard', theme_dict)     # if using 4.20.0.1+

sg.LOOK_AND_FEEL_TABLE['Dashboard'] = theme_dict
sg.theme('Dashboard')


BORDER_COLOR = '#81827b'
DARK_HEADER_COLOR = '#1B2838'
BPAD_TOP = ((20,20), (20, 10))
BPAD_LEFT = ((20,10), (0, 10))
BPAD_LEFT_INSIDE = (0, 10)
BPAD_RIGHT = ((10,20), (10, 20))
BPAD_RIGHT_INSIDE = (0, 10)

# Top Block setup
top_block = [[sg.Text('TIC id',justification='l',font='Any 15'), sg.Input(key='-TICID-',size=20),
              sg.Text('TESS sector',font='Any 15'), sg.Input(key='-SECTOR-',size=10), 
              sg.Button('Download LC',key='-DownloadLC-'),sg.Button('Exit',key='-EXIT-')]]

# Target Pixel File block setup
TPF_block = [[sg.Text('Target Pixel File', justification='c', font='Any 20')],
             [sg.Canvas(key='-TPF-',size=(700,700),pad=(0,20))]]
TPF_params = [[sg.Text('Parameters',font='Any 15')],
               [sg.T('m_lim'),sg.Input(size=10,key='-MLIM-')],
               [sg.T('gaiaid'),sg.Input(size=10,key='-GID-')],
               [sg.T('gaia mag'),sg.Input(size=10,key='-GMAG-')],
               [sg.Checkbox('Clear params',default=True,key='-CLEAR_TPF-')],
               [sg.Button('Get TPF',key='-GET_TPF-')],
               ]
TPF_info = [[sg.T('Results',font='Any 15')],
             [sg.InputText('',key='-GFRAC-',use_readonly_for_disable=True,disabled=True,text_color=sg.theme_text_color())],
             [sg.InputText('',key='-Nin-',use_readonly_for_disable=True,disabled=True,text_color=sg.theme_text_color())]]


# Light Curve block setup
LC_SAP_tab = [[sg.Text('SAP Light Curve', font='Any 20', justification='c')],
            [sg.Canvas(key='-SAP_LIGHTCURVE-')],]
LC_PDCSAP_tab = [[sg.Text('PDCSAP Light Curve', font='Any 20', justification='c')],
            [sg.Canvas(key='-PDC_LIGHTCURVE-')],]

# Periodogram block setup
Periodogram_block = [[sg.Text('Periodogram', font='Any 20'),sg.Canvas(key='CONTROLS_Periodogram')],
                      [sg.Canvas(key='-PERIODOGRAM-',size=(525,350),pad=(10,0)),]]
Period_params = [[sg.Text('Parameters',font='Any 15')],
                [sg.Text('Pbeg'),sg.Input(size=10,key='-PBEG-')],
                [sg.Text('Pend'),sg.Input(size=10,key='-PEND-')],
                [sg.Text('\u03C3 out'),sg.Input('5',size=10,key='-OUTLIERS-',pad=(5,10))],
                [sg.Text('Np'),sg.Input('3',size=10,key='-NPEAKS-',pad=(17,10))],
                [sg.Radio('SAP', "FLUX_TYPE", default=False,key='-SAP_periodogram-')],
                [sg.Radio('PDCSAP', "FLUX_TYPE", default=True,key='-PDC_periodogram-')],
                [sg.Button('Get periodogram',key='-GET_PERIODOGRAM-')],
                ]
Period_info = [[sg.Text('Results',font='Any 15')],[sg.InputText('',key='-BESTPERIOD-', use_readonly_for_disable=True, disabled=True,text_color=sg.theme_text_color())],
                [sg.InputText('',key='-FAP-', use_readonly_for_disable=True, disabled=True,text_color=sg.theme_text_color())],
                [sg.InputText('',key='-2P-' , use_readonly_for_disable=True, disabled=True,text_color=sg.theme_text_color())],
                [sg.InputText('',key='-P/2-', use_readonly_for_disable=True, disabled=True,text_color=sg.theme_text_color())],
                [sg.InputText('',key='-P_2-', use_readonly_for_disable=True, disabled=True,text_color=sg.theme_text_color())],
                [sg.InputText('',key='-P_3-', use_readonly_for_disable=True, disabled=True,text_color=sg.theme_text_color())],
                [sg.InputText('',key='-P_4-', use_readonly_for_disable=True, disabled=True,text_color=sg.theme_text_color())],
                ]

# Phase-folded Light Curve block setup
folded_P1_tab = [[sg.Text('Phase-folded LC P', font='Any 20',justification='c'),sg.Button('Fold',key='-FOLD1-')],
                 [sg.Canvas(key='-LCFOLDED_P1-')]]
folded_P2_tab = [[sg.Text('Phase-folded LC P2', font='Any 20',justification='c'),sg.Button('Fold',key='-FOLD2-')],
                 [sg.Canvas(key='-LCFOLDED_P2-')]]
folded_P3_tab = [[sg.Text('Phase-folded LC P3', font='Any 20',justification='c'),sg.Button('Fold',key='-FOLD3-')],
                 [sg.Canvas(key='-LCFOLDED_P3-')]]
folded_P4_tab = [[sg.Text('Phase-folded LC P4', font='Any 20',justification='c'),sg.Button('Fold',key='-FOLD4-')],
                 [sg.Canvas(key='-LCFOLDED_P4-')]]
folded_2P1_tab = [[sg.Text('Phase-folded LC 2P', font='Any 20',justification='c'),sg.Button('Fold',key='-FOLD5-')],
                 [sg.Canvas(key='-LCFOLDED_2P1-')]]
folded_P12_tab = [[sg.Text('Phase-folded LC P/2', font='Any 20',justification='c'),sg.Button('Fold',key='-FOLD6-')],
                 [sg.Canvas(key='-LCFOLDED_P12-')]]
folded_Pc_tab = [[sg.Text('Phase-folded LC Custom P', font='Any 20',justification='c'),sg.Input(key='-CUSTOM_P-',size=15),sg.Button('Fold',key='-FOLD_CUSTOM-')],
                 [sg.Canvas(key='-LCFOLDED_Pc-')]]

Fold_events = ['-FOLD{0}-'.format(i) for i in range(1,7)]

# Window layout created using the previous setups
layout = [[[sg.Column(top_block,size=(1720,50), pad=BPAD_TOP)],
           sg.Column([[sg.Column(TPF_block, size=(530,425), pad=BPAD_LEFT_INSIDE),
                       sg.Column(TPF_info,size=(155,425)),
                       sg.Column(TPF_params,size=(155,425),pad=BPAD_LEFT_INSIDE)],
                      [sg.Column(Periodogram_block, size=(530,425),pad=BPAD_LEFT_INSIDE),
                       sg.Column(Period_info,size=(155,425)),sg.Column(Period_params,size=(155,425),pad=BPAD_LEFT_INSIDE)]],
                       pad=BPAD_LEFT, background_color=BORDER_COLOR),
           sg.Column([[sg.TabGroup([[sg.Tab('PDCSAP',LC_PDCSAP_tab, font='Any,25', key='-PDCSAP_LC-'),
                         sg.Tab('SAP', LC_SAP_tab,font='Any 10',key='-SAP_LC-')]], key='-LC-', tab_location='top', size=(850,400), pad=BPAD_RIGHT_INSIDE)],
                      [sg.TabGroup([[sg.Tab('P',folded_P1_tab, font='Any,25', key='-FoldedP1-'),
                         sg.Tab('2P', folded_2P1_tab,font='Any 10',key='-Folded2P-'),
                         sg.Tab('P/2', folded_P12_tab,font='Any 10',key='-FoldedP/2-'),
                         sg.Tab('P2', folded_P2_tab,font='Any 10',key='-FoldedP2-'),
                         sg.Tab('P3', folded_P3_tab,font='Any 10',key='-FoldedP3-'),
                         sg.Tab('P4', folded_P4_tab,font='Any 10',key='-FoldedP4-'),
                         sg.Tab('P custom', folded_Pc_tab,font='Any 10',key='-FoldedPc-')]], key='-FOLDEDLC-', tab_location='top', size=(850,400), pad=BPAD_RIGHT_INSIDE)]], 
                       pad=BPAD_RIGHT, background_color=BORDER_COLOR)]]

window = sg.Window('TESS-diagnosis', layout, margins=(0,0), 
                   background_color=BORDER_COLOR, grab_anywhere=False,finalize=True)

# Make some texts selectable
selectable_text = ['-BESTPERIOD-','-FAP-','-2P-','-P/2-','-P_2-','-P_3-','-P_4-','-GFRAC-','-Nin-']
for key in selectable_text:
    window[key].Widget.config(readonlybackground=sg.theme_background_color())
    window[key].Widget.config(borderwidth=0)

# --------------------------- End of window setup --------------------------- #

# Set some defaults 

lc_file = None
periodogram = None

# ------------------------------ Event loop --------------------------------- #

while True:             
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == '-EXIT-':
        break
    if event == '-DownloadLC-':
        # Download light curve when user clicks on "Download LC" button
        try:
            # Check if values are correct
            TIC = int(values['-TICID-'])
            sec = values['-SECTOR-']
            if sec == '':
                warnings.warn('Sector not specified. If multiple files are found, only' 
                      +'the first one will be downloaded',Warning)
                sg.Popup('Sector not specified. If multiple files are found, only' 
                      +'the first one will be downloaded',title='Warning',keep_on_top=True)
            else:
                sec = int(sec)
            lc_file = fn.download_lc(TIC,sec)
            if lc_file is None:
                # Warn if no light curve is found
                warnings.warn('Light curve for TIC {0} sector {1} not found'.format(TIC,sec),Warning)
                sg.Popup('Light curve for TIC {0} sector {1} not found'.format(TIC,sec), 
                         title='Warning',keep_on_top=True)
            else:
                fig_lc_pdc = fn.plot_lc(lc_file,'PDCSAP')
                fig_canvas_pdc = fn.draw_figure(window['-PDC_LIGHTCURVE-'].TKCanvas, fig_lc_pdc)
                fig_lc_sap = fn.plot_lc(lc_file,'SAP')
                fig_canvas_sap = fn.draw_figure(window['-SAP_LIGHTCURVE-'].TKCanvas, fig_lc_sap)
        except:
            # Warn if invalid argument for TIC and/or sector
            warnings.warn('Write valid TIC and sector (both must be integers)',Warning)
            sg.Popup('TIC and Sector must be integer values',
                     keep_on_top=True,title='Warning')
    elif event == '-GET_PERIODOGRAM-':
        # Calculate periodogram when user clicks on "Get periodogram" button
        if lc_file is not None:
            if values['-SAP_periodogram-']:
                lc = lc_file.SAP_FLUX.remove_nans()
            elif values['-PDC_periodogram-']:
                lc = lc_file.PDCSAP_FLUX.remove_nans()
            # Error if non numerical values are inserted
            params = (values['-OUTLIERS-'],values['-PBEG-'],values['-PEND-'],values['-NPEAKS-'])
            try:
                params = [float(p) if p != '' else None for p in params]
                sig = params[0]
                Pbeg = params[1]
                Pend = params[2]
                Npeaks = int(params[3])
                # Calculate periodogram with inserted parameters
                periodogram, Pbeg, Pend = fn.get_periodogram(lc,sigma=sig,
                                                                      Pbeg=Pbeg,Pend=Pend)
    
                window['-PBEG-'].update(Pbeg)
                window['-PEND-'].update(Pend)
                # Plot periodogram
                fig_period,best_period,period_error,fap = fn.plot_periodogram(periodogram,
                                                                  TIC,sec,Pbeg=Pbeg,Pend=Pend,N=Npeaks)
                DPI = fig_period.get_dpi()
                fig_period.set_size_inches(360*1.5 / float(DPI), 360 / float(DPI))
                fn.draw_figure_w_toolbar(window['-PERIODOGRAM-'].TKCanvas, fig_period, window['CONTROLS_Periodogram'].TKCanvas)
                #fig_canvas_per = fn.draw_figure(window['-PERIODOGRAM-'].TKCanvas, fig_period)
                periods, heights = fn.periodogram_peaks(periodogram,N_peaks=3)
                # Print periodogram information
                window['-BESTPERIOD-'].update('P={0} d'.format(round(best_period,4)))
                if round(fap,4) > 0:
                    window['-FAP-'].update('FAP={0}'.format(round(fap,4)))
                else:
                    window['-FAP-'].update('FAP<10^{-4}')
                window['-2P-'].update('2P={0} d'.format(round(2*best_period,4)))
                window['-P/2-'].update('P/2={0} d'.format(round(best_period/2,4)))
                
                i = 0 
                while i <= len(periods)-1 and i < 4:
                    window['-P_{0}-'.format(i+2)].update('P_{1}={0} d'.format(round(periods[i],4),i+2))
                    i += 1
            except:
                warnings.warn('Use numerical values for parameters',Warning)
                sg.Popup('Use numerical values for parameters',title='Warning',
                         keep_on_top=True )

        else:
            warnings.warn('No light curve was downloaded.',Warning)
            sg.Popup('No light curve was downloaded.',title='Warning',keep_on_top=True)
    
    elif event in Fold_events:
        # Fase fold light curve with obtained periods
        if periodogram is not None:
            fig_P1 = fn.fold_lc(lc, best_period)
            fig_canvas_P1 = fn.draw_figure(window['-LCFOLDED_P1-'].TKCanvas, fig_P1)
            fig_2P1 = fn.fold_lc(lc, 2*best_period)
            fig_canvas_2P1 = fn.draw_figure(window['-LCFOLDED_2P1-'].TKCanvas, fig_2P1)
            fig_P12 = fn.fold_lc(lc, best_period/2)
            fig_canvas_P12 = fn.draw_figure(window['-LCFOLDED_P12-'].TKCanvas, fig_P12)
            
            figs_P = []
            fig_canvas_Ps = []
            i = 0
            while i <= len(periods)-1 and i < 4:
                figs_P.append(fn.fold_lc(lc,periods[i]))
                i += 1
            for i in range(len(figs_P)):
                fig_canvas_Pn = fn.draw_figure(window['-LCFOLDED_P{0}-'.format(i+2)].TKCanvas, figs_P[i])
                fig_canvas_Ps.append(fig_canvas_Pn)
        else:
            warnings.warn('Create a periodogram first',Warning)
            sg.Popup('Create a periodogram first',title='Warning',keep_on_top=True)
    elif event == '-FOLD_CUSTOM-':
        try:
            custom_period = float(values['-CUSTOM_P-'])
            fig_Pcustom = fn.fold_lc(lc, custom_period)
            fig_canvas_Pc = fn.draw_figure(window['-LCFOLDED_Pc-'].TKCanvas, fig_Pcustom)
        except:
            warnings.warn('The custom period must be numerical',Warning)
            sg.Popup('The custom period must be numerical',title='Warning',
                     keep_on_top=True)
    elif event == '-GET_TPF-':
        if values['-CLEAR_TPF-']==True:
            window['-GID-'].update('')
            window['-MLIM-'].update('')
            window['-GMAG-'].update('')
            values['-GID-'] = ''
            values['-MLIM-'] = ''
            values['-GMAG-'] = ''
        try:
            TIC = values['-TICID-']
            sec = values['-SECTOR-']
            # Get values
            info_tpf = [values['-GID-'],values['-MLIM-'],values['-GMAG-']]
            tpf_params = [int(p) if p != '' else None for p in info_tpf]
            if tpf_params[1] == None:
                tpf_params[1] = 5
            fig_tpf, data_tpf = tpfplotter.tpfplotter(str(TIC),sector=str(sec),
                                                      gid=tpf_params[0],gmag=tpf_params[2],maglim=tpf_params[1],SAVEGAIA=True)
            fig_canvas_tpf = fn.draw_figure(window['-TPF-'].TKCanvas,fig_tpf)
            FG_frac, Gmag, Gid, Nin = fn.get_poll(data_tpf)
            window['-GFRAC-'].update('FG_frac = {0}'.format(round(FG_frac,4)))
            window['-Nin-'].update('N_in = {0}'.format(Nin))
            window['-GMAG-'].update(Gmag)
            window['-GID-'].update(Gid)
            window['-MLIM-'].update(tpf_params[1])
        except:
            warnings.warn('TPF not found.',Warning)
            sg.Popup('TPF not found',title='Warning',keep_on_top=True)
window.close()

# --------------------------- End of event loop ------------------------------#





