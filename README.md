git clone https://github.com/qyguo/lhe_related.git -b all

cd YOURPATH/MG5_aMC_v2_7_3
cp -r /data/pubfs/pku_visitor/guoqianying/public/cards/ YOURPATH/MG5_aMC_v2_7_3/../

LO:

./bin/mg5_aMC ../cards/ppeem_EZ/proc_card.dat
./bin/mg5_aMC ../cards/ppeem_ESZ/proc_card.dat
./bin/mg5_aMC ../cards/ppeem_SZ/proc_card.dat
./bin/mg5_aMC ../cards/ppeem_Z/proc_card.dat
./bin/mg5_aMC ../cards/ppeem/proc_card.dat
### sed -i "s/^.* = ptl / 10.0 = ptl /" ppeem*/Cards/run_card.dat
sed -i "s/^.* = use_syst/   False  = use_syst/"  ppeem*/Cards/run_card.dat
./ppeem_EZ/bin/generate_events
./ppeem_ESZ/bin/generate_events
./ppeem_SZ/bin/generate_events
./ppeem_Z/bin/generate_events
./ppeem/bin/generate_events
mkdir plots
cd plots
cp -r /data/pubfs/pku_visitor/guoqianying/public/cards/*.py ./
cp -r /data/pubfs/pku_visitor/guoqianying/public/cards/*.cc ./

cd YOURPATH/MG5_aMC_v2_7_3
cp -r /data/pubfs/pku_visitor/guoqianying/public/cards/ YOURPATH/MG5_aMC_v2_7_3/../
LO:
cp ../ppeem_EZ/Events/run_01/unweighted_events.lhe.gz ./ppeem_EZ_unweighted_events.lhe.gz
cp ../ppeem_ESZ/Events/run_01/unweighted_events.lhe.gz ./ppeem_ESZ_unweighted_events.lhe.gz
cp ../ppeem_SZ/Events/run_01/unweighted_events.lhe.gz ./ppeem_SZ_unweighted_events.lhe.gz
cp ../ppeem_Z/Events/run_01/unweighted_events.lhe.gz ./ppeem_Z_unweighted_events.lhe.gz
cp ../ppeem/Events/run_01/unweighted_events.lhe.gz ./ppeem_unweighted_events.lhe.gz
gunzip *.lhe.gz
python lhe.py plotsppeem_unweighted_events
python lhe.py plotsppeem_Z_unweighted_events
python lhe.py plotsppeem_SE_unweighted_events
python lhe.py plotsppeem_EZ_unweighted_events
python lhe.py plotsppeem_ESZ_unweighted_events
root -l -b -q draw_1f.cc\(\"ppeem_unweighted_events\"\)
root -l -b -q draw_1f.cc\(\"ppeem_Z_unweighted_events\"\)
root -l -b -q draw_1f.cc\(\"ppeem_EZ_unweighted_events\"\)
root -l -b -q draw_1f.cc\(\"ppeem_SE_unweighted_events\"\)
root -l -b -q draw_1f.cc\(\"ppeem_ESZ_unweighted_events\"\)

sed -i "s/^.*= cut_decays / True = cut_decays /" ppeem_Z/Cards/run_card.dat
./ppeem_Z/bin/generate_events
cd plots
cp ../ppeem_Z/Events/run_02/unweighted_events.lhe.gz ./ppeem_Z_2_unweighted_events.lhe.gz
gunzip ppeem_Z_2_unweighted_events.lhe.gz 
python lhe.py ppeem_Z_2_unweighted_events
root -l -b -q draw_1f.cc\(\"ppeem_Z_2_unweighted_events\"\)
root -l -b -q ./draw_1f_plus.cc


NLO:

./bin/mg5_aMC  ../cards/ppllm_NLO/proc_card.dat
sed -i "s/HERWIG6   = parton_shower/PYTHIA8   = parton_shower/" ppllm_NLO/Cards/run_card.dat
sed -i "s/^.*= fixed_fac_scale/ True     = fixed_fac_scale/" ppllm_NLO/Cards/run_card.dat
sed -i "s/^.*= fixed_ren_scale/ True     = fixed_ren_scale/" ppllm_NLO/Cards/run_card.dat
sed -i "s/^.*= nevents / 100 = nevents /" ppllm_NLO/Cards/run_card.dat
sed -i "s/^.*= jetalgo / -1.0  = jetalgo /" ppllm_NLO/Cards/run_card.dat
sed -i "s/^.*= jetradius /  0.4   = jetradius /" ppllm_NLO/Cards/run_card.dat
sed -i "s/^.*= ptj /  5.0   = ptj /" ppllm_NLO/Cards/run_card.dat
sed -i "s/^.*= ptgmin /  0.0   = ptgmin /" ppllm_NLO/Cards/run_card.dat
sed -i "s/^.*hadronize    = T /hadronize    = F /" ppllm_NLO/Cards/shower_card.dat 
sed -i "s/^.*njmax      = 0 /njmax      = -1.0 /" ppllm_NLO/Cards/shower_card.dat
sed -i "s/extralibs.*/extralibs    = stdhep Fmcfio dl     # Extra-libraries (not LHAPDF)/" ppllm_NLO/Cards/shower_card.dat
sed -i "s/EXTRALIBS.*/EXTRALIBS    = stdhep Fmcfio dl     # Extra-libraries (not LHAPDF)/" ppllm_NLO/Cards/shower_card.dat
./ppllm_NLO/bin/generate_events
./ppllm_NLO/bin/calculate_xsect


