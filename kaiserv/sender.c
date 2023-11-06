#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <netinet/in.h>

#define PORT 12345
#define MAX_BUFFER_SIZE 1024

int main() {
    int client_socket;
    struct sockaddr_in server_address;
    char buffer[MAX_BUFFER_SIZE];

    // Open the file for reading
    FILE *file = fopen("building.json", "r");

    if (file == NULL) {
        perror("Error opening file");
        exit(EXIT_FAILURE);
    }

    // Read the JSON data from the file
    size_t bytes_read = fread(buffer, 1, MAX_BUFFER_SIZE, file);

    if (bytes_read == 0) {
        perror("Error reading from file");
        exit(EXIT_FAILURE);
    }

    // Close the file
    fclose(file);

    // Null-terminate the buffer
    buffer[bytes_read] = '\0';

    // Create a socket
    if ((client_socket = socket(AF_INET, SOCK_STREAM, 0)) == -1) {
        perror("Error creating socket");
        exit(EXIT_FAILURE);
    }

    // Configure the server address
    server_address.sin_family = AF_INET;
    server_address.sin_port = htons(PORT);
    server_address.sin_addr.s_addr = INADDR_ANY;

    // Connect to the server
    if (connect(client_socket, (struct sockaddr*)&server_address, sizeof(server_address)) == -1) {
        perror("Error connecting to server");
        exit(EXIT_FAILURE);
    }

    // Send the JSON data
    ssize_t bytes_sent = send(client_socket, buffer, strlen(buffer), 0);

    if (bytes_sent == -1) {
        perror("Error sending data");
        exit(EXIT_FAILURE);
    }

    printf("Data sent.\n");

    // Close the client socket
    close(client_socket);

    return 0;
}
