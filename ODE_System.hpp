double Shifted_Hill(double c, double c0, double n, double lambda)
{
	return(lambda + (1.0 - lambda)*(1.0 / (1.0 + pow((c / c0), n))));
}

double dShifted_Hilldx(double c, double c0, double n, double lambda, int interaction_type)
{
	double j0 = std::pow(1.0 + std::pow((c / c0), n), 2.0);
	j0 = 1.0 / j0;
	double j1 = (n / c0)*std::pow((c / c0), n - 1.0);

	if(interaction_type == 1)
	{
		return((-(1.0 - lambda)*j0*j1) / lambda);
	}
	else if(interaction_type == 2)
	{
		return(-(1.0 - lambda)*j0*j1);
	}
	else
	{
		std::cout << "Acyclovir + Ribovirin." << "\n";
	}

	return(0.0);
}

double dShifted_Hilldlambda(double c, double c0, double n, double lambda, int interaction_type)
{
	double j0 = (1.0 / (1.0 + pow((c / c0), n)));
	if(interaction_type == 1)
	{
		return(-j0 / (lambda*lambda));
	}
	else if(interaction_type == 2)
	{
		return(1.0 - j0);
	}
	else
	{
		std::cout << "Trooper Reese." << "\n";
	}

	return(0.0);
}

void Jacobian(RegNetwork &R, std::vector<double> &P, const std::vector<double> &x, std::vector<double> &H, std::vector<std::vector<double>> &J)
{
	int source, target, paramindex;
	for(int i = 0; i < R.numnodes; i++)
	{
		for(int j = 0; j < R.numnodes; j++)
		{
			J[i][j] = H[i];
		}
	}
	for(int i = 0; i < R.numnodes; i++)
	{
		for(int j = 0; j < R.numnodes; j++)
		{
			if(R.T[j][i] == 0)
			{
				J[i][j] = 0.0;
			}
			else
			{
				source = j;
				target = i;
				paramindex = R.L[source][target];
				if(R.T[source][target] == 1)
				{
					J[i][j] = J[i][j] / (Shifted_Hill(x[source], P[paramindex], P[paramindex + 1], P[paramindex + 2]) / P[paramindex + 2]);
					J[i][j] = J[i][j]*dShifted_Hilldx(x[source], P[paramindex], P[paramindex + 1], P[paramindex + 2], 1);
				}
				else if(R.T[source][target] == 2)
				{
					J[i][j] = J[i][j] / Shifted_Hill(x[source], P[paramindex], P[paramindex + 1], P[paramindex + 2]);
					J[i][j] = J[i][j]*dShifted_Hilldx(x[source], P[paramindex], P[paramindex + 1], P[paramindex + 2], 2);
				}
			}
		}
		J[i][i] -= P[i + R.numnodes];
	}

	return;
}

void Calculate_dfdP(RegNetwork &R, std::vector<double> &P, const std::vector<double> &x, std::vector<double> &H, std::vector<std::vector<double>> &dfdP)
{
	int source, target, paramindex, lambdaindex;
	for(int i = 0; i < R.numnodes; i++)
	{
		dfdP[i][i] = (P[i])*(H[i] / P[i]);
		dfdP[i][i + R.numnodes] = (P[i + R.numnodes])*(-x[i]);
	}
	for(int i = 0; i < R.numnodes; i++)
	{
		for(int j = 0; j < R.numnodes; j++)
		{
			if(R.T[i][j] == 0)
			{
				continue;
			}
			source = i;
			target = j;
			paramindex = R.L[i][j];
			lambdaindex = 2*R.numnodes + ((R.L[i][j] - 2*R.numnodes) / 3);
			if(R.T[i][j] == 1)
			{
				dfdP[target][lambdaindex] = H[target] / (Shifted_Hill(x[source], P[paramindex], P[paramindex + 1], P[paramindex + 2]) / P[paramindex + 2]);
				dfdP[target][lambdaindex] = P[paramindex + 2]*dfdP[target][lambdaindex]*dShifted_Hilldlambda(x[source], P[paramindex], P[paramindex + 1], P[paramindex + 2], 1);
			}
			else if(R.T[i][j] == 2)
			{
				dfdP[target][lambdaindex] = H[target] / (Shifted_Hill(x[source], P[paramindex], P[paramindex + 1], P[paramindex + 2]));
				dfdP[target][lambdaindex] = P[paramindex + 2]*dfdP[target][lambdaindex]*dShifted_Hilldlambda(x[source], P[paramindex], P[paramindex + 1], P[paramindex + 2], 2);
			}
		}
	}
}

