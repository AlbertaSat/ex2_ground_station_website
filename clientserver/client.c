#include <stdio.h> /* printf, sprintf */
#include <stdlib.h> /* exit */
#include <unistd.h> /* read, write, close */
#include <string.h> /* memcpy, memset */
#include <sys/socket.h> /* socket, connect */
#include <netinet/in.h> /* struct sockaddr_in, struct sockaddr */
#include <netdb.h> /* struct hostent, gethostbyname */
#include <sys/types.h>
/*for getting file size using stat()*/
#include<sys/stat.h>

#define MAX 80 
#define PORT 8080 
#define SA struct sockaddr

void client_main(int sockfd) 
{ 
	char buff[MAX]; 
	int n;

	// MAIN CLIENT LOOP //
	for (;;) { 
		bzero(buff, sizeof(buff)); 
		printf("Enter the string : "); 
		n = 0; 
		while ((buff[n++] = getchar()) != '\n');

		write(sockfd, buff, sizeof(buff));
		bzero(buff, sizeof(buff)); // erase buffer

		// await response from 
		read(sockfd, buff, sizeof(buff));
		printf("From Server : %s", buff);
		if ((strncmp(buff, "exit", 4)) == 0) {
			printf("Client Exit...\n");
			break;
		}
	}
}


int main()
{
	int sockfd, connfd;
	struct sockaddr_in servaddr, cli;

	// Create socket, initialize connection
	sockfd = socket(AF_INET, SOCK_STREAM, 0);
	if (sockfd == -1) {
		printf("socket creation failed...\n");
		exit(0);
	}
	else
		printf("Socket successfully created..\n");
	bzero(&servaddr, sizeof(servaddr));

	// assign IP, PORT
	servaddr.sin_family = AF_INET;
	servaddr.sin_addr.s_addr = inet_addr("127.0.0.1");
	servaddr.sin_port = htons(PORT);
	// connect the client socket to server socket
	if (connect(sockfd, (SA*)&servaddr, sizeof(servaddr)) != 0) {
		printf("connection with the server failed...\n"); 
		exit(0); 
	}
	else
		printf("connected to the server..\n"); 

	// client loop for communication
	client_main(sockfd); 

	// close the socket 
	close(sockfd); 
} 
