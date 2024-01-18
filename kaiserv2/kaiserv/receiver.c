
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <netinet/in.h>

#define MAX_BUFFER_SIZE 1024

int main() {
    int server_socket, client_socket;
    struct sockaddr_in server_address, client_address;
    char buffer[MAX_BUFFER_SIZE];
    int port;
    FILE *configFile, *saveFile;


    // Open the connection file
    configFile = fopen("connection.txt", "r");
    if (configFile == NULL) {
        perror("Error opening connection file");
        exit(EXIT_FAILURE);
    }

    // Read port number from the connection file
    if (fscanf(configFile, "%d", &port) != 1) {
        perror("Error reading connection file");
        fclose(configFile);
        exit(EXIT_FAILURE);
    }
    fclose(configFile);

    // Create a socket
    if ((server_socket = socket(AF_INET, SOCK_STREAM, 0)) == -1) {
        perror("Error creating socket");
        exit(EXIT_FAILURE);
    }

    // Configure the server address
    server_address.sin_family = AF_INET;
    server_address.sin_port = htons(port);
    server_address.sin_addr.s_addr = INADDR_ANY;

    // Bind the socket to the port
    if (bind(server_socket, (struct sockaddr*)&server_address, sizeof(server_address)) == -1) {
        perror("Error binding socket");
        exit(EXIT_FAILURE);
    }

    // Listen for incoming connections
    if (listen(server_socket, 5) == -1) {
        perror("Error listening for connections");
        exit(EXIT_FAILURE);
    }

    printf("Server listening on port %d...\n", port);

    // Accept the incoming connection
    socklen_t client_address_len = sizeof(client_address);
    client_socket = accept(server_socket, (struct sockaddr*)&client_address, &client_address_len);

    if (client_socket == -1) {
        perror("Error accepting connection");
        exit(EXIT_FAILURE);
    }

    // Receive data
    ssize_t bytes_received = recv(client_socket, buffer, sizeof(buffer), 0);

    if (bytes_received == -1) {
        perror("Error receiving data");
        exit(EXIT_FAILURE);
    }

    // Null-terminate the buffer for correct printing
    buffer[bytes_received] = '\0';

    // Open the onlineWorld.sav file for writing
    saveFile = fopen("onlineWorld.sav", "w");
    if (saveFile == NULL) {
        perror("Error opening save file");
        exit(EXIT_FAILURE);
    }

    // Write the received data to the file
    fwrite(buffer, 1, bytes_received, saveFile);

    // Close the save file
    fclose(saveFile);

    printf("Received data: %s\n", buffer);

    // Close the sockets
    close(client_socket);
    close(server_socket);

    return 0;
}

