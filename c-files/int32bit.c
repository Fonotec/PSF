#include <sys/socket.h>
#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <sys/time.h>
#include <sys/types.h>
#include <netdb.h>
#include <string.h>
#include <strings.h>
#include <netinet/in.h>
#include <unistd.h>
#include <math.h>
#include <time.h>
#include <sys/time.h>

#define MTU 8900
unsigned char * packet_buf;
unsigned char out_buffer[20];
double power[512];
int fd;

int main(int argc, char ** argv)
{
    int i;
    unsigned int f_power;
    struct sockaddr_in server_addr, client_addr;
    struct hostent *hp;
    int packet_counter, max_packet_counter, client_len=sizeof(client_addr);
    unsigned long int stamps[1000000];
    struct timeval start, end;
    double sum_power;
    struct timeval stamp;
    double freq;

    if (argc == 2)
    {
	    sscanf(argv[1], "%lf", &freq);
    }
    if (freq < 20 || freq > 5700)
    {
	    fprintf(stderr,"Frequency out of range\n");
	    exit(10);
    }
    if ((fd = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)) < 0) {
	    fprintf(stderr, "no socket\n");
	    exit(10);
    }
    /*    if(!(hp = gethostbyname("192.42.120.250"))) {
	  fprintf(stderr, "gethostbyname failed\n");
	  exit(10); } */
    bzero(&server_addr, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(22102);
    /* bcopy(hp->h_addr, &server_addr.sin_addr, hp->h_length); */
    server_addr.sin_addr.s_addr=htonl(INADDR_ANY);
    if(bind(fd, (struct sockaddr *)&server_addr, sizeof(server_addr)) <0) {
	    fprintf(stderr, "bind failed\n");
	    exit(10); 
    }
    if((packet_buf = malloc(MTU)) == NULL) {
	    fprintf(stderr, "malloc failed\n");
	    exit(10);
    }

    printf("set terminal x11 noraise persist; set nomouse; set grid; set grid mytics; set title \"70MHz dual 10bit AD9216\"; set xlabel \"Freq (MHz)\"; set yrange [5:70]; set ytics 10; set ylabel \"Power\"\n"); 
    while (1) {
	    if(recvfrom(fd, packet_buf, MTU, 0, 
				    (struct sockaddr *)&client_addr, &client_len)<0) {
		    fprintf(stderr, "first recvfrom() failed\n");
		    exit(10);
	    }
	    printf ("plot \"-\" u 1:(10*log10($2)) with l lw 2\n");  
	    for(i = 256; i < 512; i++) { 
/*		for(i=0; i < 255; i++) { */
		    f_power = ntohl(((unsigned long *)packet_buf)[i+1]);
	    power[i] = 0.02 * (double)f_power + 0.98 * power[i];
	    printf("%f\t%f\n", (i)*70./512+freq+21.4-70.0,power[i]); 
	    /* printf("%d\t%f\n", i,power[i]); */
    }
    printf("e\n");
    sum_power = 0;
    for (i = 351; i < 361; i++) {
	    sum_power += power[i];
    }
    gettimeofday(&stamp,NULL);

    fprintf(stderr,"%f\t%f\n",(double)stamp.tv_sec+(double)stamp.tv_usec/1000000,10*log(sum_power/10.)/log(10.0));
    fflush(stdout);
}
}

