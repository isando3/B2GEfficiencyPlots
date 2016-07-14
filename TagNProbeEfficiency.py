import re
import sys
from ROOT import *
from array import array
import tdrstyle , CMS_lumi

from optparse import OptionParser
parser = OptionParser()
import glob
import os

# _ __   __ _ _ __ ___  ___ _ __ 
#| '_ \ / _` | '__/ __|/ _ \ '__|
#| |_) | (_| | |  \__ \  __/ |   
#| .__/ \__,_|_|  |___/\___|_|   
#| |                             
#|_| 
#
parser.add_option('--channel', type='string', action='store',
                  default='e',
                  dest='channel',
                  help='mu or e?')

parser.add_option('--tag', type='string', action='store',
                  default='HLT_Mu45_eta2p1_v1',
                  dest='tag',
                  help='tag trigger')

parser.add_option('--probe', type='string', action='store',
                  default='HLT_Ele45PFJet200PFJet50',
                  dest='probe',
                  help='probe trigger')

parser.add_option('--ORprobe', type='string', action='store',
                  default='HLT_PFHT900_v1',
                  dest='ORprobe',
                  help='or probe trigger')

parser.add_option('--useOR', type='string', action='store',
                  default='False',
                  dest='useOR',
                  help='Use Or combination or trigger?')

parser.add_option('--sample', type='string', action='store',
                  default='TTbar',
                  dest='sample',
                  help='Sample used:')

parser.add_option('--file', type='string', action='store',
                  default='uhh.AnalysisRunner.TTbar.root',
                  dest='file',
                  help='File to be analyzed')


parser.add_option('--tagdir', type='string', action='store',
                  default='trigtag',
                  dest='tagdir',
                  help='Directory where the tag files are')


parser.add_option('--probedir', type='string', action='store',
                  default='trigprobe',
                  dest='probedir',
                  help='Directory where the probe files are')

parser.add_option('--foutname', type='string', action='store',
                  default='data.root',
                  dest='foutname',
                  help='name of the output root file: data.root or ttbar.root')

parser.add_option('--applyfit', action="store_true",
                  default=False,
                  dest='applyfit',
                  help='Apply fit: True or False')
(options, args) = parser.parse_args()
argv = []

#options, remainder = parser.parse_args()
if len(sys.argv[1:]) == 0:
    print "no argument given!"
    parser.print_help()
    sys.exit(1)
#type here an example of how to use this script: 

#Setting up size of canvas
H_ref = 1200; 
W_ref = 1800; 
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


#file & input histograms

f1 = TFile(options.file)
fout = TFile(options.foutname, "recreate")
tag_d = options.tagdir
probe_d = options.probedir
if options.channel == 'e':
    leptag_pt = f1.Get(tag_d+'/ele1__pt')
    leptag_eta= f1.Get(tag_d+'/ele1__eta')
    leptag_minDR_jet = f1.Get(tag_d+'/ele1__minDR_jet')
    lepprobe_pt = f1.Get(probe_d+'/ele1__pt')
    lepprobe_eta= f1.Get(probe_d+'/ele1__eta')
    lepprobe_minDR_jet =f1.Get(probe_d+'/ele1__minDR_jet')
elif options.channel == 'mu':
    leptag_pt = f1.Get(tag_d+'/muo1__pt')
    leptag_eta= f1.Get(tag_d+'/muo1__eta')
    leptag_minDR_jet = f1.Get(tag_d+'/muo1__minDR_jet')
    lepprobe_pt = f1.Get(probe_d+'/muo1__pt')
    lepprobe_eta= f1.Get(probe_d+'/muo1__eta')
    lepprobe_minDR_jet =f1.Get(probe_d+'/muo1__minDR_jet')
jet1tag_pt=f1.Get(tag_d+'/jet1__pt')
jet1tag_eta=f1.Get(tag_d+'/jet1__eta')
jet2tag_pt=f1.Get(tag_d+'/jet2__pt')
jet2tag_eta = f1.Get(tag_d+'/jet2__eta')
jet1probe_pt=f1.Get(probe_d+'/jet1__pt')
jet1probe_eta=f1.Get(probe_d+'/jet1__eta')
jet2probe_pt=f1.Get(probe_d+'/jet2__pt')
jet2probe_eta =f1.Get(probe_d+'/jet2__eta')

