# nuwinter
Code for WINTER neutrino follow-up


## Installing the package

* Clone the repository
```bash
git clone git@github.com:robertdstein/nuwinter.git
```
* Navigate to the repository
```bash
cd nuwinter
```
* Create a conda environment with the required packages
```bash
conda env create -c nuwinter python=3.11
```
* Activate the environment
```bash
conda activate nuwinter
```
* Install the package
```bash
pip install -e .
```

You might have trouble with the odd astronomy package (looking at you ligo-segments/lalsuite). If you do, you should try installing those dependencies with conda:
```bash
conda install -c conda-forge lalsuite
```

etc.