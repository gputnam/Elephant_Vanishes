#ifndef PROPELLER_H_
#define PROPELLER_H_

// STANDARD
#include <vector>
#include <string>
#include <algorithm>
#include <cmath>

namespace PROfit{

    class PROpeller {

	private:
            int nevents;

        public:

            //Constructors
            PROpeller(){
		nevents = -1;
		truth.clear();
		reco.clear();
		baseline.clear();
		pdg.clear();
		added_weights.clear();
		bin_indices.clear();
	               }

            PROpeller(std::vector<float> intruth, std::vector<float> inreco, std::vector<float> inbaseline, std::vector<int> inpdg, std::vector<float> inadded_weights, std::vector<int> inbin_indices) : nevents(truth.size()), truth(intruth), reco(inreco), baseline(inbaseline), pdg(inpdg), added_weights(inadded_weights), bin_indices(inbin_indices){}

           std::vector<float> truth;
           std::vector<float> reco;
           std::vector<float> baseline;
           std::vector<int>   pdg;
           std::vector<float> added_weights;
           std::vector<int>   bin_indices;

    };

}
#endif
