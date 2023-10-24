#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <pthread.h>

typedef struct {
    int socket;

} SocketInfo;

SocketInfo socket_info;

void *client_handler(void *arg) {
    int client_socket = *((int *)arg);
    char buffer_r[2046];
    ssize_t bytes_received;

    while (1) {
        bytes_received = recv(client_socket, buffer_r, sizeof(buffer_r), 0);
        if (bytes_received <= 0) {
            close(client_socket);
            break;
        } else {
            buffer_r[bytes_received] = '\0'; // Ensure the string is null-terminated.
            printf("Received: %s", buffer_r);
            
            // Handle the client's request here and send a response if needed.
            char message[] = "Hello, server!";
            strcpy(message, buffer_r);

            if (send(client_socket, message, strlen(message), 0) < 0) {
                perror("Error sending data");
            }
        }
    }

    return NULL;
}

int main() {
    int server_socket, client_socket;
    struct sockaddr_in server_address, client_address;
    socklen_t client_address_length = sizeof(client_address);

    server_socket = socket(AF_INET, SOCK_STREAM, 0);
    if (server_socket == -1) {
        perror("Error creating socket");
        exit(EXIT_FAILURE);
    }

    // Initialize and bind the server socket (similar to your original code).
    // Initialize the server address structure
    server_address.sin_family = AF_INET;
    server_address.sin_port = htons(2024); // Replace with your desired port
    server_address.sin_addr.s_addr = INADDR_ANY;

      // Bind the socket to the address
    if (bind(server_socket, (struct sockaddr*)&server_address, sizeof(server_address)) < 0) {
        perror("Error binding socket");
        close(server_socket);
        exit(EXIT_FAILURE);
    }
    // Listen for incoming connections (similar to your original code).
    if (listen(server_socket, 5) < 0) {
        perror("Error listening");
        close(server_socket);
        exit(EXIT_FAILURE);
    }

    printf("Server listening on port 2024...\n");

    while (1) {
        client_socket = accept(server_socket, (struct sockaddr*)&client_address, &client_address_length);
        printf("le numero de socket : %d\n", client_socket);
        if (client_socket < 0) {
            perror("Error accepting connection");
            continue;
        }

        pthread_t client_thread;
        if (pthread_create(&client_thread, NULL, client_handler, &client_socket) != 0) {
            perror("Error creating client thread");
            close(client_socket);
        }

        pthread_t client_thread1;
        if (pthread_create(&client_thread1, NULL, client_handler, &client_socket) != 0) {
            perror("Error creating client thread");
            close(client_socket);
        }
    }

    close(server_socket);

    return 0;
}
