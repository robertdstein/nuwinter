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


## Set up the environment

Copy .env.example to .env and fill in the details. You will need to get a WINTER API key from the WINTER team.


## Using the code

You will want to use jupyter notebooks. The rough order:

* plan_obs.ipynb to plan your observations
* download_data.ipynb to download the data
* analyse_data.ipynb to analyse the data using WINTER/ZTF
* analyse_data_winter_only.ipynb to analyse the data using WINTER only