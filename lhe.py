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

    if len(sys.argv)-1 != 1:
        KILL('two command-line arguments required: [1] input .lhe file name, such as unweight_lhe')

    ifile  = file      (sys.argv[1]+'.lhe', 'r')
    ofile = ROOT.TFile(sys.argv[1]+'.root', 'recreate')

    ###

    event_num_max = -1

    # find number of weights. begin with initial weight


    orig_wgt_label = 'SM'
    Nwgts = 1
    wgt_id = [orig_wgt_label]
#    print "wgt_id orig_wgt_label", wgt_id

    Line_N=0
    Marketed_L=0
    NoneIntergratedWeight=False
    tmp=""
    for line in ifile:
        Line_N+=1
        if line.replace(" ", "").startswith("<weightid="):
            Nwgts+=1
            wgt_id.append(line.split("'")[1])
        if line.replace(" ", "").startswith("<init>"):
            Marketed_L=Line_N+2
        if Line_N==Marketed_L:
            if line.startswith(" "):
                tmp=line.replace(" ", "", 1)
            else:
                tmp=line
        #if line.replace(" ", "").startswith("</weightgroup>"):
        #if line.startswith("<MGGenerationInfo>"):
        if line.replace(" ", "").startswith("</init>"):
            print "ccccccccccc: ", wgt_id
            break
    else:
        print "end of file reached. no new weights found"

    if tmp.startswith(" "):
        line=tmp.replace(" ","", 1)
    else:
        line=tmp
    IntegralWeight_SM=float(line.split(" ")[0])
    print "Integral Weight of SM: ", IntegralWeight_SM

    if type(IntegralWeight_SM+1) is not float:  
        sys.stderr.write("Warning. Break. The period was unknown. Integral Weight of SM is Known type. \n")
        sys.exit("sorry, goodbye!")


    ## define relevant histograms
    m_Z   = {}
    pT_Z  = {}
    m_2l  = {}
    pT_2l = {}
    pT_l = {}

    for k in wgt_id: # one histo per weight class
        label = k

        m_Z[k]  = ROOT.TH1F('m_Z_'+label , 'm_Z_'+label ,40, 40, 140)
        pT_Z[k]  = ROOT.TH1F('pT_Z_'+label , 'pT_Z_'+label , 40, 0, 160)
        m_2l[k]  = ROOT.TH1F('m_2l_'+label , 'm_2l_'+label ,50, 0, 160)
        pT_2l[k] = ROOT.TH1F('pT_2l_'+label , 'pT_2l_'+label , 40, 0, 160)
        pT_l[k] = ROOT.TH1F('pT_l_'+label , 'pT_l_'+label , 40, 0, 100)

        m_Z[k].Sumw2()
        pT_Z[k].Sumw2()
        m_2l[k].Sumw2()
        pT_2l[k].Sumw2()
        pT_l[k].Sumw2()
  
    event_num, in_event = 0, False

    # reads the lhe and looks into the events
    for line in ifile:
        if line[:1] == '#': continue
        if line.replace(" ", "").startswith('<scales'): continue

        if event_num_max > 0:
            if event_num > event_num_max: continue

        if line.replace(" ", "").startswith('<event>'):
            event_num += 1

            genp_ls = []
            weight = {}
            in_event = True
            continue

        if in_event:
            weight['SM'] = 1;

            if not line.replace(" ", "").startswith('</event>'):
                l0 = line.strip('\n')
                
                if l0.replace(" ", "").startswith('<wgt'):
                #if l0.startswith("wgt id='rw00"):
                    l1 = l0.split()
                    weight[l1[1].split("=")[1].strip("'>")] = float(l1[2])
                    continue

                if l0.replace(" ", "").startswith('<'): continue
                if len(l0.split()) == 6: 
                    weight[orig_wgt_label] = float(l0.split()[2])
                    continue

                genp_ls.append(l0)

            else:
                ### event analysis

                # define the four momentum of the dilepton pair. 

                Z_p4 = ROOT.TLorentzVector(0, 0, 0, 0)
                ll_p4 = ROOT.TLorentzVector(0, 0, 0, 0)
                ee_p4 = ROOT.TLorentzVector(0, 0, 0, 0)
                mm_p4 = ROOT.TLorentzVector(0, 0, 0, 0)
                tautau_p4 = ROOT.TLorentzVector(0, 0, 0, 0)

                for p in genp_ls:

                # for each particle in an event: extract four momentum
                    i_p4 = ROOT.TLorentzVector(lhep_px(p), lhep_py(p), lhep_pz(p), lhep_E(p))

                    if lhep_status(p) == 2: 
                        if abs(lhep_pdgID(p)) == 23: 
                           Z_p4 = i_p4
   
                    if lhep_status(p) == 1: 

                        #if abs(lhep_pdgID(p)) == 25: 
                        #   h_p4 = i_p4

                        # e or mu
                        if abs(lhep_pdgID(p)) == 11: 
                            ll_p4 += i_p4
                            ee_p4 += i_p4

                        if abs(lhep_pdgID(p)) == 13: 
                            ll_p4 += i_p4
                            mm_p4 += i_p4

                        if abs(lhep_pdgID(p)) == 15: 
                            ll_p4 += i_p4
                            tautau_p4 += i_p4

                        if abs(lhep_pdgID(p)) == 15 or abs(lhep_pdgID(p)) == 13 or abs(lhep_pdgID(p)) == 11:
                            for k in wgt_id:
                                pT_l[k].Fill(i_p4.Pt(), weight[k])


                # for each event: store the observables in the histograms
                for k in wgt_id:
                    #h_[k].Fill(h_p4.M(), weight[k]) 
                    #h_pth[k].Fill(h_p4.Pt(), weight[k]) 
                    #h_m4l[k].Fill(llll_p4.M(), weight[k]) 
                    #h_mll_min[k].Fill(min(ee_p4.M(), mm_p4.M()), weight[k]) 
                    #h_mll_max[k].Fill(max(ee_p4.M(), mm_p4.M()), weight[k]) 
                    m_Z[k].Fill(Z_p4.M(),weight[k])
                    pT_Z[k].Fill(Z_p4.Pt(),weight[k])
                    m_2l[k].Fill(ll_p4.M(),weight[k])
                    pT_2l[k].Fill(ll_p4.Pt(),weight[k])
                    

                in_event = False
                continue

    # output a root file
    ofile.cd()

    print("processed %i events" %event_num)


    xsec = {}
    xsec_ = {}
    xsec__ = {}
    xsec_1 = {}
    xsec_2 = {}
    for k in wgt_id:
        if k=="SM":
            event_num=event_num/IntegralWeight_SM
        m_Z[k].Scale(1./event_num)
        pT_Z[k].Scale(1./event_num)
        m_2l[k].Scale(1./event_num)
        pT_2l[k].Scale(1./event_num)
        pT_l[k].Scale(1./event_num)


        xsec_[k] = float(m_Z[k].GetSumOfWeights())
        print("m_Z integrated weight %s: %.3e" %(k, xsec_[k]))        
        xsec__[k] = float(pT_Z[k].GetSumOfWeights())
        print("pT_Z integrated weight %s: %.3e" %(k, xsec__[k]))        
        xsec[k] = float(m_2l[k].GetSumOfWeights())
        print("m_2l integrated weight %s: %.3e" %(k, xsec[k]))        
        xsec_1[k] = float(pT_2l[k].GetSumOfWeights())
        print("pT_2l integrated weight %s: %.3e" %(k, xsec_1[k]))        
        xsec_2[k] = float(pT_l[k].GetSumOfWeights())
        print("pT_l integrated weight %s: %.3e" %(k, xsec_2[k]))        

        m_Z[k].Write()
        pT_Z[k].Write()
        m_2l[k].Write()
        pT_2l[k].Write()
        pT_l[k].Write()

    ofile.Close()
    print("file %s produced" %sys.argv[1])
