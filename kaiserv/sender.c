#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <fcntl.h>
#include <unistd.h>

#define MAX_BUFFER_SIZE 1024

int main() {
    int server_socket, client_socket;
    struct sockaddr_in server_address, client_address;
    char buffer[MAX_BUFFER_SIZE];
    int port, pipe_fd;
    FILE *configFile;

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

    // Enable the socket to reuse the address
    int yes = 1;
    if (setsockopt(server_socket, SOL_SOCKET, SO_REUSEADDR, &yes, sizeof(yes)) == -1) {
        perror("setsockopt");
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
        perror("Error listening on socket");
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

    // Open the named pipe for reading
    pipe_fd = open("/tmp/netstat_pipe", O_RDONLY);
    if (pipe_fd == -1) {
        perror("Error opening named pipe");
        exit(EXIT_FAILURE);
    }

    // Continuously read from the named pipe and send its contents
    while (1) {
        ssize_t bytes_read = read(pipe_fd, buffer, sizeof(buffer));
        if (bytes_read > 0) {
            ssize_t bytes_sent = send(client_socket, buffer, bytes_read, 0);
            if (bytes_sent == -1) {
                perror("Error sending data");
                break;
            }
        } else if (bytes_read == -1) {
            perror("Error reading from pipe");
            break;
        }
    }

    // Close the named pipe and sockets
    close(pipe_fd);
    close(client_socket);
    close(server_socket);

    printf("Server socket closed.\n");
    return 0;
}
