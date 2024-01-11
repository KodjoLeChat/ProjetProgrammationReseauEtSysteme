#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <fcntl.h>

#define MAX_BUFFER_SIZE 1024
#define PIPE_NAME "/tmp/netstat_pipe_received"

int main() {
    int client_socket, pipe_fd;
    struct sockaddr_in server_address;
    char buffer[MAX_BUFFER_SIZE];
    char ip[INET_ADDRSTRLEN];
    int port;
    FILE *configFile;

    // Open the config file
    configFile = fopen("config.txt", "r");
    if (configFile == NULL) {
        perror("Error opening config file");
        exit(EXIT_FAILURE);
    }

    // Read IP and port from the config file
    if (fscanf(configFile, "%s %d", ip, &port) != 2) {
        perror("Error reading config file");
        fclose(configFile);
        exit(EXIT_FAILURE);
    }
    fclose(configFile);

    // Create a socket
    if ((client_socket = socket(AF_INET, SOCK_STREAM, 0)) == -1) {
        perror("Error creating socket");
        exit(EXIT_FAILURE);
    }

    // Configure the server address
    server_address.sin_family = AF_INET;
    server_address.sin_port = htons(port);
    if (inet_pton(AF_INET, ip, &server_address.sin_addr) <= 0) {
        perror("Invalid address/Address not supported");
        exit(EXIT_FAILURE);
    }

    // Connect to the server
    if (connect(client_socket, (struct sockaddr*)&server_address, sizeof(server_address)) == -1) {
        perror("Error connecting to server");
        exit(EXIT_FAILURE);
    }

    // Open the named pipe for writing
    pipe_fd = open(PIPE_NAME, O_WRONLY);
    if (pipe_fd == -1) {
        perror("Error opening named pipe");
        exit(EXIT_FAILURE);
    }

// Loop to continuously receive data and write to the named pipe
ssize_t bytes_received;
while (1) { // Infinite loop
    bytes_received = recv(client_socket, buffer, sizeof(buffer), 0);
    
    // Check for errors or socket closure
    if (bytes_received == -1) {
        perror("Error receiving data");
        break;
    } else if (bytes_received == 0) {
        printf("Socket closed by the server.\n");
        break;
    }

    // Write received data to the named pipe
    if (write(pipe_fd, buffer, bytes_received) == -1) {
        perror("Error writing to named pipe");
        break;
    }

    // Example condition to exit the loop - you can modify this according to your needs
    if (strcmp(buffer, "STOP") == 0) {
        printf("Stop message received. Exiting loop.\n");
        break;
    }
}

// Close the named pipe and client socket
close(pipe_fd);
close(client_socket);

printf("Client disconnected.\n");

    return 0;
}
