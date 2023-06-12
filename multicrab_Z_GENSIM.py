from CRABAPI.RawCommand import crabCommand
from WMCore.Configuration import Configuration
from CRABClient.UserUtilities import config
import os
import sys
import argparse


lfn_path = '/store/group/phys_smp/ZLFV/MC_generation' #no "/" in end

config = Configuration()
config.section_('General')
config.General.transferOutputs = True
config.section_('JobType')
config.JobType.pluginName = 'PrivateMC'
config.JobType.allowUndistributedCMSSW = True

config.section_('Data')
config.Data.splitting = 'EventBased'
config.Data.publication = True

config.section_('Site')
config.Site.storageSite = 'T2_CH_CERN'


if __name__ == '__main__':

    p = argparse.ArgumentParser(description='Submit MC generation jobs')
    p.add_argument('--zemu'  , help='Submit Z->e+mu generation'  , action='store_true', required=False)
    p.add_argument('--zetau' , help='Submit Z->e+tau generation' , action='store_true', required=False)
    p.add_argument('--zmutau', help='Submit Z->mu+tau generation', action='store_true', required=False)

    p.add_argument('--gen_config', help='Generation configuration file name', default="", required=False)
    p.add_argument('--year'      , help='Sample year',default="", required=True)
    p.add_argument('--tag'       , help='Generation version tag', default="", required=False)

    p.add_argument('--njobs'     , help='Generation N(jobs)', default=2000, required=False)
    p.add_argument('--nunits'    , help='Generation N(units/job)', default=200, required=False)

    p.add_argument('--dryrun'    , help='Setup merging without running', action='store_true', required=False)
    p.add_argument('--verbose'   , help='Print additional information', action='store_true', required=False)

    args = p.parse_args()

    zemu       = args.zemu
    zetau      = args.zetau
    zmutau     = args.zmutau
    gen_config = args.gen_config
    tag        = args.tag
    year       = args.year
    njobs      = int(args.njobs)
    nunits     = int(args.nunits)
    dryrun     = args.dryrun
    verbose    = args.verbose

    if tag != "": tag = "_"+tag

    if not (zemu or zetau or zmutau):
        print "No signal process selected for generation!"
        exit()

    config.General.workArea = 'crab_projects/GEN'+year
    config.Data.unitsPerJob = nunits
    config.Data.totalUnits = nunits * njobs

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

    def print_config(config):
        print "request:", config.General.requestName
        print "pset   :", config.JobType.psetName
        print "primary:", config.Data.outputPrimaryDataset
        print "tag    :", config.Data.outputDatasetTag
        print "outdir :", config.Data.outLFNDirBase
        print


    if verbose:
        print "Outdir       :", lfn_path
        print "N(jobs)      :", njobs
        print "N(units/job) :", nunits
        print

    config.General.requestName = 'LFVAnalysis_ZEMu_GENSIM_'+year+tag
    config.JobType.psetName = 'LFVAnalysis_ZEMu' + gen_config + '_13TeV_pythia8_GENSIM_'+year+'_cfg.py'
    config.Data.outputPrimaryDataset = 'LFVAnalysis_ZEMu_'+year+tag
    config.Data.outputDatasetTag = 'LFVAnalysis_ZEMu_GENSIM_'+year+tag
    config.Data.outLFNDirBase = lfn_path+'/ZEMu_GENSIM_'+year+tag
    if zemu:
        if verbose: print_config(config)
        if not dryrun:
            p = Process(target=submit, args=(config,))
            p.start()
            p.join()
        else:
            print "Dry run: not submitting Z->e+mu"


    config.General.requestName = 'LFVAnalysis_ZETau_GENSIM_'+year+tag
    config.JobType.psetName = 'LFVAnalysis_ZETau' + gen_config + '_13TeV_pythia8_GENSIM_'+year+'_cfg.py'
    config.Data.outputPrimaryDataset = 'LFVAnalysis_ZETau_'+year+tag
    config.Data.outputDatasetTag = 'LFVAnalysis_ZETau_GENSIM_'+year+tag
    config.Data.outLFNDirBase = lfn_path+'/ZETau_GENSIM_'+year+tag
    if zetau:   
        if verbose: print_config(config)
        if not dryrun:
            p = Process(target=submit, args=(config,))
            p.start()
            p.join()
        else:
            print "Dry run: not submitting Z->e+tau"


    config.General.requestName = 'LFVAnalysis_ZMuTau_GENSIM_'+year+tag
    config.JobType.psetName = 'LFVAnalysis_ZMuTau_13TeV_pythia8_GENSIM_'+year+'_cfg.py'
    config.Data.outputPrimaryDataset = 'LFVAnalysis_ZMuTau_'+year+tag
    config.Data.outputDatasetTag = 'LFVAnalysis_ZMuTau' + gen_config + '_GENSIM_'+year+tag
    config.Data.outLFNDirBase = lfn_path+'/ZMuTau_GENSIM_'+year+tag
    if zmutau:
        if verbose: print_config(config)
        if not dryrun:
            p = Process(target=submit, args=(config,))
            p.start()
            p.join()
        else:
            print "Dry run: not submitting Z->mu+tau"

