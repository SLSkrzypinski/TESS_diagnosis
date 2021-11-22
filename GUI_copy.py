import PySimpleGUI as sg
import functions as fn


# ----------------------------- Window setup ---------------------------------#

theme_dict = {'BACKGROUND': '#2B475D',
                'TEXT': '#FFFFFF',
                'INPUT': '#F2EFE8',
                'TEXT_INPUT': '#000000',
                'SCROLL': '#F2EFE8',
                'BUTTON': ('#000000', '#C2D4D8'),
                'PROGRESS': ('#FFFFFF', '#C7D5E0'),
                'BORDER': 1,'SLIDER_DEPTH': 0, 'PROGRESS_DEPTH': 0}

# sg.theme_add_new('Dashboard', theme_dict)     # if using 4.20.0.1+

sg.LOOK_AND_FEEL_TABLE['Dashboard'] = theme_dict
sg.theme('Dashboard')

BORDER_COLOR = '#C7D5E0'
DARK_HEADER_COLOR = '#1B2838'
BPAD_TOP = ((20,20), (20, 10))
BPAD_LEFT = ((20,10), (0, 10))
BPAD_LEFT_INSIDE = (0, 10)
BPAD_RIGHT = ((10,20), (10, 20))
BPAD_RIGHT_INSIDE = (0, 10)

top_block = [[sg.Text('TIC id',justification='l',font='Any 15'), sg.Input(key='-TICID-',size=20),
              sg.Text('TESS sector',font='Any 15'), sg.Input(key='-SECTOR-',size=10), 
              sg.Button('Download LC',key='-DownloadLC-'),sg.Button('Exit',key='-EXIT-')]]

TPF_block  = [[sg.Text('Target Pixel File', justification='c', font='Any 20')],
             [sg.Canvas(key='-TPF-')]]

#LC_block = [[sg.Text('Light Curve', font='Any 20', justification='c')],
#            [sg.Canvas(key='-LIGHTCURVE-')],]

LC_SAP_tab = [[sg.Text('SAP Light Curve', font='Any 20', justification='c')],
            [sg.Canvas(key='-SAP_LIGHTCURVE-')],]
LC_PDCSAP_tab = [[sg.Text('PDCSAP Light Curve', font='Any 20', justification='c')],
            [sg.Canvas(key='-PDC_LIGHTCURVE-')],]

Periodogram_block = [[sg.Text('Periodogram', font='Any 20')],
                      [sg.Canvas(key='-PERIODOGRAM-'),]]

Period_info = [[sg.Text('Parameters',font='Any 15')],
                [sg.Text('Pbeg'),sg.Input(size=10,key='-PBEG-')],
                [sg.Text('Pend'),sg.Input(size=10,key='-PEND-')],
                [sg.Text('\u03C3 out'),sg.Input('5',size=10,key='-OUTLIERS-',pad=(5,10))],
                [sg.Text('Np'),sg.Input('3',size=10,key='-NPEAKS-',pad=(17,10))],
                [sg.Radio('SAP', "FLUX_TYPE", default=False,key='-SAP_periodogram-')],
                [sg.Radio('PDCSAP', "FLUX_TYPE", default=True,key='-PDC_periodogram-')],
                [sg.Button('Get periodogram',key='-GET_PERIODOGRAM-')],
                [sg.Text('Information',font='Any 15')],
                [sg.InputText('',key='-BESTPERIOD-', use_readonly_for_disable=True, disabled=True,text_color=sg.theme_text_color())],
                [sg.InputText('',key='-FAP-', use_readonly_for_disable=True, disabled=True,text_color=sg.theme_text_color())],
                [sg.InputText('',key='-2P-' , use_readonly_for_disable=True, disabled=True,text_color=sg.theme_text_color())],
                [sg.InputText('',key='-P/2-', use_readonly_for_disable=True, disabled=True,text_color=sg.theme_text_color())],
                [sg.InputText('',key='-P_2-', use_readonly_for_disable=True, disabled=True,text_color=sg.theme_text_color())],
                [sg.InputText('',key='-P_3-', use_readonly_for_disable=True, disabled=True,text_color=sg.theme_text_color())],
                [sg.InputText('',key='-P_4-', use_readonly_for_disable=True, disabled=True,text_color=sg.theme_text_color())],
                ]

LCfolded_block = [[sg.Text('Phase-folded Light Curve', font='Any 20')],
            [sg.T('This is some random text')],
            [sg.T('This is some random text')],
            [sg.T('This is some random text')],
            [sg.T('This is some random text')],
            ]

folded_P1_tab = [[sg.Text('Phase folded Light Curve', font='Any 20',justification='c')],
                 [sg.Canvas(key='-LCFOLDED_P1-')]]
