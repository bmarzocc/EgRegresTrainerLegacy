#!/usr/bin/python
import numpy as n
from ROOT import *
import sys, getopt
from array import array
from optparse import OptionParser
import operator
import math 
from collections import OrderedDict

def getHistoRange(h1,h2):

   bin1_min = h1.FindFirstBinAbove(0.)
   bin1_max = h1.FindLastBinAbove(0.) 
   bin2_min = h2.FindFirstBinAbove(0.)
   bin2_max = h2.FindLastBinAbove(0.)  
   x1_min = h1.GetBinCenter(bin1_min)-h1.GetBinWidth(bin1_min)
   x1_max = h1.GetBinCenter(bin1_max)+h1.GetBinWidth(bin1_max)
   x2_min = h2.GetBinCenter(bin2_min)-h2.GetBinWidth(bin2_min)
   x2_max = h2.GetBinCenter(bin2_max)+h2.GetBinWidth(bin2_max)
   
   xs_min = [x1_min,x2_min]
   xs_max = [x1_max,x2_max]
 
   x_min = min(xs_min)
   x_max = max(xs_max)
   
   if x_min>0.: 
      x_min = x_min*0.8
   else: 
      x_min = 1.2*x_min
   
   if x_max>0.: 
      x_max = x_max*1.2
   else: 
      x_max = 0.8*x_max

   return [x_min,x_max]

def drawHistos(h1,h2,name,region):

  h1.SetMarkerStyle(9)
  h1.SetLineWidth(2)
  h1.SetMarkerColor(kBlack)
  h1.SetLineColor(kBlack) 
  h1.GetXaxis().SetTitle(name)

  h2.SetMarkerStyle(9)
  h2.SetLineWidth(2)
  h2.SetMarkerColor(kRed)
  h2.SetLineColor(kRed) 
  h2.GetXaxis().SetTitle(name)

  max = h1.GetMaximum()
  if(h2.GetMaximum()>max):
     max = h2.GetMaximum()
  h1.SetMaximum(max*1.2)

  name = name.replace("/","OVER")
  c1 = TCanvas()
  c1.cd()
  h1.Draw("Hist")
  h2.Draw("Hist,same")
  c1.SaveAs("varPlots/"+str(name)+"_"+region+".png")
  c1.SaveAs("varPlots/"+str(name)+"_"+region+".pdf")

  c2 = TCanvas()
  c2.cd()
  c2.SetLogy()
  h1.Draw("Hist")
  h2.Draw("Hist,same")
  c2.SaveAs("varPlots/"+str(name)+"_"+region+"_log.png")
  c2.SaveAs("varPlots/"+str(name)+"_"+region+"_log.pdf")

  h1.Scale(1./h1.Integral())
  h2.Scale(1./h2.Integral())

  c3 = TCanvas()
  c3.cd()
  h1.Draw("Hist")
  h2.Draw("Hist,same")
  c3.SaveAs("varPlots/"+str(name)+"_"+region+"_norm.png")
  c3.SaveAs("varPlots/"+str(name)+"_"+region+"_norm.pdf")

  c4 = TCanvas()
  c4.cd()
  c4.SetLogy()
  h1.Draw("Hist")
  h2.Draw("Hist,same")
  c4.SaveAs("varPlots/"+str(name)+"_"+region+"_norm_log.png")
  c4.SaveAs("varPlots/"+str(name)+"_"+region+"_norm_log.pdf")

