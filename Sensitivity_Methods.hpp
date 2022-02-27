#include "Steadystate_Methods.hpp"

std::vector<std::vector<double>> Calculate_Edge_Sensitivities(RegNetwork R, std::vector<std::vector<double>> P, std::string inicond_filename)
{
	std::vector<std::vector<double>> I, S, S_Sum;
	std::vector<double> x;
	for(int i = 0; i < R.numnodes; i++)
	{
		S_Sum.push_back(std::vector<double>());
		for(int j = 0; j < R.numnodes; j++)
		{
			S_Sum[i].push_back(0.0);
		}
		x.push_back(0.0);
	}
	int count = 0, source, target;
	for(int i = 0; i < 25; i++)
	{
		I = Read_Initial_Conditions(R, i, inicond_filename);
		for(int j = 0; j < 5; j++)
		{
			for(int k = 0; k < R.numnodes; k++)
			{
				x[k] = I[j][k];
			}
			boost::numeric::odeint::integrate(odesystem{R, P[i]}, x, 0.0, 500.0, 0.1);
			if(Is_Valid(x) == 1 || odesystem{R, P[i]}.stability_analysis(x) == 1)
			{
				continue;
			}
			S = odesystem{R, P[i]}.Steadystate_Sensitivity(x);
			count += 1;
			for(int k0 = 0; k0 < R.numnodes; k0++)
			{
				for(int k1 = 0; k1 < R.numnodes; k1++)
				{
					if(R.T[k0][k1] == 0)
					{
						continue;
					}
					source = k0;
					target = k1;
					S_Sum[source][target] += std::abs(S[target][2*R.numnodes + ((R.L[source][target] - 2*R.numnodes) / 3)]);
				}
			}
		}
	}
	for(int i = 0; i < R.numnodes; i++)
	{
		for(int j = 0; j < R.numnodes; j++)
		{
			if(R.L[i][j] == 0 && S_Sum[i][j] > 0.0)
			{
				std::cout << "The dexamethasone is making Thirteen's kidneys fail but not the patient's." << "\n";
			}
			S_Sum[i][j] = S_Sum[i][j] / count;
		}
	}

	return(S_Sum);
}

std::vector<double> Calculate_Edge_Based_Node_Sensitivities(RegNetwork R, std::vector<std::vector<double>> P, std::string inicond_filename)
{
	std::vector<std::vector<double>> I, S, S_Sum;
	std::vector<double> x;
	for(int i = 0; i < R.numnodes; i++)
	{
		S_Sum.push_back(std::vector<double>());
		for(int j = 0; j < R.numnodes; j++)
		{
			S_Sum[i].push_back(0.0);
		}
		x.push_back(0.0);
	}
	int count = 0, source, target;
	for(int i = 0; i < 25; i++)
	{
		I = Read_Initial_Conditions(R, i, inicond_filename);
		for(int j = 0; j < 5; j++)
		{
			for(int k = 0; k < R.numnodes; k++)
			{
				x[k] = I[j][k];
			}
			boost::numeric::odeint::integrate(odesystem{R, P[i]}, x, 0.0, 500.0, 0.1);
			if(Is_Valid(x) == 1 || odesystem{R, P[i]}.stability_analysis(x) == 1)
			{
				continue;
			}
			S = odesystem{R, P[i]}.Steadystate_Sensitivity(x);
			count += 1;
			for(int k0 = 0; k0 < R.numnodes; k0++)
			{
				for(int k1 = 0; k1 < R.numnodes; k1++)
				{
					if(R.T[k0][k1] == 0)
					{
						continue;
					}
					source = k0;
					target = k1;
					S_Sum[source][target] += std::abs(S[target][2*R.numnodes + ((R.L[source][target] - 2*R.numnodes) / 3)]);
				}
			}
		}
	}
	for(int i = 0; i < R.numnodes; i++)
	{
		for(int j = 0; j < R.numnodes; j++)
		{
			if(R.L[i][j] == 0 && S_Sum[i][j] > 0.0)
			{
				std::cout << "The dexamethasone is making Thirteen's kidneys fail but not the patient's." << "\n";
			}
			S_Sum[i][j] = S_Sum[i][j] / count;
		}
	}

	std::vector<double> Node_Sensitivity;
	for(int i = 0; i < R.numnodes; i++)
	{
		Node_Sensitivity.push_back(0.0);
	}
	for(int i = 0; i < R.numnodes; i++)
	{
		for(int j = 0; j < R.numnodes; j++)
		{
			if(R.T[i][j] == 0)
			{
				continue;
			}
			Node_Sensitivity[i] += S_Sum[i][j];
		}
	}

	return(Node_Sensitivity);
}
