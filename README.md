# Generate MC samples for the LFV Z analysis

## Setup

```
#move to clean directory
mkdir GenMC
cd GenMC
echo "Checking out 2016 CMSSW releases"
cmsrel CMSSW_8_0_28
cmsrel CMSSW_9_4_9
echo "Checking out 2017 CMSSW releases"
cmsrel CMSSW_9_3_4
cmsrel CMSSW_9_4_7
echo "Checking out 2018 CMSSW releases"
cmsrel CMSSW_10_2_18
echo "Checking out NanoAOD conversion CMSSW release"
cmsrel CMSSW_10_2_22

echo "Checking out generation configurations"
git clone git@github.com:michaelmackenzie/ZLFV_generation.git
for DIR in `ls -d CMSSW_*`; do
  cd ${DIR}/src/;
  ln -s ../../ZLFV_generation ZLFV_generation;
  cd -;
done
```

## Generating samples

Samples are generated using the Pythia event generator. Generation steps include `gen`, `reco`, `digi+hlt`, `mini`, and `nano` stages.
All nano generation from mini use: CMSSW_10_2_22
Put the correct cfgs in the folders.
Two scripts to run: for gen multicrab_Z_GENSIM.py; for everything else multicrab_Z_MultiStep.py

### 2016 MC generation
2016 generation uses:
gen-reco step: CMSSW_8_0_28
mini step: CMSSW_9_4_9

### 2017 MC generation
2017 generation uses:
gen step: CMSSW_9_3_4
reco-mini step: CMSSW_9_4_7

### 2018 MC generation
2018 generation uses:
gen-mini step: CMSSW_10_2_18





