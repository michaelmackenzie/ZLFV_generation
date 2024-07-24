//Plot Z mass distribution

int plot_z_mass(const char* file) {
  TFile* f = TFile::Open(file, "READ");
  if(!f) return 1;
  TTree* Events = (TTree*) f->Get("Events");
  if(!Events) return 2;

  TCanvas* c = new TCanvas();
  Events->Draw("recoGenParticles_genParticles__SIM.obj.m_state.p4Polar_.Phi()");
  c->SaveAs("phi.png");
  Events->Draw("recoGenParticles_genParticles__SIM.obj.m_state.pdgId_", "abs(recoGenParticles_genParticles__SIM.obj.m_state.pdgId_) < 40");
  c->SaveAs("pdg.png");
  Events->Draw("recoGenParticles_genParticles__SIM.obj.m_state.p4Polar_.Pt()", "recoGenParticles_genParticles__SIM.obj.m_state.pdgId_ == 23");
  c->SaveAs("pt.png");
  return 0;

  edm::Wrapper<vector<reco::GenParticle> > gen_part;
  Events->SetBranchAddress("recoGenParticles_genParticles__SIM.", &gen_part);
  Long64_t nentries = Events->GetEntries();
  TH1* hNGen = new TH1D("hNGen", "N(gen particles)", 1010, 0, 1010);
  TH1* hPt   = new TH1D("hpt"  , "pT", 1000, 0, 1000);
  for(Long64_t entry = 0; entry < nentries; ++entry) {
    Events->GetEntry(entry);
    hNGen->Fill(gen_part->size());
    for(int i = 0; i < gen_part->size(); ++i){
      reco::GenParticle p1 = gen_part->at(i);
      hPt->Fill(p1.pt());
    }
  }
  hNGen->Draw("hist");
  c->SaveAs("ngen.png");
  hPt->Draw("hist");
  c->SetLogy();
  c->SaveAs("pt.png");
  c->SetLogy(0);
  return 0;
}
