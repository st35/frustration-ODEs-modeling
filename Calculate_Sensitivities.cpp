#include <iostream>
#include <fstream>
#include <string>
#include <cmath>
#include <algorithm>
#include <boost/numeric/odeint.hpp>
#include <gsl/gsl_linalg.h>
#include <gsl/gsl_blas.h>
#include <gsl/gsl_eigen.h>
#include "Network_Type.hpp"
#include "Process_RACIPE_Files.hpp"
#include "ODE_System.hpp"
#include "Sensitivity_Methods.hpp"

void Run(std::string filename, int network_id, int updateindex, int world_rank, int sensitivityindex)
{
	RegNetwork R = ReadTopologyFile(filename + "_" + std::to_string(updateindex) + ".ids", filename + "_" + std::to_string(updateindex) + "_T_matrix.log", filename + "_" + std::to_string(updateindex) + "_L_matrix.log");
	if(!R.isvalid)
	{
		std::cout << "Network input failed. Your input files disrespected Tuco Salamanca." << "\n";
		return;
	}

	std::vector<int> numstablestates, numstates;
	std::vector<std::vector<double>> P = Read_Parameters(R, numstablestates, filename + "_" + std::to_string(updateindex) + "_parameters.dat");

	if(sensitivityindex == 0)
	{
		std::vector<std::vector<double>> S = Calculate_Edge_Sensitivities(R, P, filename + "_" + std::to_string(updateindex) + "_initial_conditions.log");

		std::ofstream f("sensitivities/RUN_" + std::to_string(network_id) + "/sensitivity_" + std::to_string(updateindex) + ".log");
		for(int i = 0; i < S.size(); i++)
		{
			for(int j = 0; j < S[i].size(); j++)
			{
				f << S[i][j] << " ";
			}
			f << "\n";
		}
		f.close();
	}
	else if(sensitivityindex == 1)
	{
		std::vector<double> S = Calculate_Edge_Based_Node_Sensitivities(R, P, filename + "_" + std::to_string(updateindex) + "_initial_conditions.log");

		std::ofstream f("sensitivities/RUN_" + std::to_string(network_id) + "/sensitivity_" + std::to_string(updateindex) + ".log");
		for(int i = 0; i < S.size(); i++)
		{
			f << S[i] << "\n";
		}
		f.close();
	}

	return;
}

int main(int argc, char *argv[])
{
	//MPI_Init(NULL, NULL);
        int world_size;
        //MPI_Comm_size(MPI_COMM_WORLD, &world_size);
        int world_rank = 0;
        //MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);

	std::string filename = argv[1];
	int network_id = std::stoi(argv[2]);
	int updateindex = std::stoi(argv[3]);
	int sensitivityindex = std::stoi(argv[4]);

	Run("RACIPE_Output/RUN_" + std::to_string(network_id) + "/RUN_" + std::to_string(updateindex) + "/" + filename, network_id, updateindex, world_rank, sensitivityindex);

	//MPI_Finalize();

	return(0);
}
