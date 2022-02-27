int Is_Valid(const std::vector<double> x)
{
	int flag = 0;
	for(int i = 0; i < x.size(); i++)
	{
		if(std::abs(x[i]) < 1e-16)
		{
			flag = 1;
		}
		if(x[i] < 0.0)
		{
			flag = 1;
		}
		if(std::isnan(x[i]))
		{
			flag = 1;
		}
	}

	return(flag);
}

void Find_Steadystates(RegNetwork R, std::vector<std::vector<double>> P, std::string inicond_filename, std::vector<int> &numstablestates, std::ofstream *f, std::ofstream *g)
{
	std::vector<std::vector<double>> I;
	std::vector<double> x;
	for(int i = 0; i < R.numnodes; i++)
	{
		x.push_back(0.0);
	}
	I = Read_Initial_Conditions_Alt(R, inicond_filename);

	int source, target, statecount = 0;
	for(int i = 0; i < P.size(); i++)
	{
		for(int j = 0; j < I.size(); j++)
		{
			for(int k = 0; k < R.numnodes; k++)
			{
				x[k] = I[j][k];
			}
			boost::numeric::odeint::integrate(odesystem{R, P[i]}, x, 0.0, 500.0, 0.1);
			if(Is_Valid(x) == 1)
			{
				continue;
			}

			(*f) << i << " " << numstablestates[i] << " ";
			for(int k = 0; k < R.numnodes; k++)
			{
				(*f) << x[k] << " ";
			}
			(*f) << "\n";

			(*g) << i << " " << numstablestates[i] << " ";
			for(int k = 0; k < R.numnodes; k++)
			{
				(*g) << I[j][k] << " ";
			}
			(*g) << "\n";
		}
	}
}
