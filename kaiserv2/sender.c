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
    FILE *configFile, *sendFile;

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
    while (listen(server_socket, 5) == -1) {
        perror("Error connecting to server");
	sleep(1);
    }

    printf("Server listening on port %d...\n", port);

    // Accept the incoming connection
    socklen_t client_address_len = sizeof(client_address);
    client_socket = accept(server_socket, (struct sockaddr*)&client_address, &client_address_len);

    if (client_socket == -1) {
        perror("Error accepting connection");
        exit(EXIT_FAILURE);
    }

    // Open the file to send
    sendFile = fopen("save.sav", "rb");
    if (sendFile == NULL) {
        perror("Error opening file to send");
        exit(EXIT_FAILURE);
    }

    // Read the file and send its contents
    ssize_t bytes_read;
    while ((bytes_read = fread(buffer, 1, sizeof(buffer), sendFile)) > 0) {
        ssize_t bytes_sent = send(client_socket, buffer, bytes_read, 0);
        if (bytes_sent == -1) {
            perror("Error sending file data");
            fclose(sendFile);
            exit(EXIT_FAILURE);
        }
    }

    // Close the file and sockets
    fclose(sendFile);
    close(client_socket);
    close(server_socket);

    printf("File sent.\n");

    return 0;
}