if __name__ == '__main__':

  gROOT.SetBatch(kTRUE)
  gStyle.SetOptStat(0)
 
  #Variables for Electron regression 
  inputVariablesEB = ["sc.rawEnergy","sc.etaWidth","sc.phiWidth","sc.seedClusEnergy/sc.rawEnergy","ssFull.e5x5/sc.rawEnergy","ele.hademTow","rho","sc.dEtaSeedSC","sc.dPhiSeedSC","ssFull.e3x3/sc.rawEnergy","ssFull.sigmaIEtaIEta","ssFull.sigmaIEtaIPhi","ssFull.sigmaIPhiIPhi","ssFull.eMax/ssFull.e5x5","ssFull.e2nd/ssFull.e5x5","ssFull.eTop/ssFull.e5x5","ssFull.eBottom/ssFull.e5x5","ssFull.eLeft/ssFull.e5x5","ssFull.eRight/ssFull.e5x5","ssFull.e2x5Max/ssFull.e5x5","ssFull.e2x5Left/ssFull.e5x5","ssFull.e2x5Right/ssFull.e5x5","ssFull.e2x5Top/ssFull.e5x5","ssFull.e2x5Bottom/ssFull.e5x5","ele.nrSatCrys","sc.numberOfClusters","sc.iEtaOrX","sc.iPhiOrY","sc.iEtaMod5","sc.iPhiMod2","sc.iEtaMod20","sc.iPhiMod20","(sc.rawEnergy+sc.rawESEnergy)*regIdealMean","regRealSigma/regIdealMean","ele.trkPModeErr/ele.trkPMode","(sc.rawEnergy+sc.rawESEnergy)*regIdealMean/ele.trkPMode","ele.ecalDrivenSeed","ssFull.e3x3/sc.rawEnergy","ele.fbrem","ele.trkEtaMode","ele.trkPhiMode"]

  inputVariablesEE = ["sc.rawEnergy","sc.etaWidth","sc.phiWidth","sc.seedClusEnergy/sc.rawEnergy","ssFull.e5x5/sc.rawEnergy","ele.hademTow","rho","sc.dEtaSeedSC","sc.dPhiSeedSC","ssFull.e3x3/sc.rawEnergy","ssFull.sigmaIEtaIEta","ssFull.sigmaIEtaIPhi","ssFull.sigmaIPhiIPhi","ssFull.eMax/ssFull.e5x5","ssFull.e2nd/ssFull.e5x5","ssFull.eTop/ssFull.e5x5","ssFull.eBottom/ssFull.e5x5","ssFull.eLeft/ssFull.e5x5","ssFull.eRight/ssFull.e5x5","ssFull.e2x5Max/ssFull.e5x5","ssFull.e2x5Left/ssFull.e5x5","ssFull.e2x5Right/ssFull.e5x5","ssFull.e2x5Top/ssFull.e5x5","ssFull.e2x5Bottom/ssFull.e5x5","ele.nrSatCrys","sc.numberOfClusters","sc.iEtaOrX","sc.iPhiOrY","sc.rawESEnergy/sc.rawEnergy","(sc.rawEnergy+sc.rawESEnergy)*regIdealMean","regRealSigma/regIdealMean","ele.trkPModeErr/ele.trkPMode","(sc.rawEnergy+sc.rawESEnergy)*regIdealMean/ele.trkPMode","ele.ecalDrivenSeed","ssFull.e3x3/sc.rawEnergy","ele.fbrem","ele.trkEtaMode","ele.trkPhiMode"] 
  
  tree_Mustache = TChain()
  tree_Mustache_friend = TChain()
  tree_Mustache.AddFile('/eos/cms/store/group/dpg_ecal/alca_ecalcalib/bmarzocc/Clustering/FourElectronsGunPt1-100_pythia8_StdMixing_Flat55To75_14TeV_123X_mcRun3_2021_realistic_v11_UL18_pfRechitThres_EleRegression_Mustache_125X_bugFix/regEleEcal2021Run3_RealIC_RealTraining_stdVar_stdCuts_ntrees1500_applied.root/egRegTree_genMatched')
  tree_Mustache_friend.AddFile('/eos/cms/store/group/dpg_ecal/alca_ecalcalib/bmarzocc/Clustering/FourElectronsGunPt1-100_pythia8_StdMixing_Flat55To75_14TeV_123X_mcRun3_2021_realistic_v11_UL18_pfRechitThres_EleRegression_Mustache_125X_bugFix/regEleEcalTrk2021Run3_RealIC_stdVar_stdCuts_ntrees1500_applied.root/egRegTree_genMatchedFriend')
  tree_Mustache.AddFriend(tree_Mustache_friend)
  
  tree_DeepSC = TChain()
  tree_DeepSC_friend = TChain()
  tree_DeepSC.AddFile('/eos/cms/store/group/dpg_ecal/alca_ecalcalib/bmarzocc/Clustering/FourElectronsGunPt1-100_pythia8_StdMixing_Flat55To75_14TeV_123X_mcRun3_2021_realistic_v11_UL18_pfRechitThres_EleRegression_DeepSC_AlgoA_125X_bugFix/regEleEcal2021Run3_RealIC_RealTraining_stdVar_stdCuts_ntrees1500_applied.root/egRegTree_genMatched')
  tree_DeepSC_friend.AddFile('/eos/cms/store/group/dpg_ecal/alca_ecalcalib/bmarzocc/Clustering/FourElectronsGunPt1-100_pythia8_StdMixing_Flat55To75_14TeV_123X_mcRun3_2021_realistic_v11_UL18_pfRechitThres_EleRegression_DeepSC_AlgoA_125X_bugFix/regEleEcalTrk2021Run3_RealIC_stdVar_stdCuts_ntrees1500_applied.root/egRegTree_genMatchedFriend')
  tree_DeepSC.AddFriend(tree_DeepSC_friend)
  
  ''' 
  #Variables for Photon regression 
  inputVariablesEB = ["sc.rawEnergy","sc.etaWidth","sc.phiWidth","sc.seedClusEnergy/sc.rawEnergy","ssFull.e5x5/sc.rawEnergy","pho.hademCone","rho","sc.dEtaSeedSC","sc.dPhiSeedSC","ssFull.e3x3/sc.rawEnergy","ssFull.sigmaIEtaIEta","phoSSFull.sigmaIEtaIPhi","ssFull.sigmaIPhiIPhi","ssFull.eMax/ssFull.e5x5","ssFull.e2nd/ssFull.e5x5","ssFull.eTop/ssFull.e5x5","ssFull.eBottom/ssFull.e5x5","ssFull.eLeft/ssFull.e5x5","ssFull.eRight/ssFull.e5x5","ssFull.e2x5Max/ssFull.e5x5","ssFull.e2x5Left/ssFull.e5x5","ssFull.e2x5Right/ssFull.e5x5","ssFull.e2x5Top/ssFull.e5x5","ssFull.e2x5Bottom/ssFull.e5x5","pho.nrSatCrys","sc.numberOfClusters","sc.iEtaOrX","sc.iPhiOrY","sc.iEtaMod5","sc.iPhiMod2","sc.iEtaMod20","sc.iPhiMod20"]

  inputVariablesEE = ["sc.rawEnergy","sc.etaWidth","sc.phiWidth","sc.seedClusEnergy/sc.rawEnergy","ssFull.e5x5/sc.rawEnergy","pho.hademCone","rho","sc.dEtaSeedSC","sc.dPhiSeedSC","ssFull.e3x3/sc.rawEnergy","ssFull.sigmaIEtaIEta","phoSSFull.sigmaIEtaIPhi","ssFull.sigmaIPhiIPhi","ssFull.eMax/ssFull.e5x5","ssFull.e2nd/ssFull.e5x5","ssFull.eTop/ssFull.e5x5","ssFull.eBottom/ssFull.e5x5","ssFull.eLeft/ssFull.e5x5","ssFull.eRight/ssFull.e5x5","ssFull.e2x5Max/ssFull.e5x5","ssFull.e2x5Left/ssFull.e5x5","ssFull.e2x5Right/ssFull.e5x5","ssFull.e2x5Top/ssFull.e5x5","ssFull.e2x5Bottom/ssFull.e5x5","pho.nrSatCrys","sc.numberOfClusters","sc.iEtaOrX","sc.iPhiOrY","sc.rawESEnergy/sc.rawEnergy"] 
  
  tree_Mustache = TChain()
  tree_Mustache_friend = TChain()
  tree_Mustache.AddFile('/eos/cms/store/group/dpg_ecal/alca_ecalcalib/bmarzocc/Clustering/FourGammasGunPt1-100_pythia8_StdMixing_Flat55To75_14TeV_123X_mcRun3_2021_realistic_v11_UL18_pfRechitThres_PhoRegression_Mustache_125X_bugFix/regPhoEcal2021Run3_RealIC_RealTraining_stdVar_stdCuts_ntrees1500_applied.root/egRegTree_genMatched')
  tree_Mustache_friend.AddFile('/eos/cms/store/group/dpg_ecal/alca_ecalcalib/bmarzocc/Clustering/FourGammasGunPt1-100_pythia8_StdMixing_Flat55To75_14TeV_123X_mcRun3_2021_realistic_v11_UL18_pfRechitThres_PhoRegression_Mustache_125X_bugFix/regPhoEcal2021Run3_RealIC_RealTraining_stdVar_stdCuts_ntrees1500_applied.root/egRegTree_genMatchedFriend')
  tree_Mustache.AddFriend(tree_Mustache_friend)
  
  tree_DeepSC = TChain()
  tree_DeepSC_friend = TChain()
  tree_DeepSC.AddFile('/eos/cms/store/group/dpg_ecal/alca_ecalcalib/bmarzocc/Clustering/FourGammasGunPt1-100_pythia8_StdMixing_Flat55To75_14TeV_123X_mcRun3_2021_realistic_v11_UL18_pfRechitThres_PhoRegression_DeepSC_AlgoA_125X_bugFix/regPhoEcal2021Run3_RealIC_RealTraining_stdVar_stdCuts_ntrees1500_applied.root/egRegTree_genMatched')
  tree_DeepSC_friend.AddFile('/eos/cms/store/group/dpg_ecal/alca_ecalcalib/bmarzocc/Clustering/FourGammasGunPt1-100_pythia8_StdMixing_Flat55To75_14TeV_123X_mcRun3_2021_realistic_v11_UL18_pfRechitThres_PhoRegression_DeepSC_AlgoA_125X_bugFix/regPhoEcal2021Run3_RealIC_RealTraining_stdVar_stdCuts_ntrees1500_applied.root/egRegTree_genMatchedFriend')
  tree_DeepSC.AddFriend(tree_DeepSC_friend)
  '''

  for i,var in enumerate(inputVariablesEB):
  
     h1_range_EB = TH1F("h1_range_"+str(i)+"_EB","h1_range_"+str(i)+"_EB",50000,-999.,999) 
     h2_range_EB = TH1F("h2_range_"+str(i)+"_EB","h2_range_"+str(i)+"_EB",50000,-999.,999) 

     tree_Mustache.Draw(var+">>h1_range_"+str(i)+"_EB","mc.energy>0 && ssFrac.sigmaIEtaIEta>0 && ssFrac.sigmaIPhiIPhi>0 && ele.et>0 && sc.isEB")
     tree_DeepSC.Draw(var+">>h2_range_"+str(i)+"_EB","mc.energy>0 && ssFrac.sigmaIEtaIEta>0 && ssFrac.sigmaIPhiIPhi>0 && ele.et>0 && sc.isEB")
     range = getHistoRange(h1_range_EB,h2_range_EB)
     x_min = range[0]
     x_max = range[1]    

     x_min = 0.
     print "EB:",var,", range:",range[0],range[1]    
    
     h1_EB = TH1F("h1_"+str(i)+"_EB",var,150,x_min,x_max) 
     tree_Mustache.Draw(var+">>h1_"+str(i)+"_EB","mc.energy>0 && ssFrac.sigmaIEtaIEta>0 && ssFrac.sigmaIPhiIPhi>0 && ele.et>0 && sc.isEB")

     h2_EB = TH1F("h2_"+str(i)+"_EB",var,150,x_min,x_max)      
     tree_DeepSC.Draw(var+">>h2_"+str(i)+"_EB","mc.energy>0 && ssFrac.sigmaIEtaIEta>0 && ssFrac.sigmaIPhiIPhi>0 && ele.et>0 && sc.isEB") 

     drawHistos(h1_EB,h2_EB,var,"EB") 

  for i,var in enumerate(inputVariablesEE): 

     h1_range_EE = TH1F("h1_range_"+str(i)+"_EE","h1_range_"+str(i)+"_EE",50000,-999.,999) 
     h2_range_EE = TH1F("h2_range_"+str(i)+"_EE","h2_range_"+str(i)+"_EW",50000,-999.,999) 

     tree_Mustache.Draw(var+">>h1_range_"+str(i)+"_EE","mc.energy>0 && ssFrac.sigmaIEtaIEta>0 && ssFrac.sigmaIPhiIPhi>0 && ele.et>0 && sc.isEB==0")
     tree_DeepSC.Draw(var+">>h2_range_"+str(i)+"_EE","mc.energy>0 && ssFrac.sigmaIEtaIEta>0 && ssFrac.sigmaIPhiIPhi>0 && ele.et>0 && sc.isEB==0")
     range = getHistoRange(h1_range_EE,h2_range_EE)
     x_min = range[0]
     x_max = range[1]    

     print "EE:",var,", range:",range[0],range[1]    
    
     h1_EE = TH1F("h1_"+str(i)+"_EE",var,150,x_min,x_max) 
     tree_Mustache.Draw(var+">>h1_"+str(i)+"_EE","mc.energy>0 && ssFrac.sigmaIEtaIEta>0 && ssFrac.sigmaIPhiIPhi>0 && ele.et>0 && sc.isEB==0")

     h2_EE = TH1F("h2_"+str(i)+"_EE",var,150,x_min,x_max)      
     tree_DeepSC.Draw(var+">>h2_"+str(i)+"_EE","mc.energy>0 && ssFrac.sigmaIEtaIEta>0 && ssFrac.sigmaIPhiIPhi>0 && ele.et>0 && sc.isEB==0") 

     drawHistos(h1_EE,h2_EE,var,"EE")  