struct odesystem
{
	RegNetwork R;
	std::vector<double> P;
	odesystem(RegNetwork param1, std::vector<double> param2)
	{
		if(!param1.isvalid)
		{
			std::cout << "One is the loneliest number..." << "\n";
		}
		R.numnodes = param1.numnodes;
		R.numedges = param1.numedges;
		R.nodeIDs = std::vector<std::string>();
		for(int i = 0; i < R.numnodes; i++)
		{
			R.nodeIDs.push_back(param1.nodeIDs[i]);
		}
		R.T = std::vector<std::vector<int>>();
		for(int i = 0; i < R.numnodes; i++)
		{
			R.T.push_back(std::vector<int>());
			for(int j = 0; j < R.numnodes; j++)
			{
				R.T[i].push_back(param1.T[i][j]);
			}
		}
		R.L = std::vector<std::vector<int>>();
		for(int i = 0; i < R.numnodes; i++)
		{
			R.L.push_back(std::vector<int>());
			for(int j = 0; j < R.numnodes; j++)
			{
				R.L[i].push_back(param1.L[i][j]);
			}
		}
		R.isvalid = true;
		for(int i = 0; i < param2.size(); i++)
		{
			P.push_back(param2[i]);
		}
	}
	void operator()(const std::vector<double> &x, std::vector<double> &dxdt, double t)
	{
		int source, target, paramindex, index, flag;
		std::vector<double> H;
		for(int i = 0; i < R.numnodes; i++)
		{
			dxdt[i] = P[i];
			for(int j = 0; j < R.numnodes; j++)
			{
				if(R.T[j][i] == 0)
				{
					continue;
				}
				else
				{
					source = j;
					target = i;
					paramindex = R.L[j][i];
					if(R.T[j][i] == 1)
					{
						dxdt[target] = dxdt[target]*Shifted_Hill(x[source], P[paramindex], P[paramindex + 1], P[paramindex + 2]) / P[paramindex + 2];
					}
					else if(R.T[j][i] == 2)
					{
						dxdt[target] = dxdt[target]*Shifted_Hill(x[source], P[paramindex], P[paramindex + 1], P[paramindex + 2]);
					}
				}
			}
			H.push_back(dxdt[i]);
			dxdt[i] = dxdt[i] - P[i + R.numnodes]*x[i];
		}
	}

