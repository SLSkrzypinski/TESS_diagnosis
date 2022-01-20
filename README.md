# TESS_diagnosis

Now it is a GUI!

## Overview

This tool has been developed to find and validate periodic signals in *TESS* 2-minute cadence light curves. It allows the user to download the target pixel file (TPF) and light curve given a TIC number and *TESS* sector, implement the GLS periodogram on the data to find the stellar rotational period and phase-fold the light curve. 

It is possible to generate a one-page PDF summary with 
the obtained period and four figures:
1. TPF with TESS aperture mask
2. TESS light curve
3. Periodogram
4. Folded light curve

## Details

The TPF plot is created using a fork of the Python3 version of **tpf plotter** by J. Lillo-Box (publicly available in https://github.com/jlillo/tpfplotter), which also uses the Python packages **astropy**, **lightkurve** and **numpy**.

Periods are calculated using the **Generalised Lomb-Scargle** periodogram by M. Zechmeister (publicly available in https://github.com/mzechmeister/GLS). For this, photometric points which deviate more than 5 standard deviations from the average flux are removed, so the effect flares, transits or eclipses in the calculated rotational period is reduced. 

As TESS targets are observed at a 2 minute cadence and each sector is observed for 27 days, the periodogram will look for periods between about 4 minutes and about 13.5 days. 

The periodogram plot contains three horizontal lines corresponding to False Alarm Probabilities (FAP) of 10%, 1% and 0.1%. It also includes two vertical lines that mark the periods corresponding to double and half the period given by the main periodogram peak. 

The phase folded light curve plot is limited to points that deviate less than 10 standard deviations from the mean flux. Two dashed lines show the 5<img src="https://render.githubusercontent.com/render/math?math=\sigma"> limit used for the GLS. This is done to better show the star's variability.

## Requirements

**TESS_diagnosis** is written in Python3.8. The following packages need to be installed:
- **lightkurve** v2.0.11 (https://docs.lightkurve.org/index.html)
- **numpy**
- **matplotlib**
- **pandas**

Additionally, the GLS periodogram must be installed following the instructions given by its author: https://github.com/mzechmeister/GLS/tree/master/python.  

The GUI version (**TESSdiagnosis_GUI.py**) is constructed using **PySimpleGUI** v4.55.1 (https://github.com/PySimpleGUI/PySimpleGUI), so you must install it if you want to use the GUI. 

## How to use

Clone or download this folder. 

### GUI

To launch the GUI:

```
python3 TESSdiagnosis_GUI.py
```
There are four panels: the Target Pixel File, the Light Curve, the Periodogram and the Phase-folded Light Curve. 

Once you specified the TIC number and sector, click on "Dowload LC" to download the light curve and plot it in its corresponding panel. You can check both SAP and PDCSAP light curves. 

For the periodogram, you can change different parameters:
- Pbeg and Pend: the smallest and largest periods for the periodogram. The default values are calculated as twice the sampling rate and half of the total baseline.
- The standard deviation threshold used to remove outliers. The default value is 5.  
- The number of secondary peaks that will be marked. Secondary peaks too close to the main period are ignored. 

You can also select to perform the periodogram on the SAP or PDCSAP light curve. 

Once the periodogram is calculated, multiple results are shown:
- P: the period corresponding to the main peak.
- FAP: the false alarm probability of the main peak.
- 2P: the period corresponding to twice the main peak.
- P/2: the period corresponding to half the main peak.
- P_n: the period of the n-th peak found in the periodogram. 

After calculating the periodogram, the user can plot the phase-folded light curve using the periods P, 2P, P/2 and P_n by clicking on the "Fold" button in the Phase-folded LC panel. A tab with the name "P custom" allows to phase-fold the light curve using an arbitrary period (in days). 

The Target Pixel File panel allows to plot the TPF and the aperture mask used for the SAP and PDCSAP light curves. *Gaia* sources found in the field are also ploted, using circles of varying sizes depending on their magnitude. The user can introduce the following parameters:
- m_lim: the limiting magnitude for stars in the TPF to be ploted, compared to the target star. Defaults to 5.
- gaiaid: *Gaia* id number of the target. If it is not specified, the program will look for a *Gaia* identifier in the TIC catalog. 
- gaia mag: the *Gaia* g band magnitude of the target star. If it is not specified, the program will look for it in the TIC catalog. 

The results columns will show two values:
-FG_frac: the fraction of the *Gaia* g band flux corresponding to the target star compared to the sum of all stars found inside the aperture mask. 
-N_in: the number of sources found inside the aperture mask that are not the target star. 

### Terminal

If you just want to get the PDF repor, you can do it by typing:

```
python3 TESSdiagnosis.py {TIC} {sec}
```
where *TIC* and *sector* are the *TESS* Input Catalog ID of the star and *sec* the sector in which it was observed. 

As an example, FF And has the TIC number 26780244, which is in the 17th TESS sector. To generate the diagnosis pdf, we simply use the command line:

```
python TESS_diagnosis_main.py 267802440 17
```
The output pdf looks like this: 

![alt text](https://github.com/SLSkrzypinski/TESS_diagnosis/blob/master/EampleTIC267802440/TIC_267802440_S_17_summary.png)

Additionally, a csv file is created specifying the period, its error and its FAP. 

## Credits

If you use **TESS_diagnosis**, please cite:

- Skrzypinski, S. L, MSc thesis, Universidad Complutense de Madrid, 
Spain, 2021.

- Revilla, D., MSc thesis, Universidad Complutense de Madrid, Spain, 2020.

Besides you should also give credit to the authors of **tpfplotter** and **GLS**, 
and their papers:

- Aller, A., Lillo-Box, J., Jones, D., et al. (2020, A&A, 635, 128) "Planetary nebulae seen with TESS: Discovery of new binary central star candidates from Cycle 1," [ADS link](https://ui.adsabs.harvard.edu/abs/2020A%26A...635A.128A/abstract)

- M. Zechmeister & M. Kürster, The generalised Lomb-Scargle periodogram. A new formalism for the floating-mean and Keplerian periodograms, 2009, [ADS link](https://ui.adsabs.harvard.edu/abs/2009A%26A...496..577Z/abstract)


















