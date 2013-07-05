#include <stdio.h>
#include <rpc/rpc.h>
#define SIZE 2
#define THEFILE "./readss.py"


void catfile(char *filename[]);


main(int argc, char *argv[]){

	FILE* f;
	double *array[SIZE]; /* an array of pointers to doubles*/
	double xarr[100], yarr[100]; /* two arrays of numbers*/
	int i, j; /*two integers*/
	int *jptr; /*a pointer to an integer*/
	char str[80];
	
	for(i=0;i<100;i++){
		xarr[i] = (double)i;
	}
	for(i=0;i<100;i++){
		yarr[i] = (double)100-(double)i;
	}
	j = 9;
	jptr = &j;
	
	printf("%i, %i\n", j, *jptr);
	j=8;
	printf("%i, %i\n", j, *jptr);
	printf("Hello world\n");
	
	printf("%s, %i, %lf, %lf\n", argv[1], argc, xarr[1], yarr[1]);
	
	array[0] = xarr;
	array[1] = yarr;
	
	for(i=0;i<20;i++){
		str[i] = THEFILE[i];
	}
	printf("%s\n", str);
	
	printf("%lf, %lf\n", array[0][1], array[1][1]);

	f = fopen(THEFILE, "r");
	for(i=0;i<1;i++){
		fgets(str, 80, f);
		printf("%s", str);
	}
	fclose(f);
	
	/*catfile(THEFILE);*/

}


void catfile(char *filename[]){
	FILE* fptr;
	char ch;
	
	printf("Printing this file to screen: %s\n", filename);
	
	fptr = fopen(filename, "r");
	for(ch=getc(fptr);ch!=EOF & ch!=NULL;ch=getc(fptr)){
		printf("%c", ch);
	}
	fclose(fptr);
	return(0);
}