# Generate MC samples for the LFV Z analysis

## Setup

```
#move to clean directory
mkdir GenMC
cd GenMC
source /cvmfs/cms.cern.ch/cmsset_default.sh
source /cvmfs/cms.cern.ch/crab3/crab.sh
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

#### GENSIM:

Interactive processing:
```
source /cvmfs/cms.cern.ch/cmsset_default.sh
cd CMSSW_8_0_28/src
cmsenv
source /cvmfs/cms.cern.ch/crab3/crab.sh
voms-proxy-init --rfc --voms cms --hours 192
cd ZLFV_generation/cfg16/
cmsRun LFVAnalysis_<ZEMu/ZETau/ZMuTau>_13TeV_pythia8_GENSIM_<2016/2017/2018>_cfg.py
```

Submission through crab:
```
source /cvmfs/cms.cern.ch/cmsset_default.sh
cd CMSSW_8_0_28/src
cmsenv
source /cvmfs/cms.cern.ch/crab3/crab.sh
voms-proxy-init --rfc --voms cms --hours 192
cd ZLFV_generation/cfg16/
python ../multicrab_Z_GENSIM.py --year 2016 [--zemu] [--zetau] [--zmutau] [--dryrun] [--verbose]
```

#### DIGIHLT:

Interactive processing:
```
source /cvmfs/cms.cern.ch/cmsset_default.sh
cd CMSSW_8_0_28/src
cmsenv
source /cvmfs/cms.cern.ch/crab3/crab.sh
voms-proxy-init --rfc --voms cms --hours 192
cd ZLFV_generation/cfg16/
#FILE=<path to example 2016 GENSIM file>
FILE="/eos/cms/store/group/phys_smp/ZLFV/MC_generation/ZEMu_GENSIM_2016_no-zgamma-dev/LFVAnalysis_ZEMu_2016_no-zgamma-dev/LFVAnalysis_ZEMu_GENSIM_2016_no-zgamma-dev/230606_144833/0000/ZEMuAnalysis_pythia8_GENSIM_2016_1.root"
cp ${FILE} ./ZEMuAnalysis_pythia8_SIM_2016.root
cmsRun LFVAnalysis_13TeV_DIGIL1HLT_2016_cfg.py
```

Submission through crab:
```
source /cvmfs/cms.cern.ch/cmsset_default.sh
cd CMSSW_8_0_28/src
cmsenv
source /cvmfs/cms.cern.ch/crab3/crab.sh
voms-proxy-init --rfc --voms cms --hours 192
cd ZLFV_generation/cfg16/
python ../multicrab_Z_Multistep.py --year 2016 --step digihlt --input <path> [--zemu] [--zetau] [--zmutau] [--dryrun] [--verbose] [--tag <dataset tag>]
```

#### RECO:

Interactive processing:
```
source /cvmfs/cms.cern.ch/cmsset_default.sh
cd CMSSW_8_0_28/src
cmsenv
source /cvmfs/cms.cern.ch/crab3/crab.sh
voms-proxy-init --rfc --voms cms --hours 192
cd ZLFV_generation/cfg16/
#FILE=<path to example 2016 DIGIL1HLT file>
FILE="/eos/cms/store/group/phys_smp/ZLFV/MC_generation/ZEMu_DIGIL1HLT_no-zgamma-dev/CRAB_UserFiles/ZLFVAnalysis_DIGIL1HLT_no-zgamma-dev/230606_183941/0000/ZEMuAnalysis_pythia8_DIGIL1HLT_2016_1.root"
cp ${FILE} ./ZEMuAnalysis_pythia8_DIGIL1HLT_2016.root
cmsRun LFVAnalysis_13TeV_RECO_2016_cfg.py
```

Submission through crab:
```
source /cvmfs/cms.cern.ch/cmsset_default.sh
cd CMSSW_8_0_28/src
cmsenv
source /cvmfs/cms.cern.ch/crab3/crab.sh
voms-proxy-init --rfc --voms cms --hours 192
cd ZLFV_generation/cfg16/
python ../multicrab_Z_Multistep.py --year 2016 --step reco --input <path> [--zemu] [--zetau] [--zmutau] [--dryrun] [--verbose] [--tag <dataset tag>]
```

#### MINI:

Interactive processing:
```
source /cvmfs/cms.cern.ch/cmsset_default.sh
cd CMSSW_9_4_9/src
cmsenv
source /cvmfs/cms.cern.ch/crab3/crab.sh
voms-proxy-init --rfc --voms cms --hours 192
cd ZLFV_generation/cfg16/
#FILE=<path to example 2016 RECO file>
FILE="/eos/cms/store/group/phys_smp/ZLFV/MC_generation/ZEMu_RECO_no-zgamma-dev/CRAB_UserFiles/ZLFVAnalysis_RECO_no-zgamma-dev/230606_200048/0000/ZEMuAnalysis_pythia8_RECO_2016_1.root"
cp ${FILE} ./ZEMuAnalysis_pythia8_RECO_2016.root
cmsRun LFVAnalysis_13TeV_MINIAOD_2016_cfg.py
```

Submission through crab:
```
source /cvmfs/cms.cern.ch/cmsset_default.sh
cd CMSSW_9_4_9/src
cmsenv
source /cvmfs/cms.cern.ch/crab3/crab.sh
voms-proxy-init --rfc --voms cms --hours 192
cd ZLFV_generation/cfg16/
python ../multicrab_Z_Multistep.py --year 2016 --step mini --input <path> [--zemu] [--zetau] [--zmutau] [--dryrun] [--verbose] [--tag <dataset tag>]
```

#### MINI:

Interactive processing:
```
source /cvmfs/cms.cern.ch/cmsset_default.sh
cd CMSSW_10_2_22/src
cmsenv
source /cvmfs/cms.cern.ch/crab3/crab.sh
voms-proxy-init --rfc --voms cms --hours 192
cd ZLFV_generation/cfg16/
#FILE=<path to example 2016 MINIAOD file>
FILE="/eos/cms/store/group/phys_smp/ZLFV/MC_generation/ZEMu_MINI_no-zgamma-dev/CRAB_UserFiles/ZLFVAnalysis_MINI_no-zgamma-dev/230612_154033/0000/ZEMuAnalysis_pythia8_MINIAOD_2016_1.root"
cp ${FILE} ./ZEMuAnalysis_pythia8_MINIAOD_2016.root
cmsRun LFVAnalysis_13TeV_NANOAOD_2016_cfg.py
```

Submission through crab:
```
source /cvmfs/cms.cern.ch/cmsset_default.sh
cd CMSSW_10_2_22/src
cmsenv
source /cvmfs/cms.cern.ch/crab3/crab.sh
voms-proxy-init --rfc --voms cms --hours 192
cd ZLFV_generation/cfg16/
python ../multicrab_Z_Multistep.py --year 2016 --step nano --input <path> [--zemu] [--zetau] [--zmutau] [--dryrun] [--verbose] [--tag <dataset tag>]
```

### 2017 MC generation
2017 generation uses:
gen step: CMSSW_9_3_4
reco-mini step: CMSSW_9_4_7

#### GENSIM:
Follow the 2016 workflow, except using CMSSW_9_3_4

Submission through crab:
```
#setup enviroment, as described above
source /cvmfs/cms.cern.ch/cmsset_default.sh
cd ZLFV_generation/cfg17/
python ../multicrab_Z_GENSIM.py --year 2017 [--zemu] [--zetau] [--zmutau] [--dryrun] [--verbose]
```

### 2018 MC generation
2018 generation uses:
gen-mini step: CMSSW_10_2_18

#### GENSIM:
Follow the 2016 workflow, except using CMSSW_10_2_18

Submission through crab:
```
#setup enviroment, as described above
source /cvmfs/cms.cern.ch/cmsset_default.sh
cd ZLFV_generation/cfg18/
python ../multicrab_Z_GENSIM.py --year 2018 [--zemu] [--zetau] [--zmutau] [--dryrun] [--verbose]
```


### Useful CRAB information

Working directories are:
GEN: crab_projects/GEN<year>/xxx/

Output directories are by default at /store/group/phys_smp/ZLFV/MC_generation on eos

Check status of submitted jobs:
```
crab status -d <working directory> [--verboseErrors]
```
