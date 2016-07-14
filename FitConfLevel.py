import ROOT as R 
import sys

filein = sys.argv[1]
n_bins = sys.argv[2]
x_axis_label = sys.argv[3]
fileout = sys.argv[4]

sf_file = R.TFile(filein)
asymm_graph = R.TGraphAsymmErrors(sf_file.Get("ScaleFactor"))
myfit = R.TF1("myfit","pol0")
asymm_graph.Fit("myfit")
error_graph = R.TGraphErrors(int(n_bins))
confinterval = R.TVirtualFitter.GetFitter()
for i in range(0,int(n_bins)):
    error_graph.SetPoint(i,asymm_graph.GetX()[i],0)
confinterval.GetConfidenceIntervals(error_graph)
error_graph.SetFillColor(R.kRed)
error_graph.SetFillStyle(3018)
error_graph.GetYaxis().SetRangeUser(0.5,1.5)
error_graph.GetXaxis().SetRangeUser(0.,1000.)
c1 = R.TCanvas("SF","SF")
c1.cd()
R.gStyle.SetOptStat(1111111)
R.gStyle.SetStatY(0.5)
R.gStyle.SetStatX(0.5)
R.gStyle->SetOptFit(); 
error_graph.Draw("a3")
c1.SetGridx()
c1.SetGridy()
c1.Update()
error_graph.GetXaxis().SetTitle("pT(e)[GeV]")
error_graph.GetYaxis().SetTitle("Trigger Scale Factor")
asymm_graph.Draw("same")
#error_graph.Draw("same a3")
c1.SaveAs(fileout+".png")
fout = R.TFile(fileout+".root", "RECREATE")
myfit.Write()
fout.Close()
