#include <iostream>
#include <string>
using namespace std;
void draw_1f(const string & _name_DS_="ppeem_unweighted_events")
{
    TFile *f1;
    TCanvas *c1 = new TCanvas("c1","distribution",200, 10, 700, 500);

    //c1->SetGrid();
    c1->SetLeftMargin(0.25);
    c1->SetBottomMargin(0.17);
    TH1F *h_1f;

    string Name_InputFile = (_name_DS_+".root").c_str();
    
    string pathfile = "./";
    string Name_InputFile__ = pathfile+Name_InputFile;
    f1 = TFile::Open(Name_InputFile__.c_str());
    
    h_1f = (TH1F*)gDirectory->FindObjectAny("m_2l_SM");
    h_1f->SetTitle("");
    
    h_1f->GetYaxis()->SetTitleSize(0.03);

    h_1f->GetXaxis()->SetLabelSize(0.03);
    h_1f->GetYaxis()->SetTitle("Cross Section (pb)");
    h_1f->GetYaxis()->SetLabelSize(0.03);
    
    h_1f->Draw();
    h_1f->GetXaxis()->SetTitle("M_{2l} GeV");

    h_1f->SetStats(0);
    
    c1->SaveAs((_name_DS_+".pdf").c_str());
    c1->SaveAs((_name_DS_+".png").c_str());
    c1->SetLogy();
    c1->SaveAs((_name_DS_+"_log.png").c_str());
    f1->Close();
    exit(EXIT_FAILURE);

}