	int stability_analysis(const std::vector<double> &x)
	{
		int source, target, paramindex, index, flag;
		std::vector<double> dxdt, H;
		std::vector<std::vector<double>> J;
		for(int i = 0; i < R.numnodes; i++)
		{
			dxdt.push_back(0.0);
			J.push_back(std::vector<double>());
			for(int j = 0; j < R.numnodes; j++)
			{
				J[i].push_back(0.0);
			}
		}
		for(int i = 0; i < R.numnodes; i++)
		{
			dxdt[i] = P[i];
			for(int j = 0; j < R.numnodes; j++)
			{
				if(R.T[j][i] == 0)
				{
					continue;
				}
				else
				{
					source = j;
					target = i;
					paramindex = R.L[j][i];
					if(R.T[j][i] == 1)
					{
						dxdt[target] = dxdt[target]*Shifted_Hill(x[source], P[paramindex], P[paramindex + 1], P[paramindex + 2]) / P[paramindex + 2];
					}
					else if(R.T[j][i] == 2)
					{
						dxdt[target] = dxdt[target]*Shifted_Hill(x[source], P[paramindex], P[paramindex + 1], P[paramindex + 2]);
					}
				}
			}
			H.push_back(dxdt[i]);
			dxdt[i] = dxdt[i] - P[i + R.numnodes]*x[i];
		}
		Jacobian(R, P, x, H, J);
		gsl_matrix *gJ = gsl_matrix_alloc(R.numnodes, R.numnodes);
		gsl_matrix *gJ0 = gsl_matrix_alloc(R.numnodes, R.numnodes);
		for(int i = 0; i < R.numnodes; i++)
		{
			for(int j = 0; j < R.numnodes; j++)
			{
				gsl_matrix_set(gJ, i, j, J[i][j]);
				gsl_matrix_set(gJ0, i, j, J[i][j]);
			}
		}
		gsl_permutation *p = gsl_permutation_alloc(R.numnodes);
		int s;
		gsl_linalg_LU_decomp(gJ, p, &s);

		double det = gsl_linalg_LU_det(gJ, s);

		gsl_eigen_nonsymmv_workspace *w = gsl_eigen_nonsymmv_alloc(R.numnodes);
		gsl_vector_complex *eigen = gsl_vector_complex_alloc(R.numnodes);
		gsl_matrix_complex *evec = gsl_matrix_complex_alloc(R.numnodes, R.numnodes);
		gsl_eigen_nonsymmv(gJ0, eigen, evec, w);

		int sflag = 0;
		for(int i = 0; i < R.numnodes; i++)
		{
			if(GSL_REAL(gsl_vector_complex_get(eigen, i)) > 0 || std::abs(GSL_REAL(gsl_vector_complex_get(eigen, i))) < 1e-16)
			{
				sflag = 1;
			}
		}
		if(std::abs(det) < 1e-16)
		{
			sflag = 1;
		}

		gsl_matrix_free(gJ);
		gsl_matrix_free(gJ0);
		gsl_permutation_free(p);
		gsl_eigen_nonsymmv_free(w);
		gsl_vector_complex_free(eigen);
		gsl_matrix_complex_free(evec);

		return(sflag);
	}

