#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <netinet/in.h>

#define PORT 12345
#define MAX_BUFFER_SIZE 1024

int main() {
    int server_socket, client_socket;
    struct sockaddr_in server_address, client_address;
    char buffer[MAX_BUFFER_SIZE];

    // Créez un socket
    if ((server_socket = socket(AF_INET, SOCK_STREAM, 0)) == -1) {
        perror("Error creating socket");
        exit(EXIT_FAILURE);
    }

    // Configurez l'adresse du serveur
    server_address.sin_family = AF_INET;
    server_address.sin_port = htons(PORT);
    server_address.sin_addr.s_addr = INADDR_ANY;

    // Liez le socket au port
    if (bind(server_socket, (struct sockaddr*)&server_address, sizeof(server_address)) == -1) {
        perror("Error binding socket");
        exit(EXIT_FAILURE);
    }

    // Écoutez les connexions entrantes
    if (listen(server_socket, 5) == -1) {
        perror("Error listening for connections");
        exit(EXIT_FAILURE);
    }

    printf("Server listening on port %d...\n", PORT);

    // Acceptez la connexion entrante
    socklen_t client_address_len = sizeof(client_address);
    client_socket = accept(server_socket, (struct sockaddr*)&client_address, &client_address_len);

    if (client_socket == -1) {
        perror("Error accepting connection");
        exit(EXIT_FAILURE);
    }

    // Recevez les données JSON
    ssize_t bytes_received = recv(client_socket, buffer, sizeof(buffer), 0);

    if (bytes_received == -1) {
        perror("Error receiving data");
        exit(EXIT_FAILURE);
    }

    // Ajoutez un caractère de fin de chaîne à la fin du buffer pour imprimer correctement
    buffer[bytes_received] = '\0';

    // Affichez les données reçues
    printf("Received data: %s\n", buffer);

    // Fermez les sockets
    close(client_socket);
    close(server_socket);

    return 0;
}
