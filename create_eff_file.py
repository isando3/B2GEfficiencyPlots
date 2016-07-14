from ROOT import *
import sys


fout_name = sys.argv1[]
fin = TFile("uhh2.AnalysisModuleRunner.MC.TTbar.root")
#fin2 = TFile("uhh2.AnalysisModuleRunner.MC.TTbar.root")
den_h = fin.Get("trigtag/l")
num_h = fin.Get("trigOR/lep_pt_VS_lep_eta")
clone_h = den_h.Clone()
clone_h.SetTitle("Efficiency(TTbar)")
clone_h.Divide(num_h, den_h, 1.0, 1.0, "B")
clone_h.SetDrawOption("COLZ TEXT")
fout = TFile("HLT_Ele50PFJET_or_HLT_Ele105__TTbar__Eff.root", "recreate")
fout.cd()
dir = fout.mkdir("PtEtaBins")
dir.cd()
dir.WriteObject(clone_h,"ptetadata")
fout.Write()
fout.Close()