	std::vector<std::vector<double>> Steadystate_Sensitivity(const std::vector<double> &x)
	{
		int source, target, paramindex, index, flag;
		std::vector<double> dxdt, H;
		std::vector<std::vector<double>> J, dfdP;
		for(int i = 0; i < R.numnodes; i++)
		{
			dxdt.push_back(0.0);
			J.push_back(std::vector<double>());
			dfdP.push_back(std::vector<double>());
			for(int j = 0; j < R.numnodes; j++)
			{
				J[i].push_back(0.0);
			}
			for(int j = 0; j < 2*R.numnodes + R.numedges; j++)
			{
				dfdP[i].push_back(0.0);
			}
		}
		for(int i = 0; i < R.numnodes; i++)
		{
			dxdt[i] = P[i];
			for(int j = 0; j < R.numnodes; j++)
			{
				if(R.T[j][i] == 0)
				{
					continue;
				}
				else
				{
					source = j;
					target = i;
					paramindex = R.L[j][i];
					if(R.T[j][i] == 1)
					{
						dxdt[target] = dxdt[target]*Shifted_Hill(x[source], P[paramindex], P[paramindex + 1], P[paramindex + 2]) / P[paramindex + 2];
					}
					else if(R.T[j][i] == 2)
					{
						dxdt[target] = dxdt[target]*Shifted_Hill(x[source], P[paramindex], P[paramindex + 1], P[paramindex + 2]);
					}
				}
			}
			H.push_back(dxdt[i]);
			dxdt[i] = dxdt[i] - P[i + R.numnodes]*x[i];
		}
		Jacobian(R, P, x, H, J);
		gsl_matrix *gJ = gsl_matrix_alloc(R.numnodes, R.numnodes);
		for(int i = 0; i < R.numnodes; i++)
		{
			for(int j = 0; j < R.numnodes; j++)
			{
				gsl_matrix_set(gJ, i, j, J[i][j]);
			}
		}
		gsl_matrix *YI = gsl_matrix_alloc(R.numnodes, R.numnodes);
		gsl_matrix_set_zero(YI);
		for(int i = 0; i < R.numnodes; i++)
		{
			gsl_matrix_set(YI, i, i, 1.0 / x[i]);
		}
		gsl_permutation *p = gsl_permutation_alloc(R.numnodes);
		int s;
		gsl_linalg_LU_decomp(gJ, p, &s);
		gsl_matrix *gJI = gsl_matrix_alloc(R.numnodes, R.numnodes);
		gsl_linalg_LU_invert(gJ, p, gJI);

		gsl_matrix *L = gsl_matrix_alloc(R.numnodes, R.numnodes);

		gsl_blas_dgemm(CblasNoTrans, CblasNoTrans, 1.0, YI, gJI, 0.0, L);

		Calculate_dfdP(R, P, x, H, dfdP);
		gsl_matrix *gdfdP = gsl_matrix_alloc(R.numnodes, 2*R.numnodes + R.numedges);
		for(int i = 0; i < R.numnodes; i++)
		{
			for(int j = 0; j < 2*R.numnodes + R.numedges; j++)
			{
				gsl_matrix_set(gdfdP, i, j, dfdP[i][j]);
			}
		}
		gsl_matrix *S = gsl_matrix_alloc(R.numnodes, 2*R.numnodes + R.numedges);
		gsl_blas_dgemm(CblasNoTrans, CblasNoTrans, -1.0, L, gdfdP, 0.0, S);

		std::vector<std::vector<double>> sensitivity;
		for(int i = 0; i < R.numnodes; i++)
		{
			sensitivity.push_back(std::vector<double>());
			for(int j = 0; j < 2*R.numnodes + R.numedges; j++)
			{
				sensitivity[i].push_back(gsl_matrix_get(S, i, j));
			}
		}
//		gsl_matrix *Hessian = gsl_matrix_alloc(2*R.numnodes + R.numedges, 2*R.numnodes + R.numedges);
//		gsl_blas_dgemm(CblasTrans, CblasNoTrans, 2.0, S, S, 0.0, Hessian);
//		gsl_eigen_nonsymmv_workspace *w = gsl_eigen_nonsymmv_alloc(2*R.numnodes + R.numedges);
//		gsl_vector_complex *eigen = gsl_vector_complex_alloc(2*R.numnodes + R.numedges);
//		gsl_matrix_complex *evec = gsl_matrix_complex_alloc(2*R.numnodes + R.numedges, 2*R.numnodes + R.numedges);
//		gsl_eigen_nonsymmv(Hessian, eigen, evec, w);
//		std::vector<double> eigH;
//		for(int i = 0; i < 2*R.numnodes + R.numedges; i++)
//		{
//			eigH.push_back(GSL_REAL(gsl_vector_complex_get(eigen, i)));
//		}

		gsl_matrix_free(gJ);
		gsl_matrix_free(YI);
		gsl_matrix_free(gJI);
		gsl_permutation_free(p);
		gsl_matrix_free(L);
		gsl_matrix_free(gdfdP);
		gsl_matrix_free(S);
//		gsl_matrix_free(Hessian);
//              gsl_eigen_nonsymmv_free(w);
//              gsl_vector_complex_free(eigen);
//              gsl_matrix_complex_free(evec);

		return(sensitivity);
	}