## Update canvas 
gROOT.SetBatch(kTRUE)
c1.cd()
gStyle.SetOptTitle(0)
gStyle.SetOptStat(0)
gStyle.SetTitleFontSize(0.1)
c1.Modified()
CMS_lumi.CMS_lumi(c1,4,11)
c1.Update()
useOR = options.useOR
p = TH1F()
q = TH1F()
#lep pt 
x= array("d",[0.,25.,50.,75.,100.,125.,150.,200.,300.,500.,700.,900.])
p=lepprobe_pt.Rebin(11,"lepprobe_pt",x)
q=leptag_pt.Rebin(11,"leptag_pt",x)
eff_lep_pt = TEfficiency(p,q)
eff_lep_pt.SetMarkerStyle(20)
if useOR =='True':
    title_lep_pt = 'TagNProbe; pT_{'+options.channel+'}[GeV]; Eff['+options.probe+'||'+options.ORprobe+']'
else:
    title_lep_pt = 'TagNProbe; pT_{'+options.channel+'}[GeV]; Eff['+options.probe+']'
eff_lep_pt.SetTitle(title_lep_pt)
tgraph2 = TGraphAsymmErrors()
eff_lep_pt.Draw()
eff_lep_pt.Paint("")
tgraph2 = eff_lep_pt.GetPaintedGraph()
tgraph2.GetYaxis().SetRangeUser(0.,1.1)
tgraph2.SetLineColor(0)
tgraph2.SetMarkerStyle(20)
if (options.applyfit):
    fit = tgraph2.Fit("pol0",'S')
    value = fit.Parameter(0)
    error = fit.ParError(0)
#print value, error
tgraph2.Draw("P")
fout.WriteObject(tgraph2,"lep_pt")
c1.Update()
c1.SetGrid()
gStyle.SetTitleFontSize(0.1)
c1.Update()
c1.Modified()
CMS_lumi.CMS_lumi(c1,4,11)
text = TLatex()
text.SetNDC()
uppertitle = 'Tag-And-Probe('+ options.sample+')'
text.DrawText(0.3,0.95,uppertitle)
if (options.applyfit):
    text2 = TLatex()
    text2.SetNDC()
    text2.SetTextSize(0.04)
    text2.DrawText(0.2,0.45,'Eff:'+str("{0:.4f}".format(value))+'+/-'+str("{0:.4f}".format(error)))
ssleppt = 'TagNProbe_'+ options.sample+ '_' + options.channel + '_pt.png'
c1.SaveAs(ssleppt)
c1.Clear()
#ele eta
c1.cd()
lepprobe_eta.Rebin(2)
leptag_eta.Rebin(2)
eff_lep_eta = TEfficiency(lepprobe_eta,leptag_eta)
eff_lep_eta.SetMarkerStyle(20)
if useOR=='True':
    title_lep_eta = 'TagNProbe; \eta_{'+options.channel+'}; Eff['+options.probe+'||'+options.ORprobe+']'
else:
    title_lep_eta = 'TagNProbe; \eta_{'+options.channel+'}; Eff['+options.probe+']'
eff_lep_eta.SetTitle(title_lep_eta)
tgraph2 = TGraphAsymmErrors()
eff_lep_eta.Draw()
eff_lep_eta.Paint("")
tgraph2 = eff_lep_eta.GetPaintedGraph()
tgraph2.GetYaxis().SetRangeUser(0.,1.1)
tgraph2.SetLineColor(0)
tgraph2.SetMarkerStyle(20)
if (options.applyfit):
    fit = tgraph2.Fit("pol0",'S')
    value = fit.Parameter(0)
    error = fit.ParError(0)
