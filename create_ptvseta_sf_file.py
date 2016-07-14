from ROOT import *
import tdrstyle , CMS_lumi


#Setting up size of canvas
H_ref = 1000;
W_ref = 2000;
W = W_ref
H  = H_ref
#c1 = TCanvas('c1',"Plot",1)
T = 0.08*H_ref
B = 0.12*H_ref
L = 0.12*W_ref
R = 0.04*W_ref
c1 = TCanvas("c1","c1",50,50,W,H)
c1.SetFillColor(0)
c1.SetBorderMode(0)
c1.SetFrameFillStyle(0)
c1.SetFrameBorderMode(0)
c1.SetLeftMargin( L/W )
c1.SetRightMargin( R/W )
c1.SetTopMargin( T/H )
c1.SetBottomMargin( B/H )
c1.SetTickx(0)
c1.SetTicky(0)
CMS_lumi.extraText = "Preliminary"

## Update canvas 
gROOT.SetBatch(kTRUE)
c1.cd()
gStyle.SetOptTitle(0)
gStyle.SetOptStat(0)
gStyle.SetTitleFontSize(0.1)
c1.Modified()
CMS_lumi.CMS_lumi(c1,4,11)
c1.Update()


fin1 = TFile("uhh2.AnalysisModuleRunner.DATA.SingleEG.root")
fin2 = TFile("uhh2.AnalysisModuleRunner.MC.TTbar.root")
den_h1 = fin1.Get("trigtag/lep_pt_VS_lep_eta")
num_h1 = fin1.Get("trigprobe/lep_pt_VS_lep_eta")
clone_h1 = den_h1.Clone()
clone_h1.SetTitle("HLT Scale Factor")
clone_h1.Divide(num_h1, den_h1, 1.0, 1.0, "B")
clone_h1.SetDrawOption("COLZ TEXT")
den_h2 = fin2.Get("trigtag/lep_pt_VS_lep_eta")
num_h2 = fin2.Get("trigprobe/lep_pt_VS_lep_eta")
clone_h2 = den_h2.Clone()
clone_h2.SetTitle("HLT Scale Factor")
clone_h2.Divide(num_h2, den_h2, 1.0, 1.0, "B")
clone_h2.SetDrawOption("COLZ TEXT")
clone_sf = clone_h2.Clone()
clone_sf.Divide(clone_h2,clone_h1, 1.0, 1.0, "B")
clone_sf.SetTitle("HLT Scale Factor")
gStyle.SetPaintTextFormat("2.2f")
clone_sf.SetMarkerSize(0.7)
clone_sf.Draw("TEXTE COL2")
clone_sf.SetDrawOption("COL2 TEXTE")
c1.Update()
c1.Modified()
c1.SetGrid(0,0)
CMS_lumi.CMS_lumi(c1,4,11)
c1.SaveAs("Pt_vs_Eta_SF__HLT_Mu45_eta2p1.png")
fout = TFile("Pt_vs_Eta__HLT_Mu45_eta2p1__SF.root", "recreate")
fout.cd()
dir = fout.mkdir("PtEtaBins")
dir.cd()
dir.WriteObject(clone_sf,"ptetasf")
fout.Write()
fout.Close()
