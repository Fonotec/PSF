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

#define MTU 8900
#define PPS 140000000/2/64/4096
unsigned char * packet_buf;
unsigned char out_buffer[20];
double power[2048];
int fd;

int main(int argc, char *argv[])
{
    int i,j = 0;
    unsigned int f_power;
    struct sockaddr_in server_addr, client_addr;
    struct hostent *hp;
    double freq,time;
    int packet_counter, max_packet_counter, client_len=sizeof(client_addr);
    double sum_power;
    struct timeval stamp;

    if (argc != 3)
    {
    	fprintf(stderr, "%s requires two arguments: frequency (MHz) and integration time (s)\n", argv[0]);
	exit(10);
    }

    sscanf(argv[1],"%lf",&freq);
    sscanf(argv[2],"%lf",&time);

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

/*    printf("set xrange [1415:1425]; set yrange [64:68]; set terminal x11 noraise persist; set grid; set grid mytics; set title \"65MHz dual 10bit AD9216\"; set xlabel \"MHz\"; set ylabel \"Power\"\n"); */
    while (j < time * PPS) {
        if(recvfrom(fd, packet_buf, MTU, 0, 
                    (struct sockaddr *)&client_addr, &client_len)<0) {
            fprintf(stderr, "first recvfrom() failed\n");
            exit(10);
        }
/*            printf ("plot \"-\" u (1424-$1+21.4):(10*log10($2)) with lines\n");  */
            for(i = 0; i < 2048; i++) {
/*                printf("%f\t",(double)i*62.5/512);  */
/*                 printf("%d\t" , (signed short)ntohs(((unsigned short *)packet_buf)[i*2])); 
                printf("%d\n" , (signed short)ntohs(((unsigned short *)packet_buf)[i*2+1])); } */
                f_power = ntohl(((unsigned long *)packet_buf)[i]);
                power[i] = (double)f_power + power[i];
                /* printf("%f\n", power[i]); */
    }
/*            printf("e\n"); */
            j++;
    }
    for(i = 1; i < 2048; i++) {
	printf("%f\t%f\n",i*70.0/4096 + freq - 13.6, power[i]/(j-1));
/*        printf("%f\t%f\n",i*62.5/4096+ 62.5*5/8+ freq -41.1,power[i]/(j-1)); */
/*	printf("%f\t%f\n",(i-256)*70.0/512+ freq+21.4-35,power[i]/(j-1)); */
	
    }
}

