#!/usr/bin/env python

import subprocess
import os
import regtools
from regtools import RegArgs
import argparse

def main():
    parser = argparse.ArgumentParser(description='runs the SC regression trainings')
    parser.add_argument('--era',required=True,help='regression to produce')
    parser.add_argument('--input_dir','-i',default='/home/hep/wrtabb/Egamma/input_trees/Run3_2021',help='input directory with the ntuples')
    parser.add_argument('--output_dir','-o',default="results",help='output dir')
    args = parser.parse_args()

    # step 1, run calo only regression on the ideal IC to get the mean
    # step 2, apply the mean to the real IC sample and save the result in a tree
    # step 3, retrain the resolution for the real IC on the corrected energy
    # step 4, step 4 is ECAL-trk combination; left off for high energy electrons 
    # Only three steps are carried out

    run_step1 = True 
    run_step2 = True
    run_step3 = True 
    
    base_ele_cuts = "(mc.energy>0 && ssFrac.sigmaIEtaIEta>0 && ssFrac.sigmaIPhiIPhi>0 && ele.et>0 && ele.nrSatCrys>0 && {extra_cuts})"

    # Regression on saturated electrons
    if args.era=='HighEnergy':
        era_name = "HighEnergy"
        input_ideal_ic  = "{}/DoubleElectron_FlatPt-500To5000_FlatPU0to70IDEALGT_120X_mcRun3_2021_realistic_v6_ECALIdealIC-v2_AODSIM.root".format(args.input_dir)
        input_real_ic  = "{}/DoubleElectron_FlatPt-500To5000_FlatPU0to70_120X_mcRun3_2021_realistic_v6-v1_AODSIM.root".format(args.input_dir)
        ideal_eventnr_cut = "evt.eventnr%3==0"
        real_eventnr_cut = "evt.eventnr%3==1" 

    else:
        raise ValueError("era {} is invalid, the only available option is HighEnergy".format(era))

    #step1 train the calo only regression using IDEAL intercalibration constants
    print "starting step1"
    regArgs = RegArgs()
    regArgs.input_training = str(input_ideal_ic)
    regArgs.input_testing = str(input_ideal_ic)  
    regArgs.set_ecal_default()
    regArgs.cuts_base = base_ele_cuts.format(extra_cuts = ideal_eventnr_cut)
    regArgs.cuts_name = "stdCuts"
    regArgs.cfg_dir = "configs"
    regArgs.out_dir = "regressions/Run3Ele_Pt500to5000_NoHoverE" 
    regArgs.ntrees = 1500  
    regArgs.base_name = "regEleEcal{era_name}_IdealIC_IdealTraining".format(era_name=era_name)
    if run_step1: regArgs.run_eb_and_ee()
    
    #step2 now we run over the REAL intercalibration constant data and make a rew tree with this regression included
    print "starting step2"
    regArgs.do_eb = True
    forest_eb_file = regArgs.output_name()
    regArgs.do_eb = False
    forest_ee_file = regArgs.output_name()

    regArgs.base_name = "regEleEcal{era_name}_RealIC_IdealTraining".format(era_name=era_name)
    input_for_res_training = str(regArgs.applied_name()) #save the output name before we change it

    # Set scram arch
    arch = "slc7_amd64_gcc700"

    if run_step2: subprocess.Popen(["bin/"+arch+"/RegressionApplierExe",input_real_ic,input_for_res_training,"--gbrForestFileEE",forest_ee_file,"--gbrForestFileEB",forest_eb_file,"--nrThreads","4","--treeName",regArgs.tree_name,"--writeFullTree","1","--regOutTag","Ideal"]).communicate()
    
    #step3 we now run over re-train with the REAL sample for the sigma, changing the target to have the correction applied 
    print "starting step3"
    regArgs.base_name = "regEleEcal{era_name}_RealIC_RealTraining".format(era_name=era_name)
    regArgs.input_training = input_for_res_training
    regArgs.input_testing = input_for_res_training
    regArgs.target = "mc.energy/((sc.rawEnergy+sc.rawESEnergy)*regIdealMean)"
    regArgs.fix_mean = True
    regArgs.write_full_tree = "1"
    regArgs.reg_out_tag = "Real"
    regArgs.cuts_base = base_ele_cuts.format(extra_cuts = real_eventnr_cut)
    if run_step3: regArgs.run_eb_and_ee()

    
    
if __name__ =='__main__':
    main()


