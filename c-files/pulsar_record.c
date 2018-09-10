#define _FILE_OFFSET_BITS 64
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
#include <fcntl.h>
#include <sys/stat.h>
#include <cstdlib>

/* Define some short notations */
#define CLK (140000000. / 2)
#define SOCKSIZE (8388608*8)
#define MTU 8900
/*#define MAXCOUNT (unsigned long)(30 * CLK * 60. / 64. / 512.)*/
#define MAXCOUNT 1024*1024
unsigned char * packet_buf;
int fd,fdw;

int main(int argc, char * argv[])
{
    /* Initialize some variables
     */
    int i,j = 0;
    struct sockaddr_in server_addr, client_addr;
    struct hostent *hp;
    struct timeval stamp;
    unsigned int packet_counter, max_packet_counter, client_len=sizeof(client_addr);
    int optval, optlen;
    ssize_t ps;

    int total_time;

    /* If statement that checks if either one or two arguments 
     * are given to the function.
     */
    if (argc != 2 && argc != 3) {
        fprintf(stderr, "%s requires one or two argument:\n", argv[0]);
        fprintf(stderr, "-%s <filename>\n", argv[0]);
        fprintf(stderr, "-%s <observation time> <filename>\n", argv[0]);
    }
    /* The following statement is if only 1 extra argument is given
     */
    else if (argc == 2) {
        if ((fdw = open(argv[1],  O_WRONLY| O_CREAT | O_TRUNC, S_IRUSR | S_IWUSR)) < 0) {
            fprintf(stderr, "Can't open %s\n", argv[1]);
            exit(10);
        }
    }
    /* The following statements are exectuted if 2 extra arguments are given
     */
    else if (argc == 3) {
        if ((fdw = open(argv[2],  O_WRONLY| O_CREAT | O_TRUNC, S_IRUSR | S_IWUSR)) < 0) {
            fprintf(stderr, "Can't open %s\n", argv[2]);
            exit(10);
        }
        total_time = atoi(argv[1]);
    }
    /* The following statement is executed if the world goes down.
     */ 
    else {
        fprintf(stderr,"Weird stuff is happening\n");
    }


    /* Statement that checks if the socket is present
     */
    if ((fd = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)) < 0) {
	    fprintf(stderr, "no socket\n");
	    exit(10);
    }
    // specify socket size etc.
    optval = SOCKSIZE;
    optlen = sizeof(optval);

    /* Set some socket options
     */
    if(setsockopt(fd, SOL_SOCKET, SO_RCVBUF, &optval, optlen)<0) {
        fprintf(stderr, "setsockopt failed\n");
        exit(10);
    }
    /* Get some socket options
     */
    if(getsockopt(fd, SOL_SOCKET, SO_RCVBUF, &optval, &optlen)<0) {
        fprintf(stderr, "getsockopt failed\n");
        exit(10);
    }
    fprintf(stderr, "Getsocket SO_RCVBUF returned: %d\n",optval);
    if (optval <= SOCKSIZE) {
        fprintf(stderr, "SO_RCVBUF too small: increase net.core.rmem_max to %ld\n",SOCKSIZE);
        exit(10);
    }

    bzero(&server_addr, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(22102);
    server_addr.sin_addr.s_addr=htonl(INADDR_ANY);
    if(bind(fd, (struct sockaddr *)&server_addr, sizeof(server_addr)) <0) {
	fprintf(stderr, "bind failed\n");
	exit(10); 
    }
    if((packet_buf = malloc(MTU)) == NULL) {
	fprintf(stderr, "malloc failed\n");
	exit(10);
    }

    while (j < MAXCOUNT) {
        if((ps=recvfrom(fd, packet_buf, MTU, 0, 
                    (struct sockaddr *)&client_addr, &client_len))<0) {
            fprintf(stderr, "recvfrom() failed\n");
            exit(10);
        }
	if(ps != 2052)
	{
		fprintf(stderr, "Read %ld bytes!\n", ps);
	}
	memcpy(packet_buf+256*4, packet_buf, 4); /* Copy the packet counter to second half */
	write(fdw,packet_buf+256*4,256*4);  /* Write only the second half */
    // So that implies that the frequency freq(256) is discarded. That bin starts at FREQ+21.4-35.0 MHz. 
	j++;
	if (j % (int)(70000000/512/64) == 0)
	{
		printf("MB: %d\n",(int)(j/1024));
		fsync(fdw);
	}
    }
    close(fd);
    close(fdw);
}

