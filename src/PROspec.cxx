#include "PROspec.h"
using namespace PROfit;

PROspec::PROspec(long int num_bins):
    spec(Eigen::VectorXd::Zero(num_bins)),
    error_square(Eigen::VectorXd::Zero(num_bins)){
}

void PROspec::Zero(){
    log<LOG_INFO>(L"%1% || Zero out spectrum") % __func__ ;
    spec.setZero();
    error_square.setZero();
    return;
}

void PROspec::Fill(long int bin_index, double weight){
    log<LOG_DEBUG>(L"%1% || Fill in weight: %2% to bin: %3%") % __func__ % weight % bin_index;
    spec[bin_index] += weight;
    error_square[bin_index] += std::pow(weight, 2.0);
    return;
}


TH1D PROspec::toTH1D(PROconfig const & inconfig, int subchannel_index){

    long int global_bin_start = inconfig.GetGlobalBinStart(subchannel_index);
    int channel_index = inconfig.GetChannelIndex(subchannel_index);

    //set up hist specs
    int nbins = inconfig.m_channel_num_bins[channel_index];
    const std::vector<double>& bin_edges = inconfig.GetChannelBinEdges(channel_index);
    std::string hist_name = inconfig.m_fullnames[subchannel_index];
    std::string xaxis_title = inconfig.m_channel_units[channel_index];

    TH1D hSpec(hist_name.c_str(),hist_name.c_str(), nbins, &bin_edges[0]); 
    hSpec.GetXaxis()->SetTitle(xaxis_title.c_str());
    for(int i = 1; i <= nbins; ++i){
	hSpec.SetBinContent(i, spec[global_bin_start + i -1]);
	hSpec.SetBinError(i, std::sqrt(error_square[global_bin_start + i -1]));
    }

    return hSpec;

}


TH1D PROspec::toTH1D(const PROconfig& inconfig, const std::string& subchannel_fullname){
    int subchannel_index = inconfig.GetSubchannelIndex(subchannel_fullname);
    return this->toTH1D(inconfig, subchannel_index);
}
