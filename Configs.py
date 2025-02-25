# - Import Required Libraries
from collections import Counter, defaultdict
import matplotlib
import time
import json
import csv
import sys
import os

# - Set Matplotlib Backend
matplotlib.use('Agg')
# - Import Pyplot
import matplotlib.pyplot as plt

# - Data Headers
HEADERS = ["title", "citations", "year", "keywords", "journal", "publisher", "link1", "link2", "scholar"]

# - Data Directory Path
DATA_DIR = "Data/"
# - Data File
DATA_FILE = "papers_data.csv"
# - Json Data File
JSON_FILE = "papers.json"

# - Top Journals
TOP_N_JOURNALS = 40
# - Top Journals Plot Image Path
JOURNALS_PLOT = "journals.png"

# - Top Publishers
TOP_N_PUBLISHERS = 40
# - Top Publishers Plot Image Path
PUBLISHERS_PLOT = "publishers.png"

# - Top Keywords
TOP_N_KEYWORDS = 24
# - Top Keywords Per Years
TOP_N_KEYWORDS_PER_YEAR = 9
# - Trending Keywords Directory Path
TRENDING_KEYWORDS = "Trending/"
# - Top Keywords Plot Image Path
KEYWORDS_PLOT = "keywords.png"
# - Top Keywords Per Year Plot Image Path
KEYWORDS_PER_YEAR_PLOT = "keywords_per_year.png"
# - Keyword Synonyms
KEYWORD_SYNONYMS = {
    # - AI Titles
    "AI": ["machine learning", "deep learning", "mcmc", "monte carlo markov chain", "astrophysical inference", "gnns", "graph neural networks (gnns)", "convolutional neural network", "big data", "data-driven modeling", "large language models", "llm", "bayesian framework", "computational cost", "posterior distributions", "posterior inference", "inference", "generative model", "regression", "probabilistic modeling", "neural networks in astrophysics", "diffusion models", "machine learning in astrophysics", "statistical methods", "nested sampling", "machine learning in astronomy", "domain adaptation", "markov chain monte carlo", "monte carlo", "bayesian", "bayesian inference", "data processing", "supernova classification", "hierarchical modeling", "python", "posterior estimation", "anomaly detection", "astronomical data analysis", "python package", "model parameters", "forward modeling", "neural network", "hamiltonian monte carlo", "astrostatistics", "deep neural networks", "neural networks", "artificial intelligence", "ai", "nonlinear scales", "small scales", "bayesian neural networks", "parameter inference", "convolutional neural networks", "galaxy morphology classification", "statistical analysis", "covariance matrix", "missing data", "convolutional neural networks (cnns)", "cnns", "camels", "camels project", "graph", "gpu acceleration", "graph neural networks", "classification", "photometric classification", "galaxy classification", "variational inference", "astrophysical data analysis", "image processing", "astrophysics data analysis", "posterior sampling", "imaging", "posterior distribution", "mass estimation", "data analysis", "summary statistics", "likelihood-free inference", "computational efficiency"],
    # - Simulation Related
    "Simulation": ["simulation", "simulation techniques", "simulation analysis", "simulation predictions", "simulation algorithms", "numerical simulations", "n-body simulation", "simulation suites", "simulation training", "zoom-in simulations", "simulation-based inference", "simulation validation", "n-body simulations", "hydrodynamic simulations", "simulation training", "cosmological hydrodynamic simulations", "hydrodynamical simulations", "simulation results", "simulation comparison", "magnetohydrodynamic simulations", "simulations", "quijote simulations", "uncertainty quantifications", "uncertainty quantification", "uncertainty estimation"],
    # - Observation
    "Observation": ["observation", "observational", "observational data", "observational studies", "mock observations", "observational noise", "observational analysis", "astrophysical observations", "des", "observational results", "observational evidence", "observational constraints", "observational uncertaintes", "spectroscopic observations", "observational astronomy", "cosmological observations", "infrared observations", "ceers", "nirspec", "jwst", "james webb space telescope", "phangs", "phangs-jwst", "phangs jwst", "green bank telescope", "calibration", "subaru strategic program", "telescope instrumentation", "very large telescope", "saga survey", "photometric surveys", "3d-hst", "spectroscopic survey", "spt survey", "wide-field surveys", "atacama cosmology telescope", "euclid", "high-resolution observations", "green bank telescope", "gbt", "green bank telescope (gbt)", "high-resolution imaging", "hubble space telescope", "hubble space telescope (hst)", "alma observations", "south pole telescope", "south pole telescope (spt)", "spt", "deep-3600", "deap-3600", "spatial resolution", "observational cosmology", "high-contrast imaging", "sdss", "sdss-v", "alma", "nircam", "lsst", "astronomical surveys", "survey data", "pan-starrs1", "sloan digital sky survey", "desi", "rubin observatory", "vera c. rubin observatory", "karl g. jansky very large array", "candels", "candels survey", "hyper suprime-cam", "cosmic surveys", "spectroscopic data", "cosmological surveys", "roman space telescope", "nancy grace roman space telescope", "h3 survey", "atacama large millimeter/submillimeter array (alma)", "wide-field syrveys"],
    # - Astrophysics Related
    "Astrophysics": ["astronomy", "astrophysics", "luminosity", "astrophysical", "standard model", "h ii regions", "mass", "general relativity", "theoretical models", "theoretical predictions", "astrophysical parameters", "particle mass", "cold gas", "light curve", "astrophysical properties", "astrophysical processes", "physical parameters", "spectral lines", "near infrared", "near-infrared", "infrared emission", "near-infrared spectroscopy", "extreme adaptive optics", "parameter estimation", "parameter constraints", "astrophysical simulations", "astrophysical models", "modified gravity", "precision", "evolution", "astrophysical phenomena", "black hole mass", "astrophysical constraints", "rotation curves", "emission lines", "angular momentum", "astrophysical signatures", "astrophysical probes", "photometry", "light curves", "spectroscopic confirmation", "astrophysical modeling", "giant molecular clouds", "spectral energy distributions", "spectral energy distribution", "sed", "sed modeling", "molecular gas", "turbulence", "fundamental physics", "rotation periods", "effective field theory", "density profiles", "kinematics", "time-domain astronomy", "magnetic fields", "gas density", "gas surface density", "light curve", "radial velocity measurements", "chemical evolution", "co emission", "co (3-2)", "co (2-1)", "co (1-0)", "thermal evolution", "mechanical evolution", "chemical abundances", "abundance matching", "redshift range", "redshift distribution", "spectroscopic redshifts", "redshift", "high redshift", "matter power spectrum", "metallicity", "velocity dispersion", "spectroscopy", "temperature", "computational astrophysics", "wavefront correction", "photometric", "photometric redshifts", "redshifts", "redshift evolution", "radial velocity", "high-redshift", "massive neutrinos", "neutrino mass", "neutrino masses", "radio recombination lines (rrls)", "radio recombination line", "scatter", "particle", "particle physics", "molecular clouds"],
    # - Cosmology Related
    "Cosmology": ["cosmology", "cosmological", "power spectrum", "spectra", "surface gravity", "thermal history", "power spectra", "spectroscopid data", "mid-infrared", "cosmological parameters", "clustering", "cosmic microwave background", "cosmological simulations", "early universe", "cmb", "cosmic web", "universe expansion", "cosmic voids", "cosmological information", "polarization", "cross-correlation", "systematics", "systematic effects", "cosmic evolution", "cosmological constraints", "cosmic shear", "cosmic microwave background (cmb)", "cmb lensing", "strong gravitational lensing", "gravitational-wave astronomy", "weak gravitational lensing", "galaxy-galaxy lensing", "strong gravitational lenses", "merger trees", "cosmic structure formation", "structure growth", "cosmic structure", "substructure", "structure formation", "structure", "large-scale structure", "cosmological probes", "cosmological analysis", "cosmological observables", "hubble constant", "constraints", "cosmos field", "cosmic dawn", "reionization", "reionization history", "gaussian", "gaussian processes", "gaussian process", "gaussian process regression", "primordial non-gaussianity", "cmb-s4", "bispectrum", "weak lensing", "strong lensing", "cosmic rays", "cosmological inference", "planck", "planck data", "planck satellite", "small-scale structure", "cosmological models", "inflation", "baryons", "baryonic effects", "baryonic feedback", "baryonic physics", "cosmic time"],
    # - Dark Matter
    "Dark Matter and Dark Energy": ["dark matter", "dark matter halos", "halos", "warm dark matter", "host halo mass", "halo structure", "dark matter-dark energy interaction", "warm dark matter (wdm)", "wdm", "halo structures", "subhalo mass function", "halo finders", "snolab", "dark matter structure", "dark matter distribution", "dark matter substructure", "direct detection", "cold dark matter", "dark matter physics", "dark energy camera", "dark matter interactions", "dark matter halo", "dark energy survey", "dark matter properties", "dark matter models", "dark energy", "dark matter signatures", "self-interacting dark matter", "sidm", "dark matter detection", "cdm", "dark matter constraints", "matter clustering"],
    # - Galaxy Related
    "Galaxy": ["galaxy", "galaxies", "galactic", "galactic evolution", "galactic dynamics", "galactic halo", "host halo mass", "galaxy quenching", "galaxy growth", "local group", "galaxy catalogs", "galaxy detection", "dwarf galaxies", "dusty star-forming galaxies", "low-mass galaxies", "galaxy clustering", "star-forming galaxies", "galaxy evolution", "large magellanic cloud", "galaxy dynamics", "galaxy-halo connection", "lmc", "milky way analogs", "intergalactic medium", "galactic structure", "galaxy stellar masses", "late-type galaxies", "galaxy kinematics", "galactic morphology", "morphology", "galaxy morphology", "galaxy mergers", "galaxy merger", "galaxy assembly", "galaxy structure", "satellite galaxies", "galactic disk", "illustristng", "galactic formation", "galaxy formation", "galactic plane", "ism", "intestellar medium", "interstellar medium (ism)", "interstellar medium", "galaxy populations", "galactic properties", "galaxy properties", "central galaxies", "galactic surveys", "galaxy surveys", "circumgalactic medium", "galactic clusters", "galaxy cluster", "massive galaxies", "galaxy clusters", "agn", "agn feedback", "high-redshift galaxies", "milky way", "active galactic nuclei", "milky way satellites", "halo", "halo masses", "halo mass function", "halo properties", "halo mass", "gravitational waves", "gravitational lensing", "halo occupation distribution", "subhalos", "subhalo abundance", "subhalo properties", "halo catalogs", "halo evolution", "spiral arms", "nearby galaxies", "spiral galaxies"],
    # - Star Related
    "Stars": ["star", "stars", "stellar", "stellar evolution", "stellar properties", "white dwarf", "ultrafaint dwarf galaxies", "stellar mass functions", "star clusters", "young stars", "stellar age", "metal-poor stars", "stellar metallicity", "stellar populations", "stellar dynamics", "star-forming gas", "sun-like stars", "kepler mission", "stellar rotation periods", "star formation regulation", "stellar activity", "starspots", "supermassive black holes", "stellar formation", "stellar clusters", "stellar clusters", "stellar surveys", "star formation", "stellar masses", "stellar mass", "stellar mass function", "stellar parameters", "cosmic star formation", "star formation rates", "star formation rate", "white dwarfs", "sfr", "star formation rate (sfr)", "gaia", "gaia data", "gaia dr2", "gaia dr3", "gaia edr3", "quasars", "stellar halos", "stellar halo", "star-forming regions", "massive stars", "star formation efficiency", "stellar kinematics", "gyrochronology", "stellar rotation", "supernova", "cosmic star formation history", "type ia supernova", "type ii supernova", "type ia supernovae", "supernovae", "globular clusters", "stellar variability", "stellar ages", "stellar feedback", "star formation history", "m dwarfs", "red giant stars", "low-mass stars", "red giant branch stars"],
    # - Exoplanet Related
    "Exoplanets": ["exoplanet", "exoplanets", "exoplanet surveys", "exoplanet signatures", "exoplanet models", "exoplanet formation", "main-sequence stars", "exoplanet evolution", "exoplanet characterization", "exoplanet detection", "planetary signals", "tess", "tess (transiting exoplanet survey satellite)", "kepler", "astrometry", "star formation histories", "planet information", "transiting planets", "planet formation", "orbital periods", "orbital period", "k2", "k2 mission", "rotation period", "astrophysical transients", "orbital parameters"],
}

