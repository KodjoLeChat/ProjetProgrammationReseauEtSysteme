#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#define MAX_BUFFER_SIZE 1024

int main() {
    int client_socket;
    struct sockaddr_in server_address;
    char buffer[MAX_BUFFER_SIZE];
    char ip[INET_ADDRSTRLEN];
    int port;
    FILE *receivedFile, *configFile;

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
	sleep(1);
    }

    // Open the file to receive data
    receivedFile = fopen("onlineWorld.sav", "wb");
    if (receivedFile == NULL) {
        perror("Error opening received file");
        exit(EXIT_FAILURE);
    }

    // Receive and write data to the file
    ssize_t bytes_received;
    while ((bytes_received = recv(client_socket, buffer, sizeof(buffer), 0)) > 0) {
        ssize_t bytes_written = fwrite(buffer, 1, bytes_received, receivedFile);
        if (bytes_written != bytes_received) {
            perror("Error writing to received file");
            fclose(receivedFile);
            exit(EXIT_FAILURE);
        }
    }

    // Close the received file and client socket
    fclose(receivedFile);
    close(client_socket);

    printf("File received.\n");

    return 0;
}