tgraph2.Draw("P") 
fout.WriteObject(tgraph2,"lep_eta")
c1.Update()
c1.SetGrid()
gStyle.SetTitleFontSize(0.1)
c1.Update()
c1.Modified()
CMS_lumi.CMS_lumi(c1,4,11)
text = TLatex()
text.SetNDC()
text.DrawText(0.3,0.95,uppertitle)
if (options.applyfit):
    text2 = TLatex()
    text2.SetNDC()
    text2.SetTextSize(0.04)
    text2.DrawText(0.2,0.45,'Eff:'+str("{0:.4f}".format(value))+'+/-'+str("{0:.4f}".format(error)))
sslepeta = 'TagNProbe_'+ options.sample+ '_' + options.channel + '_eta.png'
c1.SaveAs(sslepeta)
c1.Clear()
#ele minDR
c1.cd()
leptag_minDR_jet.Rebin(2)
lepprobe_minDR_jet.Rebin(2)
eff_lep_minDR = TEfficiency(lepprobe_minDR_jet,leptag_minDR_jet)
eff_lep_minDR.SetMarkerStyle(20)
if useOR =='True':
    title_lep_minDR = 'TagNProbe; min \Delta R_{'+options.channel+'-jet}; Eff['+options.probe+'||'+options.ORprobe+']'
else:
    title_lep_minDR = 'TagNProbe; min \Delta R_{'+options.channel+'-jet}; Eff['+options.probe+']'
eff_lep_minDR.SetTitle(title_lep_minDR)
tgraph2 = TGraphAsymmErrors()
eff_lep_minDR.Draw()
eff_lep_minDR.Paint("")
tgraph2 = eff_lep_minDR.GetPaintedGraph()
tgraph2.GetYaxis().SetRangeUser(0.,1.1)
tgraph2.SetLineColor(0)
tgraph2.SetMarkerStyle(20)
if options.applyfit:
    fit = tgraph2.Fit("pol0",'S')
    value = fit.Parameter(0)
    error = fit.ParError(0)
tgraph2.Draw("P") 
fout.WriteObject(tgraph2,"minDR")
c1.Update()
c1.SetGrid()
gStyle.SetTitleFontSize(0.1)
c1.Update()
c1.Modified()
CMS_lumi.CMS_lumi(c1,4,11)
text = TLatex()
text.SetNDC()
text.DrawText(0.3,0.95,uppertitle)
if options.applyfit:
    text2 = TLatex()
    text2.SetNDC()
    text2.SetTextSize(0.04)
    text2.DrawText(0.2,0.45,'Eff:'+str("{0:.4f}".format(value))+'+/-'+str("{0:.4f}".format(error)))
sslepDR = 'TagNProbe_'+ options.sample+ '_' + options.channel + '_minDR.png'
c1.SaveAs(sslepDR)
c1.Clear()
#jet1_pt
j1probe = TH1F()
j1tag = TH1F()
j1pt = array("d",[170.,200.,250.,300.,350.,400.,500.,700.,900.])
j1probe = jet1probe_pt.Rebin(8,"j1probe",j1pt)
j1tag = jet1tag_pt.Rebin(8,"j1tag",j1pt)
eff_jet1_pt = TEfficiency(j1probe,j1tag)
eff_jet1_pt.SetMarkerStyle(20)
if useOR =='True':
    title_jet1pt = 'TagNProbe; pT_{jet1}[GeV]; Eff['+options.probe+'||'+options.ORprobe+']'
else:
    title_jet1pt = 'TagNProbe; pT_{jet}[GeV]; Eff['+options.probe+']'
eff_jet1_pt.SetTitle(title_jet1pt)
tgraph2 = TGraphAsymmErrors()
eff_jet1_pt.Draw()
eff_jet1_pt.Paint("")
tgraph2 = eff_jet1_pt.GetPaintedGraph()
tgraph2.GetYaxis().SetRangeUser(0.,1.1)
tgraph2.SetLineColor(0)
tgraph2.SetMarkerStyle(20)
if options.applyfit:
    fit = tgraph2.Fit("pol0",'S')
    value = fit.Parameter(0)
    error = fit.ParError(0)
