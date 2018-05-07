/* De-dispersion and summation only, no integration. */
/* Update a gnuplot-graph while going trough the file */
// Program to live de-disperse and sum the frequency 
// channels, this code is based on the code of Paul
// At this moment it is Paul his code with extra comments

// In this part the C++ modules that are used are loaded
#include <sys/stat.h>
#include <netdb.h>
#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/uio.h>
#include <sys/stat.h>
#include <unistd.h>
#include <string.h>

// Define short notations for constants
/* points: 160, start: +40 */
#define POINTS 160
#define BUFFER 4096
#define START (256+40)
#define PPP 8
#define FREQ 406.00
#define SOCKSIZE (8*1024*1024)
#define MTU 9000

// Initialize two ints. 
int fd, fd2;

void check_sockbuf(int fd) {
	int optval;
	socklen_t optlen;

	optval = SOCKSIZE;
	optlen = sizeof(optval);
	if(setsockopt(fd, SOL_SOCKET, SO_RCVBUF, &optval, optlen)<0) {
		fprintf(stderr, "setsockopt failed\n");
		exit(10);
	}
	if(getsockopt(fd, SOL_SOCKET, SO_RCVBUF, &optval, &optlen)<0) {
		fprintf(stderr, "getsockopt failed\n");
		exit(10);
	}
	fprintf(stderr,"Getsocket SO_RCVBUF returned: %d\n",optval);
	if (optval <= SOCKSIZE) {
		fprintf(stderr, "SO_RCVBUF too small: increase net.core.rmem_max\n");
		exit(10);
	}
	return;
}

/* Calculate frequency from channel number */
double freq(int i) {
	double f;
	f = (i-256)/512.*70.0+21.4-35.0+FREQ; 
	return(f);
}

/* Calculate dispersion, in bins */
int dispersion(double f) {
	double dispersion;
/*	 dispersion = 4148.*26.68/(f*f); */ 
	dispersion = 4148.*14.20/(f*f);
	return((int)(dispersion*70000000./64./512.));
}


// Start of the main program
// Basically the program starts with a set of arguments
int main(int argc, char ** argv)
{
    // Initialize variables
    // Define double disp_buffer
	double * disp_buffer;
    // Define a buffer array with size BUFFER
	double buffer[BUFFER];
    // Define a unsighed long int
	unsigned long seqno = 0, oseqno , seqno1 = 0;
    // Define a double for the sum and period
	double sum, period;
    // Define an unsigned int packet
	uint32_t packet[513];
    // Define a avg array and a max.
	double avg[512], max;
    // Define an unsigned int for display
	unsigned int disp[512];
    // Define an unsigned int for maximum of disp
	unsigned int maxdisp;
	int16_t output;
	int i,j;
    
    // Use struct: type of data structure
	struct sockaddr_in server_addr, client_addr;
	socklen_t client_len = sizeof(client_addr);
	/* struct hostent *hp; */
	
	sscanf(argv[1],"%lf",&period);
	fprintf(stderr,"# Period: %f, frequency: %f\n",period, FREQ);
	printf("set terminal x11; unset mouse; set xtics 1; set grid; set yrange [0.97:1.5]\n");
	/* fill in dispersion table */
	for (i = 256; i < 512; i++) {
		disp[i]=dispersion(freq(i))-dispersion(freq(512));
	}
    // maximum of display
	maxdisp = disp[256];

    // certain situation fails, print failed
	if((disp_buffer = malloc(512*maxdisp*sizeof(double))) < 0) {
		fprintf(stderr,"Malloc failed\n");
		exit(10);
	}

	/*		if((fd = open("puls_raw", O_RDONLY, NULL)) < 0) {
			fprintf(stderr, "File open failed\n");
			exit(10);
			} */

	/*	if((fd2 = open("puls_sound", O_NONBLOCK | O_WRONLY |O_CREAT | O_TRUNC, S_IRUSR | S_IWUSR)) < 0) {
		fprintf(stderr,"Can't open output file pulsar_sound\n");
		exit(10);
		} */

    
    // assigne some arbitary value to fd2.
	fd2=4;
	if ((fd = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)) < 0) {
		fprintf(stderr, "no socket\n");
		exit(10);
	} 

    // 
	check_sockbuf(fd);

    //
	bzero(&server_addr, sizeof(server_addr));
	server_addr.sin_family = AF_INET;
	server_addr.sin_port = htons(22102);
	server_addr.sin_addr.s_addr=htonl(INADDR_ANY);
	if(bind(fd, (struct sockaddr *)&server_addr, sizeof(server_addr)) <0) {
		fprintf(stderr, "bind failed\n");
		exit(10);
	}

	while(1) { 
		if(recvfrom(fd, packet, MTU, 0, (struct sockaddr *)&client_addr, &client_len)<0) {
			fprintf(stderr, "recvfrom failed\n");
			exit(10);
		}
		oseqno = seqno;
		seqno = ntohl(packet[0]);
		if(seqno1 == 0) seqno1 = seqno;
		if ((seqno - oseqno > 1) && (oseqno != 0)) {
			fprintf(stderr,"Missed %ld packets\n",seqno -oseqno);
			for (j=oseqno + 1; j< seqno; j++) {
				for(i=START; i<START+POINTS; i++) {
					disp_buffer[i*maxdisp + (j + disp[i]) % maxdisp] = avg[i];
				}
				output = 0.04;
				write(fd2,&output,sizeof(output)); 
			}
		}


		sum = 0;

		for(i=START; i<START+POINTS; i++) {
			disp_buffer[i*maxdisp + (seqno - disp[i]) % maxdisp] = ntohl(packet[i+1]);
			if(seqno == seqno1) {
				avg[i] = disp_buffer[i*maxdisp + seqno % maxdisp];
			} else if(seqno - seqno1 < 10000) {
				avg[i]=avg[i]*(1.-1./(double)(seqno-seqno1))+1./(double)(seqno-seqno1)*disp_buffer[i*maxdisp + seqno % maxdisp];
			} else {
				avg[i]=avg[i]*0.9999+0.0001*disp_buffer[i*maxdisp + seqno % maxdisp];
			}
			sum += disp_buffer[i*maxdisp + seqno % maxdisp]/avg[i];
		}
		output = (short)((sum/POINTS -1)*32768.);
		output -= 0.04 * 32768;
		if (output < 0) output = 0;
		write(fd2,&output,sizeof(output));  
		/*		 printf("%lf\n%d\n",sum/POINTS,output); */
		buffer[seqno % BUFFER] = sum/POINTS;
		if (seqno % 64 == 0) { 
			printf("set xrange [%lf:%lf]\n",(seqno - BUFFER)/period, seqno/period);
			printf("plot '-' notitle w l\n");
			for (i = 0; i< BUFFER; i+=PPP) {
				max = 0;
				for (j = 0; j < PPP; j++) {
					if (max < buffer[(seqno + 1 +i + j)%BUFFER]) max = buffer[(seqno + 1 + i + j)%BUFFER];

				}
				printf("%lf\t%lf\n",(seqno - BUFFER + i)/period,max);
			}
			printf("e\n");
		} 
	}
	close(fd);
	close(fd2);
}

