import os, sys
from censo.ensembledata import EnsembleData
from censo.configuration import configure
from censo.ensembleopt import Prescreening, Screening, Optimization
#from censo.properties import NMR
from censo.params import Config

##########
#CHECK FOR ACCURATE CHARGE AND MULT INPUTS
############

workdir = os.getcwd() # CENSO will put all files in this directory

for filename in os.listdir(workdir):

    if filename.lower().endswith('xyz'):
        input_path = os.path.join(workdir, filename) # path relative to the working directory

    if filename.lower().endswith('.censo2rc'):
        censorc_file = os.path.join(workdir, filename) # path relative to the working directory

ensemble = EnsembleData()
ensemble.read_input(input_path, charge=0, unpaired=0)

#If the user wants to use a specific rcfile:
configure(censorc_file)

# Get the number of available cpu cores on this machine
# This number can also be set to any other integer value and automatically checked for validity
#ncores = os.cpu_count()
Config.NCORES = 64


# Setup and run all the parts that the user wants to run
# Running the parts in order here, while it is also possible to use a custom order or run some parts multiple times
# Running a part will return an instance of the respective type
# References to the resulting part instances will be appended to a list in the EnsembleData object (ensemble.results)
# Note though, that currently this will lead to results being overwritten in your working directory
# (you could circumvent this by moving/renaming the folders)
# Running a part will return it's runtime in seconds
results, timings = zip(*[part.run(ensemble) for part in [Screening, Optimization]])

# You access the results using the ensemble object
# You can also find all the results the <part>.json output files
#print(ensemble.conformers[0].results["prescreening"]["sp"]["energy"])