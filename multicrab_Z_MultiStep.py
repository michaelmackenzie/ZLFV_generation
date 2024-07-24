from CRABAPI.RawCommand import crabCommand
from WMCore.Configuration import Configuration
from CRABClient.UserUtilities import config
import os
import sys
import argparse

lfn_path = '/store/group/phys_smp/ZLFV/MC_generation' #no "/" in end

# step ="mini" # (digi, hlt OR digihlt), reco, mini, nano [digi, hlt only for 2017 digihlt for 16 18]


config = Configuration()

config.section_('General')
config.General.transferOutputs = True

config.section_('JobType')
config.JobType.pluginName = 'Analysis'
config.JobType.allowUndistributedCMSSW = True


config.section_('Data')
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
config.Data.publication = False


config.section_('Site')
config.Site.storageSite = 'T2_CH_CERN'


def list_of_files(path, subset = -1, subset_size = 2000):
  files= subprocess.check_output(["ls", path]).splitlines()
  eos_path = path
  eos_path = eos_path.replace('/eos/cms', '')
  eos_path = eos_path.replace('/eos/uscms', '')
  outfiles=[]
  for line in files:
    if "root" in line:
      outfiles.append(eos_path+line)
  if subset >= 0:
    outfiles.sort()
    nfiles = len(outfiles)
    nstart = subset_size*subset
    nfinish = min(nfiles, subset_size*(subset+1))
    if nstart >= nfiles:
      print "Subset %i with size %i not defined for input list size %i" % (subset, subset_size, nfiles)
      exit()
    outfiles = outfiles[nstart:nfinish]
  return outfiles



if __name__ == '__main__':

    p = argparse.ArgumentParser(description='Submit MC generation jobs')

    # Signal selection
    p.add_argument('--zemu'   , help='Submit Z->e+mu generation'  , action='store_true', required=False)
    p.add_argument('--zetau'  , help='Submit Z->e+tau generation' , action='store_true', required=False)
    p.add_argument('--zmutau' , help='Submit Z->mu+tau generation', action='store_true', required=False)

    # Job configuration
    p.add_argument('--step'   , help='Generation step: digi, hlt, digihlt, reco, mini, or nano ', required=True)
    p.add_argument('--input'  , help='Input dataset path', required=True)
    p.add_argument('--year'   , help='Sample year', required=True)
    p.add_argument('--tag'    , help='Output dataset tag', default="", required=False)

    # Processing subsamples if requested
    p.add_argument('--subset_size', help='N(files) to process in a separate subset', default=2000, type=int, required=False)
    p.add_argument('--subset'     , help='Subset number to submit', default=-1, type=int, required=False)

    # Debug options
    p.add_argument('--dryrun' , help='Setup merging without running', action='store_true', required=False)
    p.add_argument('--verbose', help='Print additional information', action='store_true', required=False)

    args = p.parse_args()

    zemu       = args.zemu
    zetau      = args.zetau
    zmutau     = args.zmutau
    step       = args.step
    input_path = args.input
    year       = args.year

    subset_size= args.subset_size
    subset     = args.subset

    tag        = args.tag
    dryrun     = args.dryrun
    verbose    = args.verbose

    if tag != "": tag = "_"+tag

    if not (zemu or zetau or zmutau):
      print "No signal process selected for processing!"
      exit()
    if zemu + zetau + zmutau > 1:
      print "No more than one signal process can be selected for processing!"
      exit()
    if step not in ["digi", "hlt", "digihlt", "reco", "mini", "nano"]:
      print "Unrecognized step %s!" % (step)
      exit()
    if step == "digihlt" and year == "2017":
      print "digihlt step not defined for 2017, use digi and then hlt"
      exit()
    elif (step == "digi" or step == "hlt") and year != "2017":
      print "digi/hlt steps only defined for 2017, use digihlt step for %s" % (year)
      exit()

    if step=='digi':
      cfg = 'LFVAnalysis_13TeV_DIGIL1_'+year+'_cfg.py'
      step_name="DIGIL1"
    elif step=="hlt":
      cfg = 'LFVAnalysis_13TeV_HLT_'+year+'_cfg.py'
      step_name="HLT"
    elif step=="digihlt":
      cfg = 'LFVAnalysis_13TeV_DIGIL1HLT_'+year+'_cfg.py'
      step_name="DIGIL1HLT"
    elif step=='reco':
      cfg = 'LFVAnalysis_13TeV_RECO_'+year+'_cfg.py'
      step_name="RECO"
    elif step=='mini':
      cfg = 'LFVAnalysis_13TeV_MINIAOD_'+year+'_cfg.py'
      step_name="MINI"
    elif step=="nano":
      cfg = 'LFVAnalysis_13TeV_NANOAOD_'+year+'_cfg.py'
      step_name="NANO"  
    else:
      print "Unknown step in cfg",step
      exit()

    if subset >= 0:
      print "Processing subset %i with subset size %i" % (subset, subset_size)
      tag = "_s%s" % (str(subset).zfill(2))

    config.Data.outputDatasetTag = 'ZLFVAnalysis_'+step_name+tag

    # Configuration depending on the stage being processed

    # if year=="2018" and (step=="reco" or step=="digihlt"): 
    if step == "digihlt": 
      config.JobType.maxMemoryMB = 4000

    if step == "reco":
      config.JobType.maxMemoryMB = 4000

    if step == "mini": # Fairly fast processing
      config.Data.unitsPerJob = 2
    
    if step == "nano": # Very fast processing
      config.Data.unitsPerJob = 10


    config.General.workArea = 'crab_projects/'+step_name+year+tag
    config.JobType.psetName = cfg

    from CRABAPI.RawCommand import crabCommand
    from CRABClient.ClientExceptions import ClientException
    from httplib import HTTPException
    from multiprocessing import Process
    import os.path, subprocess


    def submit(config):
        try:
            crabCommand('submit', config = config)
        except HTTPException as hte:
            print "Failed submitting task: %s" % (hte.headers)
        except ClientException as cle:
            print "Failed submitting task: %s" % (cle)


    if zemu:
      config.General.requestName = 'LFVAnalysis_ZEMu_'+step_name+'_'+year+tag
      config.Data.userInputFiles = list_of_files(input_path, subset, subset_size)
      config.Data.outLFNDirBase = lfn_path+'/ZEMu_'+step_name+'_'+year+tag
    
      if dryrun or verbose:
        print config
      if not dryrun:
        p = Process(target=submit, args=(config,))
        p.start()
        p.join()

    if zetau:
      config.General.requestName = 'LFVAnalysis_ZETau_'+step_name+'_'+year+tag
      config.Data.userInputFiles = list_of_files(input_path, subset, subset_size)
      config.Data.outLFNDirBase = lfn_path+'/ZETau_'+step_name+'_'+year+tag
    
      if dryrun or verbose:
        print config
      if not dryrun:
        p = Process(target=submit, args=(config,))
        p.start()
        p.join()

    if zmutau:
      config.General.requestName = 'LFVAnalysis_ZMuTau_'+step_name+'_'+year+tag
      config.Data.userInputFiles = list_of_files(input_path, subset, subset_size)
      config.Data.outLFNDirBase = lfn_path+'/ZMuTau_'+step_name+'_'+year+tag

      if dryrun or verbose:
        print config
      if not dryrun:
        p = Process(target=submit, args=(config,))
        p.start()
        p.join()

    