# - Reset Color
RESET = f'\033[0m'
# - Error Color
ERR = f'\033[38;2;255;200;0m'
# - Info Color
INFO = f'\033[38;2;106;140;150m'
# - Light Info Color
LIGHT_INFO = f'\033[38;2;106;106;150m'
# - RKPA Terminal Output
RKPA = f'\033[38;2;150;180;180m[RKPA]\033[0m'
# - Failed Terminal Output
FAILED = f'\033[38;2;255;0;0m[FAILED]\033[0m'
# - Success Terminal Output
SUCCESS = f'\033[38;2;0;255;0m[SUCCESS]\033[0m'
# - Warning Terminal Output
WARNING = f'\033[38;2;255;255;0m[WARNING]\033[0m'
# - Debug Terminal Output
DEBUG_INFO = f'\033[38;2;237;109;0m[DEBUG]\033[0m'
# - Analyzer Label
ANALYZER = f'\033[38;2;230;219;170m[ANALYZE]\033[0m'
# - Extractor Label
EXTRACTOR = f'\033[38;2;187;237;246m[EXTRACT]\033[0m'

# - Flag to Show Logs
SHOW_LOGS = True

# - Method to Print RKPA Logs
def printRKPA(*__input, **kargs):
    # - Check if force = True has been Passed
    if "force" in kargs:
        if kargs["force"] == True:
            # - Print Current Date and Time
            print(INFO + "(" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ")", end = ' ', flush = True)
            # - Check Parameters
            for arg in __input:
                print(arg, end = ' ', flush = True)
            # - Print New Line
            print()
            return
    # - Check if Logs are Enabled
    if SHOW_LOGS == False:
        return
    # - Print Current Date and Time
    print(INFO + "(" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ")", end = ' ', flush = True)
    # - Check Parameters
    for arg in __input:
        print(arg, end = ' ', flush = True)
    # - Print New Line
    print()
    return