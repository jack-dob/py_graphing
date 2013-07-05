#include <stdio.h>
#include "sshead.h"
#include "orb_params.h"
#include <math.h>

void bin_ecc(SSHEAD sshead, SSDATA *ssdata, int *ecc_bins, int nbins);
void print_bins_i(int nbins, double start, double stop, int *bin_array);

int main(int argc, char **argv){
	int i, nbins;
	int *ecc_bins;
	SSHEAD *sshead;
	char *infile;
	
	//assume that each argument is a file to read header of
	printf("%d", argc);
	exit(0);
	if(argc < 1){
		puts("Error: No input files passed, exiting...");
		exit(0);
	}
	
	sshead = (SSHEAD*) malloc((int)argc*sizeof(SSHEAD));
	puts("Allocated sshead memory...")
	
	
	for(i=1;i<argc;i++){
	infile = argv[1]; //1st argument is the input file
	
	readin_sshead(infile, &sshead); //read in header
	}
	


	free(ecc_bins);
	free(ssdata);
}








