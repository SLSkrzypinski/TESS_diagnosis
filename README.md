# TESS_diagnosis

## Aims
Find Target Pixel Files (TPF) and Lightcurves from TESS given a TIC number and a TESS sector. 
Implement GLS to find rotational periods.
Output a PDF summary with the obtained period and 4 figures:
  1. TPF with TESS apperture mask
  2. Light curve 
  3. Periodogram
  4. Folded LC
  
## Details

The TPF is created making use of the Python3 version of **tpf plotter** by J. Lillo-Box (publicly available in https://github.com/jlillo/tpfplotter), which also made use of the Python packages **astropy**, **lightkurve** and **numpy**.

The light curve is generated using the PDCSAP flux available. 

Periods are calculated using the **Generalised Lomb-Scargle** periodogram by M. Zechmeister (publicly available in https://github.com/mzechmeister/GLS).

As TESS targets are observed at a 2 minute cadence and each sector is observed for 27 days, the periodogram will look for periods between 4 minutes and 13.5 days. 

The periodogram plot contains three lines corresponding to False Alarm Probabilities (FAP) of 10%, 1% and 0.1%. 

## Requirements
**TESS_diagnosis** is written in Python3.7 and uses the **lightkurve** package (https://docs.lightkurve.org/index.html). 

## How to use 
Clone or download this folder. 

As an example, FF And has the TIC number 26780244, which is in the 17th TESS sector. To generate the diagnosis pdf, we simply use the command line:

```
python TESS_diagnosis_main.py 267802440 17
```
The output pdf looks like this: 

![alt text](https://github.com/SLSkrzypinski/TESS_diagnosis/blob/master/TIC_267802440_S_17_summary.png)

Additionally, a csv file is created specifying the period, its error and its FAP. 


## Future additions

Future releases will add the option to specify the flux fraction which corresponds to the target source making use of the --SAVEGAIA opion built in the **tpfplotter** script. 

An option will be added so the user would be able to input a TIC and sector list with all the sources desired. 

We will add an option to download and combine multiple sector light curves for the same star. This way, the user would be able to find periods greater than 13.5 days.

## Credits

If you use **TESS_diagnosis**, please give credit to the authors of **tpfplotter** and **GLS** and their papers:

- Aller, A., Lillo-Box, J., Jones, D., et al. (2020, A&A, 635, 128) "Planetary nebulae seen with TESS: Discovery of new binary central star candidates from Cycle 1," [ADS ling](https://ui.adsabs.harvard.edu/abs/2020A%26A...635A.128A/abstract)

- M. Zechmeister & M. Kürster, The generalised Lomb-Scargle periodogram. A new formalism for the floating-mean and Keplerian periodograms, 2009, [ADS link](https://ui.adsabs.harvard.edu/abs/2009A%26A...496..577Z/abstract)

Go to the original authors' repositories linked above for further details. 