	std::vector<double> Steadystate_Hessian_Eigenvalues(const std::vector<double> &x)
	{
		int source, target, paramindex, index, flag;
		std::vector<double> dxdt, H;
		std::vector<std::vector<double>> J, dfdP;
		for(int i = 0; i < R.numnodes; i++)
		{
			dxdt.push_back(0.0);
			J.push_back(std::vector<double>());
			dfdP.push_back(std::vector<double>());
			for(int j = 0; j < R.numnodes; j++)
			{
				J[i].push_back(0.0);
			}
			for(int j = 0; j < 2*R.numnodes + R.numedges; j++)
			{
				dfdP[i].push_back(0.0);
			}
		}
		for(int i = 0; i < R.numnodes; i++)
		{
			dxdt[i] = P[i];
			for(int j = 0; j < R.numnodes; j++)
			{
				if(R.T[j][i] == 0)
				{
					continue;
				}
				else
				{
					source = j;
					target = i;
					paramindex = R.L[j][i];
					if(R.T[j][i] == 1)
					{
						dxdt[target] = dxdt[target]*Shifted_Hill(x[source], P[paramindex], P[paramindex + 1], P[paramindex + 2]) / P[paramindex + 2];
					}
					else if(R.T[j][i] == 2)
					{
						dxdt[target] = dxdt[target]*Shifted_Hill(x[source], P[paramindex], P[paramindex + 1], P[paramindex + 2]);
					}
				}
			}
			H.push_back(dxdt[i]);
			dxdt[i] = dxdt[i] - P[i + R.numnodes]*x[i];
		}
		Jacobian(R, P, x, H, J);
		gsl_matrix *gJ = gsl_matrix_alloc(R.numnodes, R.numnodes);
		for(int i = 0; i < R.numnodes; i++)
		{
			for(int j = 0; j < R.numnodes; j++)
			{
				gsl_matrix_set(gJ, i, j, J[i][j]);
			}
		}
		gsl_matrix *YI = gsl_matrix_alloc(R.numnodes, R.numnodes);
		gsl_matrix_set_zero(YI);
		for(int i = 0; i < R.numnodes; i++)
		{
			gsl_matrix_set(YI, i, i, 1.0 / x[i]);
		}
		gsl_permutation *p = gsl_permutation_alloc(R.numnodes);
		int s;
		gsl_linalg_LU_decomp(gJ, p, &s);
		gsl_matrix *gJI = gsl_matrix_alloc(R.numnodes, R.numnodes);
		gsl_linalg_LU_invert(gJ, p, gJI);

		gsl_matrix *L = gsl_matrix_alloc(R.numnodes, R.numnodes);

		gsl_blas_dgemm(CblasNoTrans, CblasNoTrans, 1.0, YI, gJI, 0.0, L);

		Calculate_dfdP(R, P, x, H, dfdP);
		gsl_matrix *gdfdP = gsl_matrix_alloc(R.numnodes, 2*R.numnodes + R.numedges);
		for(int i = 0; i < R.numnodes; i++)
		{
			for(int j = 0; j < 2*R.numnodes + R.numedges; j++)
			{
				gsl_matrix_set(gdfdP, i, j, dfdP[i][j]);
			}
		}
		gsl_matrix *S = gsl_matrix_alloc(R.numnodes, 2*R.numnodes + R.numedges);
		gsl_blas_dgemm(CblasNoTrans, CblasNoTrans, -1.0, L, gdfdP, 0.0, S);
		gsl_matrix *Hessian = gsl_matrix_alloc(2*R.numnodes + R.numedges, 2*R.numnodes + R.numedges);
		gsl_blas_dgemm(CblasTrans, CblasNoTrans, 2.0, S, S, 0.0, Hessian);
		gsl_eigen_nonsymmv_workspace *w = gsl_eigen_nonsymmv_alloc(2*R.numnodes + R.numedges);
		gsl_vector_complex *eigen = gsl_vector_complex_alloc(2*R.numnodes + R.numedges);
		gsl_matrix_complex *evec = gsl_matrix_complex_alloc(2*R.numnodes + R.numedges, 2*R.numnodes + R.numedges);
		gsl_eigen_nonsymmv(Hessian, eigen, evec, w);
		std::vector<double> eigH;
		for(int i = 0; i < 2*R.numnodes + R.numedges; i++)
		{
			eigH.push_back(GSL_REAL(gsl_vector_complex_get(eigen, i)));
		}

		gsl_matrix_free(gJ);
		gsl_matrix_free(YI);
		gsl_matrix_free(gJI);
		gsl_permutation_free(p);
		gsl_matrix_free(L);
		gsl_matrix_free(gdfdP);
		gsl_matrix_free(S);
		gsl_matrix_free(Hessian);
                gsl_eigen_nonsymmv_free(w);
                gsl_vector_complex_free(eigen);
                gsl_matrix_complex_free(evec);

		return(eigH);
	}
};
