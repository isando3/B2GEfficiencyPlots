import ROOT
import sys
from math import sqrt, pow
from array import array
import tdrstyle , CMS_lumi

#Setting up size of canvas
H_ref = 600
W_ref = 800
W = W_ref
H  = H_ref
#c1 = TCanvas('c1',"Plot",1)
T = 0.08*H_ref
B = 0.12*H_ref
L = 0.12*W_ref
R = 0.04*W_ref
c1 = ROOT.TCanvas("c1","c1",50,50,W,H)
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


f1 = ROOT.TFile(sys.argv[1],'r')#data
f2 = ROOT.TFile(sys.argv[2],'r')#MC
trig_name = sys.argv[3]
fout = ROOT.TFile(sys.argv[4], 'recreate')

variables = {'lep_pt':'pT_{l}[GeV]','lep_eta':'#eta_{l}','minDR':'#Delta R_{min}','jet1_pt':'pT_{jet1}[GeV]','jet2_pt':'pT_{jet2}[GeV]'}

for variable in variables:
    graph1 = f1.Get(variable)
    graph2 = f2.Get(variable)
    n = graph1.GetN()
    x1, y1, yerr_up1, yerr_down1, x2, y2, yerr_up2, yerr_down2, xerr_left, xerr_right  = [], [], [], [], [], [], [],[], [], []
    x12, y12 , yerr_up12, yerr_down12, xerr_left12, xerr_right12 = [],[],[],[],[],[]
    for i in range(n):
        tmpX1, tmpY1, tmpX2, tmpY2 = ROOT.Double(0), ROOT.Double(0), ROOT.Double(0), ROOT.Double(0)
        graph1.GetPoint(i, tmpX1, tmpY1)
        graph2.GetPoint(i, tmpX2, tmpY2)
        x1.append(tmpX1)
        x2.append(tmpX2)
        y1.append(tmpY1)
        yerr_up1.append(graph1.GetErrorYhigh(i))
        yerr_down1.append(graph1.GetErrorYlow(i))
        y2.append(tmpY2)
        yerr_up2.append(graph2.GetErrorYhigh(i))
        yerr_down2.append(graph2.GetErrorYlow(i))
        xerr_left.append(graph2.GetErrorXlow(i))
        xerr_right.append(graph2.GetErrorXhigh(i))
    print len(x1)
    print y1[0]
    print y2[0]
    y12=[0.]*len(x1)
    yerr_down12 = [0.]*len(x1)
    yerr_up12 = [0.]*len(x1)

    for j in  xrange(len(x1)):
        y12[j] = y1[j]/y2[j]
        yerr_down12[j]= sqrt(pow(y12[j],2)*(pow(yerr_down1[j]/y1[j], 2)+pow(yerr_down2[j]/y2[j],2)))
        yerr_up12[j]= sqrt(pow(y12[j],2)*(pow(yerr_up1[j]/y1[j], 2)+pow(yerr_up2[j]/y2[j],2)))
     #x12[j] = x1[j]
     #xerr_left12 = xerr_left[j]
     #xerr_right12 = xerr_right[j]
    ax1 = array("d",x1)
    ay12 = array("d",y12)
    axel = array("d",xerr_left)
    axer = array("d", xerr_right)
    ayd12 = array("d", yerr_down12)
    ayu12 = array("d", yerr_up12)
    sf =  ROOT.TGraphAsymmErrors(len(x1),ax1,ay12,axel,axer,ayd12,ayu12)
    #ROOT.gStyle.SetOptFit()
    sf.SetTitle(" ")
    sf.GetYaxis().SetTitle("Trigger Scale Factor")
    sf.SetMarkerColor(1)
    sf.SetMarkerStyle(20)
    sf.GetYaxis().SetRangeUser(0.,1.5)
    sf.GetXaxis().SetTitle(variables[variable])
    #myfit = ROOT.TF1("myfit","pol0")
    #sf.Fit("myfit")
    sf.Draw("AP")
    c1.Update()
    c1.SetGrid()
    c1.Modified()
    CMS_lumi.CMS_lumi(c1,4,11)
    c1.SaveAs("SF_"+trig_name+"__"+variable+".png")
    fout.WriteTObject(sf, "SF_"+variable)
fout.Close
