import os
import glob
import math
import array
import sys
import time
from optparse import OptionParser
import ROOT
from ROOT import *
from math import sqrt

def main(options,args):
    variations = []
    if options.muonCR:
        plots = [
            'h_Mpass',
            'h_Mfail',
        ]
        bkgSamples = ['qcd','wlnu','tqq','stqq','vvqq'] 
        variations = ['mutriggerUp','mutriggerDown','PuUp','PuDown','muisoUp','muisoDown','muidUp','muidDown','JESUp','JESDown','JERUp','JERDown',
                      'matched','unmatched','semimatched']  
    else:
        plots = [
            'h_Lpass',
            'h_Mpass',
            'h_Lfail',
            'h_Mfail',
        ]

        bkgSamples = ['qcd','zqq','wqq','tqq'] 
        variations =  ['triggerUp','triggerDown','PuUp','PuDown','matched','unmatched','semimatched','JESUp','JESDown','JERUp','JERDown']

    dataSamples = ['data_obs']

    ifile = options.ifile
    lumi = options.lumi

    ofile = ROOT.TFile.Open(ifile,'read')
    hnew = {}
    hnew['L'] = {}
    hnew['M'] = {}
    for plot in plots:
        print(plot)
        hb = {}; hb2d = {}
        for process in bkgSamples:
            try:
                hb[process] = ofile.Get(plot.replace('h_',process+'_')).ProjectionX().Clone()
            except:
                print(plot.replace('h_',process+'_'))
                hb[process] = ofile.Get(plot.replace('h_',process+'_')).Clone()
            hb[process].SetDirectory(0)
            hb2d[process] = ofile.Get(plot.replace('h_',process+'_')).Clone()
            hb2d[process].SetDirectory(0)

        try:
            hd = ofile.Get(plot.replace('h_','data_obs_')).ProjectionX().Clone()
        except:
            hd = ofile.Get(plot.replace('h_','data_obs_')).Clone()
        hd.SetDirectory(0)
        hd2d = ofile.Get(plot.replace('h_','data_obs_')).Clone()
        hd2d.SetDirectory(0)

        if options.muonCR:
            new = hb.copy()
            # separate tqq by template
            # if '_Mpass' in plot or '_Mfail' in plot:
            #     new['tqq_matched'] = ofile.Get(plot.replace('h_','tqq_')+'_matched').Clone()
            #     new['tqq_unmatched'] = ofile.Get(plot.replace('h_','tqq_')+'_unmatched').Clone()
            #     new['tqq_semimatched'] = ofile.Get(plot.replace('h_','tqq_')+'_semimatched').Clone()
            #     # remove tqq
            #     n = new.pop("tqq", None) 
            # scale QCD for muon CR 
            #new['qcd'].Scale(0.8467)
            #hb['qcd'].Scale(0.8467)
        else:
            new = hb.copy()
            # separate tqq by template   
            # if '_Mpass' in plot or '_Mfail' in plot:
            #     new['tqq_matched'] = ofile.Get(plot.replace('h_','tqq_')+'_matched').ProjectionX().Clone()
            #     new['tqq_unmatched'] = ofile.Get(plot.replace('h_','tqq_')+'_unmatched').ProjectionX().Clone()
            #     new['tqq_semimatched'] = ofile.Get(plot.replace('h_','tqq_')+'_semimatched').ProjectionX().Clone()
            #     # remove tqq                                                                                                                                                      
            #     n = new.pop("tqq", None)

        for wp in ['L','M']:
            if plot=='h_%spass'%wp or plot=='h_%sfail'%wp:
                for key in hb.keys():
                    hnew[wp][key+plot] = hb2d[key].Clone(hb2d[key].GetName().replace(wp,''))
                    hnew[wp][key+plot].SetDirectory(0)
                hnew[wp]['data_obs'+plot] = hd2d.Clone(hd2d.GetName().replace(wp,''))
                hnew[wp]['data_obs'+plot].SetDirectory(0)
                for var in variations:
                    for process in bkgSamples:
                        if process in ['qcd']: continue # no variations for qcd
                        hnew[wp][var+plot+process] = ofile.Get(plot.replace('h_',process+'_')+'_'+var).Clone(plot.replace('h_',process+'_').replace(wp,'')+'_'+var)
                        hnew[wp][var+plot+process].SetDirectory(0)

    for wp in ['M']:
        newfile = ROOT.TFile.Open(ifile.replace('.root','_%s.root'%wp),'RECREATE')
        for key,h in hnew[wp].iteritems():
            h.Write()
        newfile.Close()

        # write loose templates for wqq and zqq
        if wp=='M' and not 'hbbSM' in ifile:
            newfile = ROOT.TFile.Open(ifile.replace('.root','_%s_looserWZ.root'%wp),'RECREATE')
            for process in ['wqq','zqq']:
                for cat in ['pass','fail']:
                    name = '%sh_L%s'%(process,cat)
                    h = hnew['L'][name].Clone()
                    h.Write()
                    for var in variations:
                        name = '%sh_L%s%s'%(var,cat,process)
                        h = hnew['L'][name].Clone()
                        h.Write()
            newfile.Close()

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('-i','--ifile', dest='ifile', default = 'input.root',help='directory with data', metavar='idir')
    parser.add_option("--muonCR", action='store_true', default =False, help="muonCR")
    (options, args) = parser.parse_args()

    import tdrstyle
    tdrstyle.setTDRStyle()
    ROOT.gStyle.SetPadTopMargin(0.10)
    ROOT.gStyle.SetPadLeftMargin(0.16)
    ROOT.gStyle.SetPadRightMargin(0.10)
    ROOT.gStyle.SetPalette(1)
    ROOT.gStyle.SetPaintTextFormat("1.1f")
    ROOT.gStyle.SetOptFit(0000)
    ROOT.gROOT.SetBatch()

    main(options,args)
