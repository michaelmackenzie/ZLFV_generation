from CRABAPI.RawCommand import crabCommand
from WMCore.Configuration import Configuration
from CRABClient.UserUtilities import config

Debug=False
lfn_path = '/store/group/phys_smp/ZLFV/MC_generation' #no "/" in end
year = "2018"
extra_name = '_'+year+'_400k' #start with "_"
step ="mini" # (digi, hlt OR digihlt), reco, mini, nano [digi, hlt only for 2017 digihlt for 16 18]
input_emu="/store/group/phys_smp/ZLFV/MC_generation/ZEMu_RECO_2018_400k/CRAB_UserFiles/ZLFVAnalysis_RECO_2018_400k/230430_205241/0000/" # start and finish with "/"
input_etau="/store/group/phys_smp/ZLFV/MC_generation/ZETau_RECO_2018_400k/CRAB_UserFiles/ZLFVAnalysis_RECO_2018_400k/230430_205257/0000/"
input_mutau="/store/group/phys_smp/ZLFV/MC_generation/ZMuTau_RECO_2018_400k/CRAB_UserFiles/ZLFVAnalysis_RECO_2018_400k/230430_205313/0000/"
submitZEMu=True
submitZETau=True
submitZMuTau=True

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
  print "wrong step in cfg ",step
  exit()


config = Configuration()

config.section_('General')
config.General.transferOutputs = True
config.General.workArea = 'crab_projects/'+step_name+extra_name

config.section_('JobType')
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = cfg
config.JobType.allowUndistributedCMSSW = True
if year=="2018" and (step=="reco" or step=="digihlt"): 
   config.JobType.maxMemoryMB = 4000


config.section_('Data')
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
config.Data.publication = False

config.Data.outputDatasetTag = 'ZLFVAnalysis_'+step_name+extra_name

config.section_('Site')
config.Site.storageSite = 'T2_CH_CERN'


def list_of_files(path):
  files= subprocess.check_output(["ls", "/eos/cms/"+path]).splitlines()
  outfiles=[]
  for line in files:
    if "root" in line:
       outfiles.append(path+line)
  return outfiles



if __name__ == '__main__':

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


    config.General.requestName = 'LFVAnalysis_ZEMu_'+step_name+extra_name
    config.Data.userInputFiles = list_of_files(input_emu)
    config.Data.outLFNDirBase = lfn_path+'/ZEMu_'+step_name+extra_name
    

    if not Debug and submitZEMu:
      p = Process(target=submit, args=(config,))
      p.start()
      p.join()
    else:
      print config


    config.General.requestName = 'LFVAnalysis_ZETau_'+step_name+extra_name
    config.Data.userInputFiles = list_of_files(input_etau)
    config.Data.outLFNDirBase = lfn_path+'/ZETau_'+step_name+extra_name
    


    if not Debug and submitZETau:
      p = Process(target=submit, args=(config,))
      p.start()
      p.join()
    else:
      print config

    config.General.requestName = 'LFVAnalysis_ZMuTau_'+step_name+extra_name
    config.Data.userInputFiles = list_of_files(input_mutau)
    config.Data.outLFNDirBase = lfn_path+'/ZMuTau_'+step_name+extra_name


    if not Debug and submitZMuTau:
      p = Process(target=submit, args=(config,))
      p.start()
      p.join()
    else:
      print config

    
