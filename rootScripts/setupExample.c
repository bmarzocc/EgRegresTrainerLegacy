{

 gROOT->ProcessLine(".L makeResPlots.C+");
 TTree* regTestTree = HistFuncs::makeChain("egRegTree","/eos/cms/store/group/dpg_ecal/alca_ecalcalib/bmarzocc/Clustering/FourElectronsGunPt1-100_pythia8_StdMixing_Flat55To75_14TeV_112X_mcRun3_2021_realistic_v16_egmRegNtuples_Mustache.root"); 
 regTestTree->AddFriend("regCorr = egRegTreeFriend","regressions/Run3SC_results_Mustache/2021Run3_RealIC_RealTraining_stdVar_stdCuts_ntrees1500_applied.root");
}
