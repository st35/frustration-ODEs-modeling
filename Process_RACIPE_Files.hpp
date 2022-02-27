void splitstring(std::string line, std::string delim, std::vector<std::string> *l, int popflag)
{
	if(popflag == 1)
	{
        	line.pop_back();
	}

        int toklen, pos1 = 0, pos2;
        while(1)
        {
                pos2 = line.find(delim, pos1);
                if(pos2 == std::string::npos)
                {
                        break;
                }
                toklen = pos2 - pos1;
                (*l).push_back(line.substr(pos1, toklen));
                pos1 = pos2 + 1;
        }
        (*l).push_back(line.substr(pos1, std::string::npos));
}

RegNetwork ReadTopologyFile(std::string filename1, std::string filename2, std::string filename3)
{
	RegNetwork R;
	R.numnodes = 0;
	R.numedges = 0;
	R.nodeIDs = std::vector<std::string>();
	R.T = std::vector<std::vector<int>>();
	R.L = std::vector<std::vector<int>>();

	std::string nodeName;
	int nodeID, maxnodeID = -1, numlines;

	std::ifstream f(filename1);
	if(!static_cast<bool>(f))
	{
		std::cout << "Error reading the .ids file." << "\n";
		return(R);
	}
	while(f >> nodeName >> nodeID)
	{
		R.nodeIDs.push_back(nodeName);
		if(nodeID > maxnodeID)
		{
			maxnodeID = nodeID;
		}
		R.numnodes += 1;
	}
	f.close();
	if(R.numnodes != maxnodeID + 1)
	{
		std::cout << "Province of Alberta. Fortis et Liber." << "\n";
		return(R);
	}

	for(int i = 0; i < R.numnodes; i++)
	{
		R.T.push_back(std::vector<int>());
		R.L.push_back(std::vector<int>());
		for(int j = 0; j < R.numnodes; j++)
		{
			R.T[i].push_back(0);
			R.L[i].push_back(0);
		}
	}

	f.open(filename1);
	numlines = 0;
	while(getline(f, nodeName))
	{
		numlines += 1;
	}
	f.close();

	if(numlines != R.nodeIDs.size())
	{
		std::cout << "The format of the .ids file is ridonc, and frankly, completely wrong." << "\n";
		return(R);
	}

	f.open(filename2);
	if(!static_cast<bool>(f))
	{
		std::cout << "The T matrix file is missing." << "\n";
		return(R);
	}
	std::string line;
	std::vector<std::string> l;
	int index = 0;
	while(getline(f, line))
	{
		l.clear();
		splitstring(line, "\t", &l, 0);
		if(l.size() != R.numnodes)
		{
			std::cout << "We killed Yamamoto." << "\n";
			return(R);
		}
		for(int i = 0; i < l.size(); i++)
		{
			R.T[index][i] = std::stoi(l[i]);
			if(R.T[index][i] > 0)
			{
				R.numedges += 1;
			}
		}
		index += 1;
	}
	f.close();
	if(index != R.numnodes)
	{
		std::cout << "Par was 5." << "\n";
		return(R);
	}
		
        f.open(filename3);
        if(!static_cast<bool>(f))
        {
                std::cout << "The L matrix file is missing." << "\n";
                return(R);
        }
	index = 0;
	while(getline(f, line))
	{
		l.clear();
		splitstring(line, "\t", &l, 0);
		if(l.size() != R.numnodes)
		{
			std::cout << "This is the steam pipe trunk distribution venue." << "\n";
			return(R);
		}
		for(int i = 0; i < l.size(); i++)
		{
			R.L[index][i] = std::stoi(l[i]);
			if(R.L[index][i] > 0 && R.L[index][i] < 2*R.numnodes)
			{
				std::cout << "The fault, dear Brutus, is not in our stars but in ourselves..." << "\n";
				return(R);
			}
		}
		index += 1;
	}
	f.close();
	if(index != R.numnodes)
	{
		std::cout << "It was mini golf, wasn't it?" << "\n";
		return(R);
	}

	int flag = 0;
	for(int i = 0; i < R.numnodes; i++)
	{
		for(int j = 0; j < R.numnodes; j++)
		{
			if(R.T[i][j] == 0 && R.L[i][j] > 0)
			{
				flag = 1;
			}
			if(R.T[i][j] > 0 && R.L[i][j] == 0)
			{
				flag = 1;
			}
		}
	}
	if(flag == 1)
	{
		std::cout << "It's gonna be Ritchie." << "\n";
		return(R);
	}

	if(R.numnodes == R.nodeIDs.size() && R.T.size() == R.numnodes && R.L.size() == R.numnodes)
	{
		R.isvalid = true;
	}

	return(R);
}

