from CRABAPI.RawCommand import crabCommand
from WMCore.Configuration import Configuration
from CRABClient.UserUtilities import config

lfn_path = '/store/group/phys_smp/ZLFV/MC_generation' #no "/" in end
year = "2018"
extra_name = '_400k' #start with "_"
njobs=1998 #maximum number of jobs per task is 10k
nunits=200
submitZEMu=True
submitZETau=True
submitZMuTau=True

config = Configuration()
config.section_('General')
config.General.transferOutputs = True
config.General.workArea = 'crab_projects/GEN'+year
config.section_('JobType')
config.JobType.pluginName = 'PrivateMC'
config.JobType.allowUndistributedCMSSW = True

config.section_('Data')
config.Data.splitting = 'EventBased'
config.Data.unitsPerJob = nunits
NJOBS = njobs
config.Data.totalUnits = config.Data.unitsPerJob * NJOBS
config.Data.publication = True

config.section_('Site')
config.Site.storageSite = 'T2_CH_CERN'


if __name__ == '__main__':

    from CRABAPI.RawCommand import crabCommand
    from CRABClient.ClientExceptions import ClientException
    from httplib import HTTPException
    from multiprocessing import Process

    def submit(config):
        try:
            crabCommand('submit', config = config)
        except HTTPException as hte:
            print ("Failed submitting task: %s" % (hte.headers))
        except ClientException as cle:
            print ("Failed submitting task: %s" % (cle))

    config.General.requestName = 'LFVAnalysis_ZEMu_GENSIM_'+year+extra_name
    config.JobType.psetName = 'LFVAnalysis_ZEMu_13TeV_pythia8_GENSIM_'+year+'_cfg.py'
    config.Data.outputPrimaryDataset = 'LFVAnalysis_ZEMu_'+year+extra_name
    config.Data.outputDatasetTag = 'LFVAnalysis_ZEMu_GENSIM_'+year+extra_name
    config.Data.outLFNDirBase = lfn_path+'/ZEMu_GENSIM_'+year+extra_name
    if submitZEMu:
       p = Process(target=submit, args=(config,))
       p.start()
       p.join()


    config.General.requestName = 'LFVAnalysis_ZETau_GENSIM_'+year+extra_name
    config.JobType.psetName = 'LFVAnalysis_ZETau_13TeV_pythia8_GENSIM_'+year+'_cfg.py'
    config.Data.outputPrimaryDataset = 'LFVAnalysis_ZETau_'+year+extra_name
    config.Data.outputDatasetTag = 'LFVAnalysis_ZETau_GENSIM_'+year+extra_name
    config.Data.outLFNDirBase = lfn_path+'/ZETau_GENSIM_'+year+extra_name
    if submitZETau:   
       p = Process(target=submit, args=(config,))
       p.start()
       p.join()


    config.General.requestName = 'LFVAnalysis_ZMuTau_GENSIM_'+year+extra_name
    config.JobType.psetName = 'LFVAnalysis_ZMuTau_13TeV_pythia8_GENSIM_'+year+'_cfg.py'
    config.Data.outputPrimaryDataset = 'LFVAnalysis_ZMuTau_'+year+extra_name
    config.Data.outputDatasetTag = 'LFVAnalysis_ZMuTau_GENSIM_'+year+extra_name
    config.Data.outLFNDirBase = lfn_path+'/ZMuTau_GENSIM_'+year+extra_name
    if submitZMuTau:
       p = Process(target=submit, args=(config,))
       p.start()
       p.join()

