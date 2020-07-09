# TESS_diagnosis

## Aims
Find Target Pixel Files and Lightcurves from TESS given a TIC list. 
Implement GLS to find rotational periods.
Output a PDF summary with obtained period and 4 figures:
  1. TPF with TESS apperture mask
  2. Lightcurve
  3. Periodogram
  4. Folded LC
The TPF file is created using the python 3 version of the **tpf plotter** script written by J.Lillo-Box (https://github.com/jlillo/tpfplotter).
Periods are calculated using the Generalised Lomb-Scargle periodogram (https://github.com/mzechmeister/GLS) based on:
M. Zechmeister & M. Kürster, The generalised Lomb-Scargle periodogram. A new formalism for the floating-mean and Keplerian periodograms, 2009, [A&A, 496, 577](https://ui.adsabs.harvard.edu/abs/2009A%26A...496..577Z/abstract)

## Requirenments
TESS_diagnosis is written in python 3.7 and uses the **lightkurve** package (https://docs.lightkurve.org/index.html) 
