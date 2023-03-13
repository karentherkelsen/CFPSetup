CFPSetup
===================

CFPSetup is a directory that contains files for automatic cell-free protein synthesis (CFPS) assembly by OT-2 by Opentrons. This repository is aimed at researchers and scientists interested in automating CFPS experiments.


Documentation
=============

The CFPSetup contains two OT-2 python scripts that are pushed to the Opentrons software to run protocol.
Additionally, an accessory file is included for designing a full-factorial design for optimization.

## Content of the repository
1. `cfe_titration_curve.py`      - the protocol for OFAT design to optimize single reagents
2. `cfe_buffer_optimization.py`  - the protocol for 3^k full-factorial design to optimize three reagents simultanously
3. `DOE.py`                      - Accessory file to design full-factorial design
4. `README.md`


## Installation

Setting up PlasmidFinder program
```bash
# Go to the desired location for CFPSetup
cd /path/to/some/dir
# Clone the CFPSetup directory
git clone https://github.com/karentherkelsen/CFPSetup.git

```

## Dependencies
In order to run the program Python 3.10 (or newer) should be installed along with the following versions of the python packages (or newer).

#### Packages
- opentrons 6.0.1
- pandas 1.4.2
- doepy 0.0.1

## Usage

The protocols have user defined inputs in the beginning of all python scripts that can be adjusted
#### User inputs
1. `cfe_titration_curve.py`      - destination row in 384 well-plate
2. `cfe_buffer_optimization.py`  - Mg-glutamte, K-glutamate and PEG-8000 stock- and final concentrations
3. `DOE.py`                      - Mg-glutamte, K-glutamate and PEG-8000 final concentrations

To re-design the full-factorial experiment, run
```bash
python DOE.py 
```
Copy and paste the output to line 29-33 in cfe_buffer_optimization.py and update Mg-glutamate, K-glutamate, and PEG-8000 final concentrations.

The protocols can be simulated and saved in text files by
```bash
opentrons_simulate cfe_titration_curve.py > cfe_titration_curve_sim.txt
opentrons_simulate cfe_buffer_optimization.py > cfe_buffer_optimization_sim.txt
```

The final scripts can be pushed to the OT-2 robot using the Opentrons software. Please make sure to have the pipettes and deck calibrated before running the automatic CFPS assembly.

Overall, this repository simplifies and automates CFPS optimization and assembly, allowing researchers to focus on analysis and results.
