from ROOT import *


fin = TFile("uhh2.AnalysisModuleRunner.MC.TTbar.root")
#fin2 = TFile("uhh2.AnalysisModuleRunner.MC.TTbar.root")
den_h = fin.Get("trigtag/lep_pt_VS_lep_eta")
num_h = fin.Get("trigOR/lep_pt_VS_lep_eta")
clone_h = den_h.Clone()
clone_h.SetTitle("Efficiency(TTbar)")
#clone_h = TEfficiency(den_h,num_h)
clone_h.Divide(num_h, den_h, 1.0, 1.0, "B")
gStyle.SetPaintTextFormat("2.2f")
clone_h.SetMarkerSize(0.7)
clone_h.Draw("TEXTE COLZ")
fout = TFile("HLT_Ele50PFJET_or_HLT_Ele105__TTbar__Eff.root", "recreate")
fout.cd()
dir = fout.mkdir("PtEtaBins")
dir.cd()
dir.WriteObject(clone_h,"ptetadata")
fout.Write()
fout.Close()