tgraph2.Draw("P") 
fout.WriteObject(tgraph2,"jet1_pt")
c1.Update()
c1.SetGrid()
gStyle.SetTitleFontSize(0.1)
c1.Update()
c1.Modified()
CMS_lumi.CMS_lumi(c1,4,11)
text = TLatex()
text.SetNDC()
text.DrawText(0.3,0.95,uppertitle)
if options.applyfit:
    text2 = TLatex()
    text2.SetNDC()
    text2.SetTextSize(0.04)
    text2.DrawText(0.2,0.45,'Eff:'+str("{0:.4f}".format(value))+'+/-'+str("{0:.4f}".format(error)))
ssjet1pt = 'TagNProbe_'+ options.sample+ '_' + options.channel + '_jet1pt.png'
c1.SaveAs(ssjet1pt)
c1.Clear()
#jet1_eta
jet1probe_eta.Rebin(3)
jet1tag_eta.Rebin(3)
eff_jet1_eta = TEfficiency(jet1probe_eta,jet1tag_eta)
eff_jet1_eta.SetMarkerStyle(20)
if useOR == 'True':
    title_jet1eta = 'TagNProbe; \eta_{jet1}; Eff['+options.probe+'||'+options.ORprobe+']'
else:
    title_jet1eta = 'TagNProbe; \eta_{jet}; Eff['+options.probe+']'
eff_jet1_eta.SetTitle(title_jet1eta)
tgraph2 = TGraphAsymmErrors()
eff_jet1_eta.Draw()
eff_jet1_eta.Paint("")
tgraph2 = eff_jet1_eta.GetPaintedGraph()
tgraph2.GetYaxis().SetRangeUser(0.,1.1)
tgraph2.SetLineColor(0)
tgraph2.SetMarkerStyle(20)
if options.applyfit:
    fit = tgraph2.Fit("pol0",'S')
    value = fit.Parameter(0)
    error = fit.ParError(0)
tgraph2.Draw("P") 
c1.Update()
c1.SetGrid()
gStyle.SetTitleFontSize(0.1)
c1.Update()
c1.Modified()
CMS_lumi.CMS_lumi(c1,4,11)
text = TLatex()
text.SetNDC()
text.DrawText(0.3,0.95, uppertitle)
if options.applyfit:
    text2 = TLatex()
    text2.SetNDC()
    text2.SetTextSize(0.04)
    text2.DrawText(0.2,0.45,'Eff:'+str("{0:.4f}".format(value))+'+/-'+str("{0:.4f}".format(error)))
ssjet1eta = 'TagNProbe_'+ options.sample+ '_' + options.channel + '_jet1eta.png'
c1.SaveAs(ssjet1eta)
c1.Clear()
j2pt = array("d",[75.,100.,150.,250.,350.,450.,650.,1000.])
j2probe = jet2probe_pt.Rebin(7,"j2probe",j2pt)
j2tag = jet2tag_pt.Rebin(7,"j2tag",j2pt)
eff_jet2_pt = TEfficiency(j2probe,j2tag)
eff_jet2_pt.SetMarkerStyle(20)
if useOR == 'True':
    title_jet2pt = 'TagNProbe; pT_{jet1}[GeV]; Eff['+options.probe+'||'+options.ORprobe+']'
else:
    title_jet2pt = 'TagNProbe; pT_{jet2} [GeV]; Eff['+options.probe+']'
eff_jet2_pt.SetTitle(title_jet2pt)
tgraph2 = TGraphAsymmErrors()
eff_jet2_pt.Draw()
eff_jet2_pt.Paint("")
tgraph2 = eff_jet2_pt.GetPaintedGraph()
tgraph2.GetYaxis().SetRangeUser(0.,1.1)
tgraph2.SetLineColor(0)
tgraph2.SetMarkerStyle(20)
if options.applyfit:
    fit = tgraph2.Fit("pol0",'S')
    value = fit.Parameter(0)
    error = fit.ParError(0)
tgraph2.Draw("P") 
fout.WriteObject(tgraph2,"jet2_pt")
c1.Update()
c1.SetGrid()
gStyle.SetTitleFontSize(0.1)
c1.Update()
c1.Modified()
CMS_lumi.CMS_lumi(c1,4,11)
text = TLatex()
text.SetNDC()
text.DrawText(0.3,0.95,uppertitle)
if options.applyfit:
    text2 = TLatex()
    text2.SetNDC()
    text2.SetTextSize(0.04)
    text2.DrawText(0.2,0.45,'Eff:'+str("{0:.4f}".format(value))+'+/-'+str("{0:.4f}".format(error)))
