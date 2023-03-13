#!/usr/bin/env python3
from doepy import build

################################################################################
#                     Design Full factorial experiment                         #
################################################################################

# Define the final concentrations of each factor for the experiment.
Mg_final_conc = [3,5,7,9,11,13,15]
K_final_conc = [60,75,90,105,120,135,150]
P_final_conc = [0,1,2,3,4,5,6]

# Note: copy these to update line 20-22 in cfe_buffer_optimization.py.

################################################################################

# Build a full factorial experiment using the specified parameters.
params = {"Mg-glutamate": Mg_final_conc, "K-glutamate": K_final_conc, "PEG-8000":P_final_conc}
ff = build.full_fact(params).sample(frac=1, random_state=1)
# Print out the design of experiments.
print("ff_dict = ")
print(ff.to_dict()) 

# Note: Copy this output to substitute line 29-33 in cfe_buffer_optimization.py.

# Outcomment the following line to export the DOE as a CSV file.
#ff.to_csv('DOE.csv')
