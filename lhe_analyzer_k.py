#!/usr/bin/env python
import sys, math, ROOT, copy

def KILL(log):
    print '\n@@@ FATAL -- '+log+'\n'
    raise SystemExit

def lhep_pdgID  (line): return int  (line.split()[ 0])
def lhep_status (line): return int  (line.split()[ 1])
def lhep_mother1(line): return int  (line.split()[ 2])
def lhep_mother2(line): return int  (line.split()[ 3])
def lhep_px     (line): return float(line.split()[ 6])
def lhep_py     (line): return float(line.split()[ 7])
def lhep_pz     (line): return float(line.split()[ 8])
def lhep_E      (line): return float(line.split()[ 9])
def lhep_M      (line): return float(line.split()[10])

def print_lhep(l):
    print lhep_pdgID  (l),
    print lhep_status (l),
    print lhep_mother1(l),
    print lhep_mother2(l),
    print lhep_px     (l),
    print lhep_py     (l),
    print lhep_pz     (l),
    print lhep_E      (l),
    print lhep_M      (l)

    return

### main
if __name__ == '__main__':

    if len(sys.argv)-1 != 2:
        KILL('two command-line arguments required: [1] input .lhe file, [2] output .root file')

    ifile  = file      (sys.argv[1], 'r')
    ofile = ROOT.TFile(sys.argv[2], 'recreate')

    ###

    event_num_max = -1

    # find number of weights. begin with initial weight

    orig_wgt_label = 'SM'
    Nwgts = 1
    wgt_id = [orig_wgt_label]
    print "wgt_id orig_wgt_label", wgt_id
    NNNN=0

    for line in ifile:
        #if line.startswith('<weight id'):
        #if line.startswith("<weight id='rw0"):
        #if line.startswith("<weight id='y"):
        if line.startswith("<weight id='k"):
            Nwgts+=1
            wgt_id.append(line.split("'")[1])
        #if line.startswith('</weightgroup>'):
        if line.startswith("<MGGenerationInfo>"):
            print "ccccccccccc: ", wgt_id
            break
    else:
        print "end of file reached. no new weights found"



    ## define relevant histograms
    h_ = {}
    h_pth = {}
    h_m4l = {}
    h_mll_min = {}
    h_mll_max = {}

    for k in wgt_id: # one histo per weight class
        label = k

        h_[k]  = ROOT.TH1F('mh_'+label , 'mh_'+label ,10, 110, 140)
        h_pth[k]  = ROOT.TH1F('pt_h_'+label , 'pt_h_'+label , 28, 0, 140)
        h_m4l[k]  = ROOT.TH1F('m4l_'+label , 'm4l_'+label ,10, 110, 140)
        h_mll_min[k]  = ROOT.TH1F('mllMin_'+label , 'mllMin_'+label ,10, 5, 65)
        h_mll_max[k]  = ROOT.TH1F('mllMax_'+label , 'mllMax_'+label ,10, 15, 115)

        h_[k].Sumw2()
        h_pth[k].Sumw2()
        h_m4l[k].Sumw2()
        h_mll_min[k].Sumw2()
        h_mll_max[k].Sumw2()
  
    event_num, in_event = 0, False

    # reads the lhe and looks into the events
    for line in ifile:
        if line[:1] == '#': continue
        if line.startswith('<scales'): continue

        if event_num_max > 0:
            if event_num > event_num_max: continue

        if line.startswith('<event>'):
            event_num += 1

            genp_ls = []
            weight = {}
            in_event = True
            continue

        if in_event:

            if not line.startswith('</event>'):
                l0 = line.strip('\n')
                
                if l0.startswith('<wgt'):
                #if l0.startswith("wgt id='rw00"):
                    l1 = l0.split()
                    weight[l1[1].split("=")[1].strip("'>")] = float(l1[2])
                    continue

                if l0.startswith('<'): continue
                if len(l0.split()) == 6: 
                    weight[orig_wgt_label] = float(l0.split()[2])
                    continue

                genp_ls.append(l0)

            else:
                ### event analysis

	        # define the four momentum of the dilepton pair. 

		h_p4 = ROOT.TLorentzVector(0, 0, 0, 0)
		llll_p4 = ROOT.TLorentzVector(0, 0, 0, 0)
                ee_p4 = ROOT.TLorentzVector(0, 0, 0, 0)
                mm_p4 = ROOT.TLorentzVector(0, 0, 0, 0)

                for p in genp_ls:

		    # for each particle in an event: extract four momentum
                    i_p4 = ROOT.TLorentzVector(lhep_px(p), lhep_py(p), lhep_pz(p), lhep_E(p))
		   
		    if lhep_status(p) == 1: 

                        if abs(lhep_pdgID(p)) == 25: 
                           h_p4 = i_p4

			# e or mu
                        if abs(lhep_pdgID(p)) == 11: 
                           llll_p4 += i_p4
                           ee_p4 += i_p4

                        if abs(lhep_pdgID(p)) == 13: 
                           llll_p4 += i_p4
                           mm_p4 += i_p4


                # for each event: store the observables in the histograms
                for k in wgt_id:
                        h_[k].Fill(h_p4.M(), weight[k]) 
                        h_pth[k].Fill(h_p4.Pt(), weight[k]) 
                        h_m4l[k].Fill(llll_p4.M(), weight[k]) 
                        h_mll_min[k].Fill(min(ee_p4.M(), mm_p4.M()), weight[k]) 
                        h_mll_max[k].Fill(max(ee_p4.M(), mm_p4.M()), weight[k]) 
                    

                in_event = False
                continue

    # output a root file
    ofile.cd()

    print("processed %i events" %event_num)


    xsec = {}
    xsec_ = {}
    xsec__ = {}
    for k in wgt_id:
        h_[k].Scale(1./event_num)
        h_pth[k].Scale(1./event_num)
        h_m4l[k].Scale(1./event_num)
        h_mll_min[k].Scale(1./event_num)
        h_mll_max[k].Scale(1./event_num)
        

        xsec_[k] = float(h_[k].GetSumOfWeights())
        print("h_ integrated weight %s: %.3e" %(k, xsec_[k]))        
        xsec__[k] = float(h_pth[k].GetSumOfWeights())
        print("h_pth integrated weight %s: %.3e" %(k, xsec__[k]))        
        xsec[k] = float(h_m4l[k].GetSumOfWeights())
        print("integrated weight %s: %.3e" %(k, xsec[k]))        



        h_[k].Write()
        h_pth[k].Write()
        h_m4l[k].Write()
        h_mll_min[k].Write()
        h_mll_max[k].Write()

    ofile.Close()
    print("file %s produced" %sys.argv[2])                                 