ssjet2pt = 'TagNProbe_'+ options.sample+ '_' + options.channel + '_jet2pt.png'
c1.SaveAs(ssjet2pt)
c1.Clear()
#jet2_eta
jet2probe_eta.Rebin(3)
jet2tag_eta.Rebin(3)
eff_jet2_eta = TEfficiency(jet2probe_eta,jet2tag_eta)
eff_jet2_eta.SetMarkerStyle(20)
if useOR == 'True':
    title_jet2eta = 'TagNProbe; \eta_{jet1}; Eff['+options.probe+'||'+options.ORprobe+']'
else:
    title_jet2eta = 'TagNProbe; \eta_{jet2}; Eff['+options.probe+']'
eff_jet2_eta.SetTitle(title_jet2eta)
tgraph2 = TGraphAsymmErrors()
eff_jet2_eta.Draw()
eff_jet2_eta.Paint("")
tgraph2 = eff_jet2_eta.GetPaintedGraph()
tgraph2.GetYaxis().SetRangeUser(0.,1.1)
tgraph2.SetLineColor(0)
tgraph2.SetMarkerStyle(20)
if options.applyfit:
    fit = tgraph2.Fit("pol0",'S')
    value = fit.Parameter(0)
    error = fit.ParError(0)
tgraph2.Draw("P") 
fout.WriteObject(tgraph2,"jet2eta")
#fout.Close()
c1.Update()
c1.SetGrid()
gStyle.SetTitleFontSize(0.1)
c1.Update()
c1.Modified()
CMS_lumi.CMS_lumi(c1,4,11)
text = TLatex()
text.SetNDC()
text.DrawText(0.3,0.95,uppertitle)
if options.applyfit:
    text2 = TLatex()
    text2.SetNDC()
    text2.SetTextSize(0.04)
    text2.DrawText(0.2,0.45,'Eff:'+str("{0:.4f}".format(value))+'+/-'+str("{0:.4f}".format(error)))
ssjet2eta = 'TagNProbe_'+ options.sample+ '_' + options.channel + '_jet2eta.png'
c1.SaveAs(ssjet2eta)
c1.Clear()
#Create now the 2D Eff maps 
pt_vs_eta_tag = f1.Get(tag_d+"/lep_pt_VS_lep_eta")
pt_vs_eta_probe = f1.Get(probe_d+"/lep_pt_VS_lep_eta")
pt_vs_eta_tag.SetTitle("Efficiency("+options.sample+")")
pt_vs_eta_eff = pt_vs_eta_tag.Clone()
#pt_vs_eta_tag.SetTitle("Efficiency("+options.sample+")")
#clone_h = TEfficiency(den_h,num_h)
c2 = TCanvas("c2","c2",1000,600)
c2.Clear()
c2.cd()
#CMS_lumi.CMS_lumi(c2,4,11)
pt_vs_eta_eff.Divide(pt_vs_eta_probe, pt_vs_eta_tag, 1.0, 1.0, "B")
gStyle.SetPaintTextFormat("2.2f")
pt_vs_eta_eff.SetMarkerSize(0.5)
pt_vs_eta_eff.SetTitle("HLT Efficiency")
pt_vs_eta_eff.Draw("TEXTE COLZ")
#c1.SetTickx(0)
#c1.SetTicky(1)
c2.Update()
c2.Modified()
c2.SetGrid(0,0)
CMS_lumi.CMS_lumi(c2,4,11)
c2.SaveAs("Pt_vs_Eta_Eff_"+options.sample+ "__"+ options.probe+".png")
#fout = TFile("HLT_Ele50PFJET_or_HLT_Ele105__TTbar__Eff.root", "recreate")
#fout.cd()
dir = fout.mkdir("PtEtaBins")
dir.cd()
dir.WriteObject(pt_vs_eta_eff,"ptetadata")
#fout.Write()
fout.Close()

