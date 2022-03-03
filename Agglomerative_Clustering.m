function Agglomerative_Clustering(inputnetworkid, updateindex)
	D = importdata(['steadystates/RUN_' num2str(inputnetworkid) '/network_' num2str(updateindex) '.log']);
	D = D(:, 2:end);
	for i = 1:size(D, 2)
		D(:, i) = (D(:, i) - mean(D(:, i))) / std(D(:, i));
	end
	Y = pdist(D', 'correlation');
	Z = linkage(Y, 'average');
	f = fopen(['linkages/RUN_' num2str(inputnetworkid) '/linkage_' num2str(updateindex) '.log'], 'w');
	for i = 1:size(Z, 1)
		fprintf(f, '%d\t%d\n', Z(i, 1), Z(i, 2));
	end
	fclose(f);
end