folded_P2_tab = [[sg.Text('Phase folded Light Curve', font='Any 20',justification='c')],
                 [sg.Canvas(key='-LCFOLDED_P2-')]]
folded_P3_tab = [[sg.Text('Phase folded Light Curve', font='Any 20',justification='c')],
                 [sg.Canvas(key='-LCFOLDED_P3-')]]
folded_P4_tab = [[sg.Text('Phase folded Light Curve', font='Any 20',justification='c')],
                 [sg.Canvas(key='-LCFOLDED_P4-')]]
folded_2P1_tab = [[sg.Text('Phase folded Light Curve', font='Any 20',justification='c')],
                 [sg.Canvas(key='-LCFOLDED_2P1-')]]
folded_P12_tab = [[sg.Text('Phase folded Light Curve', font='Any 20',justification='c')],
                 [sg.Canvas(key='-LCFOLDED_P12-')]]

layout = [[[sg.Column(top_block,size=(1720,50), pad=BPAD_TOP)],
           sg.Column([[sg.Column(TPF_block, size=(850,425), pad=BPAD_LEFT_INSIDE)],
                      [sg.Column(Periodogram_block, size=(690,425),pad=BPAD_LEFT_INSIDE),
                       sg.Column(Period_info,size=(155,425)),]],
                       pad=BPAD_LEFT, background_color=BORDER_COLOR),
           sg.Column([[sg.TabGroup([[sg.Tab('PDCSAP',LC_PDCSAP_tab, font='Any,25', key='-PDCSAP_LC-'),
                         sg.Tab('SAP', LC_SAP_tab,font='Any 10')]], key='-SAP_LC-', tab_location='top', size=(850,400), pad=BPAD_RIGHT_INSIDE)],
                      [sg.Column(LCfolded_block, size=(850,425), pad=BPAD_RIGHT_INSIDE)]], 
                       pad=BPAD_RIGHT, background_color=BORDER_COLOR)]]

window = sg.Window('TESS-diagnosis', layout, margins=(0,0), 
                   background_color=BORDER_COLOR, grab_anywhere=False,finalize=True)


selectable_text = ['-BESTPERIOD-','-FAP-','-2P-','-P/2-','-P_2-','-P_3-','-P_4-']
for key in selectable_text:
    window[key].Widget.config(readonlybackground=sg.theme_background_color())
    window[key].Widget.config(borderwidth=0)

# ---------------------------- End of window setup ---------------------------#

lc_file = None

# ------------------------------ Event loop ----------------------------------#

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
                print('Sector not specified. If multiple files are found, only' 
                      +'the first one will be downloaded')
                sg.Popup('Sector not specified. If multiple files are found, only' 
                      +'the first one will be downloaded',title='Warning',keep_on_top=True)
            else:
                sec = int(sec)
            lc_file = fn.download_lc(TIC,sec)
            if lc_file == None:
                # Warn if no light curve is found
                sg.Popup('Light curve for TIC {0} sector {1} not found'.format(TIC,sec), 
                         title='Warning',keep_on_top=True)
            else:
                fig_lc_pdc = fn.plot_lc(lc_file,'PDCSAP')
                fig_canvas_pdc = fn.draw_figure(window['-PDC_LIGHTCURVE-'].TKCanvas, fig_lc_pdc)
                fig_lc_sap = fn.plot_lc(lc_file,'SAP')
                fig_canvas_sap = fn.draw_figure(window['-SAP_LIGHTCURVE-'].TKCanvas, fig_lc_sap)
        except:
            # Error if invalid argument for TIC and/or sector
            print('Write valid TIC and sector (both must be integers)')
            sg.Popup('TIC and Sector must be integer values',
                     keep_on_top=True,title='Error')
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
                fig_canvas_per = fn.draw_figure(window['-PERIODOGRAM-'].TKCanvas, fig_period)
                periods, heights = fn.periodogram_peaks(periodogram,N_peaks=3)
                # Print periodogram information
                window['-BESTPERIOD-'].update('P={0} d'.format(round(best_period,4)))
                if round(fap,4) > 0:
                    window['-FAP-'].update('FAP={0}'.format(round(fap,4)))
                else:
                    window['-FAP-'].update('FAP<10^{-4}')
                window['-2P-'].update('2P={0} d'.format(round(2*best_period,4)))
                window['-P/2-'].update('P/2={0} d'.format(round(best_period/2,4)))
                
                for i in range(len(periods)):
                    window['-P_{0}-'.format(i+2)].update('P_{1}={0} d'.format(round(periods[i],4),i+2))                
            except:
                print('Use numerical values for parameters')
                sg.Popup('Use numerical values for parameters',title='Error',
                         keep_on_top=True )

        else:
            print('Get light curve first')
            sg.Popup('Get a light curve first',title='Warning',keep_on_top=True)

            
window.close()

# --------------------------- End of event loop ------------------------------#





