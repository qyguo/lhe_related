#include <iostream>
#include <string>
using namespace std;
void draw_1f_plus()
{
    TFile *f1[5];
    TCanvas *c1 = new TCanvas("c1","distribution",200, 10, 700, 500);

    //c1->SetGrid();
    c1->SetLeftMargin(0.25);
    c1->SetBottomMargin(0.17);
    TH1F *h_1f;
    TH1F *h_1f_2;
    TH1F *h_1f_3;
    TH1F *h_1f_4 = new TH1F("m_2l_SM","m_2l_SM",50, 0, 160);
    TH1F *h_1f_41;
    TH1F *h_1f_42;

    string Name_InputFile = "ppeem_unweighted_events.root";
    string pathfile = "./";
    string Name_InputFile__ = pathfile+Name_InputFile;
    f1[0] = TFile::Open(Name_InputFile__.c_str());
    h_1f = (TH1F*)gDirectory->FindObjectAny("m_2l_SM");

    string Name_InputFile2 = "ppeem_Z_unweighted_events.root";
    string Name_InputFile__2 = pathfile+Name_InputFile2;
    f1[1] = TFile::Open(Name_InputFile__2.c_str());
    h_1f_2 = (TH1F*)gDirectory->FindObjectAny("m_2l_SM");

    string Name_InputFile3 = "ppeem_EZ_unweighted_events.root";
    string Name_InputFile__3 = pathfile+Name_InputFile3;
    f1[2] = TFile::Open(Name_InputFile__3.c_str());
    h_1f_3 = (TH1F*)gDirectory->FindObjectAny("m_2l_SM");

    string Name_InputFile4 = "ppeem_Z_2_unweighted_events.root";
    string Name_InputFile__4 = pathfile+Name_InputFile4;
    f1[3] = TFile::Open(Name_InputFile__4.c_str());
    h_1f_41 = (TH1F*)gDirectory->FindObjectAny("m_2l_SM");

    string Name_InputFile5 = "ppeem_ESZ_unweighted_events.root";
    string Name_InputFile__5 = pathfile+Name_InputFile5;
    f1[4] = TFile::Open(Name_InputFile__5.c_str());
    h_1f_42 = (TH1F*)gDirectory->FindObjectAny("m_2l_SM");

    h_1f->SetTitle("");
    h_1f->SetLineColor(1);
    h_1f->SetLineWidth(2);
    h_1f->GetXaxis()->SetTitle("M_{2l} GeV");
    h_1f->SetStats(0);
    h_1f->Draw("histsame");

    h_1f_41->SetTitle("");
    h_1f_41->Draw("histsame");
    h_1f_41->GetXaxis()->SetTitle("M_{2l} GeV");
    h_1f_41->SetLineColor(862);
    h_1f_41->SetLineWidth(2);
    h_1f_41->SetStats(0);

    h_1f_3->SetTitle("");
    h_1f_3->Draw("histsame");
    h_1f_3->GetXaxis()->SetTitle("M_{2l} GeV");
    h_1f_3->SetLineColor(814);
    h_1f_3->SetLineWidth(2);
    h_1f_3->SetStats(0);

    h_1f_4->Add(h_1f_41,h_1f_42);
    h_1f_4->SetTitle("");
    h_1f_4->GetYaxis()->SetTitleSize(0.03);
    h_1f_4->GetXaxis()->SetLabelSize(0.03);
    h_1f_4->GetYaxis()->SetLabelSize(0.03);
    h_1f_4->GetYaxis()->SetTitle("Cross Section (pb)");
    h_1f_4->GetXaxis()->SetTitle("M_{2l} GeV");
    h_1f_4->Draw("histsame");
    h_1f_4->SetLineColor(880);
    h_1f_4->SetLineWidth(2);
    h_1f_4->SetStats(0);
     

    TLegend *leg1 = new TLegend(0.65, 0.70, 0.8, 0.88);
    leg1->AddEntry(h_1f, "pp>e^{+}e^{-}", "l");
    leg1->AddEntry(h_1f_41, "pp>Z,Z>e^{+}e^{-}", "l");
    leg1->AddEntry(h_1f_3, "pp>e^{+}e^{-} / Z", "l");
    leg1->AddEntry(h_1f_4, "onShellZ + offShellZ ", "l");

    leg1->SetBorderSize(0);
    leg1->Draw();

    c1->SaveAs("test_comparison.pdf");
    c1->SaveAs("test_comparison.png");
    c1->SetLogy();
    c1->SaveAs("test_comparison_log.png");
    f1[0]->Close();
    f1[1]->Close();
    f1[2]->Close();
    f1[3]->Close();
    f1[4]->Close();
    exit(EXIT_FAILURE);

}