void Write_Network(RegNetwork R, std::ofstream *f)
{
	(*f) << "Source\tTarget\tType\n";
	for(int i = 0; i < R.T.size(); i++)
	{
		for(int j = 0; j < R.T.size(); j++)
		{
			if(R.T[i][j] > 0)
			{
				(*f) << R.nodeIDs[i] << "\t" << R.nodeIDs[j] << "\t" << R.T[i][j] << "\n";
			}
		}
	}

	return;
}

void Print_Network(RegNetwork R)
{
	std::cout << "Source\tTarget\tType\n";
	for(int i = 0; i < R.T.size(); i++)
	{
		for(int j = 0; j < R.T.size(); j++)
		{
			if(R.T[i][j] > 0)
			{
				std::cout << R.nodeIDs[i] << "\t" << R.nodeIDs[j] << "\t" << R.T[i][j] << "\n";
			}
		}
	}

	return;
}

std::vector<std::vector<double>> Read_Parameters(RegNetwork R, std::vector<int> &numstablestates, std::string filename)
{
	numstablestates.clear();
	std::vector<std::vector<double>> P;

	std::ifstream f(filename);
        if(!static_cast<bool>(f))
        {
                std::cout << "The parameters file has probably been dumped into the Eagleton reservoir." << "\n";
                return(P);
        }

	std::string line;
	std::vector<std::string> l;

	int count = 0;

	while(getline(f, line))
	{
		l.clear();
		splitstring(line, "\t", &l, 0);
		if(l.size() != 2*R.numnodes + 3*R.numedges + 2)
		{
			std::cout << "The parameters file is utter malarkey." << "\n";
			for(int i = 0; i < P.size(); i++)
			{
				P[i].clear();
			}
			P.clear();
			return(P);
		}
		numstablestates.push_back(std::stoi(l[1]));
		P.push_back(std::vector<double>());
		for(int i = 2; i < l.size(); i++)
		{
			P[count].push_back(std::stod(l[i]));
		}
		if(P[count].size() != (2*R.numnodes + 3*R.numedges))
		{
			std::cout << "This little restaurant will put McDonald's out of business..." << "\n";
		}
		count += 1;
	}
	f.close();

	return(P);
}

std::vector<std::vector<double>> Read_Initial_Conditions(RegNetwork R, int index, std::string filename)
{
	std::vector<std::vector<double>> I;

	std::ifstream f(filename);
        if(!static_cast<bool>(f))
        {
                std::cout << "Couldn't find the initial conditions file. Probably some Eagletonian prick took it." << "\n";
                return(I);
        }

        std::string line;
        std::vector<std::string> l;

        int count = 0, numcond = 0, point = 0;

        while(getline(f, line))
        {
		if(count != index)
		{
			count += 1;
			continue;
		}

                l.clear();
                splitstring(line, " ", &l, 1);
                if(l.size() % R.numnodes != 0)
                {
                        std::cout << "This initial conditions file was put together in Eagleton." << "\n";
                        for(int i = 0; i < I.size(); i++)
                        {
                                I[i].clear();
                        }
                        I.clear();
                        return(I);
                }
		point = 0;
		while(point < l.size())
		{
			I.push_back(std::vector<double>());
			for(int i = 0; i < R.numnodes; i++)
			{
				I[numcond].push_back(std::stod(l[point]));
				point += 1;
			}
			numcond += 1;
		}
		count += 1;
		break;
        }
	f.close();

        return(I);
}

std::vector<std::vector<double>> Read_Initial_Conditions_Alt(RegNetwork R, std::string filename)
{
	std::vector<std::vector<double>> I;

	std::ifstream f(filename);
        if(!static_cast<bool>(f))
        {
                std::cout << "Couldn't find the initial conditions file. Probably some Eagletonian prick took it." << "\n";
                return(I);
        }

        std::string line;
        std::vector<std::string> l;

        int numcond = 0, point = 0, newcond = 0, linecount = 0;

        while(getline(f, line))
        {
                l.clear();
                splitstring(line, " ", &l, 1);
                if(l.size() % R.numnodes != 0)
                {
                        std::cout << "This initial conditions file was put together in Eagleton." << "\n";
                        for(int i = 0; i < I.size(); i++)
                        {
                                I[i].clear();
                        }
                        I.clear();
                        return(I);
                }
		point = 0;
		newcond = 0;
		while(point < l.size())
		{
			I.push_back(std::vector<double>());
			for(int i = 0; i < R.numnodes; i++)
			{
				I[numcond].push_back(std::stod(l[point]));
				point += 1;
			}
			numcond += 1;
			newcond += 1;
		}
		linecount += 1;
        }
	f.close();

        return(I);
}
