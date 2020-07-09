# TESS_diagnosis

## Aims
Find Target Pixel Files and Lightcurves from TESS given a TIC number and a TESS sector. 
Implement GLS to find rotational periods.
Output a PDF summary with the obtained period and 4 figures:
  1. TPF with TESS apperture mask
  2. Lightcurve
  3. Periodogram
  4. Folded LC
The TPF file is created using the Python3 version of the **tpf plotter** script by @jlillo (https://github.com/jlillo/tpfplotter).
Periods are calculated using the Generalised Lomb-Scargle periodogram by @mzechmeister (https://github.com/mzechmeister/GLS) based on:

M. Zechmeister & M. Kürster, The generalised Lomb-Scargle periodogram. A new formalism for the floating-mean and Keplerian periodograms, 2009, [A&A, 496, 577](https://ui.adsabs.harvard.edu/abs/2009A%26A...496..577Z/abstract)

## Requirements
**TESS_diagnosis** is written in Python3.7 and uses the **lightkurve** package (https://docs.lightkurve.org/index.html). 

## How to use 
Clone or download this folder and use the command line: 

```
python TESS_diagnosis_main.py TIC SECTOR
```

Where TIC is the target TIC number and SECTOR its corresponding sector.



