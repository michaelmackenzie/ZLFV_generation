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


def list_of_files(path):
  files= subprocess.check_output(["ls", path]).splitlines()
  eos_path = path
  eos_path = eos_path.replace('/eos/cms', '')
  eos_path = eos_path.replace('/eos/uscms', '')
  outfiles=[]
  for line in files:
    if "root" in line:
      outfiles.append(eos_path+line)
  return outfiles



if __name__ == '__main__':

    p = argparse.ArgumentParser(description='Submit MC generation jobs')

    p.add_argument('--zemu'   , help='Submit Z->e+mu generation'  , action='store_true', required=False)
    p.add_argument('--zetau'  , help='Submit Z->e+tau generation' , action='store_true', required=False)
    p.add_argument('--zmutau' , help='Submit Z->mu+tau generation', action='store_true', required=False)

    p.add_argument('--step'   , help='Generation step: digi, hlt, digihlt, reco, mini, or nano ', required=True)
    p.add_argument('--input'  , help='Input dataset path', required=True)
    p.add_argument('--year'   , help='Sample year', required=True)

    p.add_argument('--tag'    , help='Output dataset tag', default="", required=False)
    p.add_argument('--dryrun' , help='Setup merging without running', action='store_true', required=False)
    p.add_argument('--verbose', help='Print additional information', action='store_true', required=False)

    args = p.parse_args()

    zemu       = args.zemu
    zetau      = args.zetau
    zmutau     = args.zmutau
    step       = args.step
    input_path = args.input
    year       = args.year

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

    config.Data.outputDatasetTag = 'ZLFVAnalysis_'+step_name+tag
    if year=="2018" and (step=="reco" or step=="digihlt"): 
      config.JobType.maxMemoryMB = 4000
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
      config.General.requestName = 'LFVAnalysis_ZEMu_'+step_name+tag
      config.Data.userInputFiles = list_of_files(input_path)
      config.Data.outLFNDirBase = lfn_path+'/ZEMu_'+step_name+tag
    
      if not dryrun:
        p = Process(target=submit, args=(config,))
        p.start()
        p.join()
      else:
        print config

    if zetau:
      config.General.requestName = 'LFVAnalysis_ZETau_'+step_name+tag
      config.Data.userInputFiles = list_of_files(input_path)
      config.Data.outLFNDirBase = lfn_path+'/ZETau_'+step_name+tag
    
      if not dryrun:
        p = Process(target=submit, args=(config,))
        p.start()
        p.join()
      else:
        print config

    if zmutau:
      config.General.requestName = 'LFVAnalysis_ZMuTau_'+step_name+tag
      config.Data.userInputFiles = list_of_files(input_path)
      config.Data.outLFNDirBase = lfn_path+'/ZMuTau_'+step_name+tag

      if not dryrun:
        p = Process(target=submit, args=(config,))
        p.start()
        p.join()
      else:
        print config

    
