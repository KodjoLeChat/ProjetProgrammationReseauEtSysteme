#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <pthread.h>

#define MAX_CLIENTS 10

int client_sockets[MAX_CLIENTS];
int num_clients = 0;

void send_utf8_message(int client_socket, const char *message) {
    char utf8_message[1024];
    int len = snprintf(utf8_message, sizeof(utf8_message), "%s", message);
    send(client_socket, utf8_message, len, 0);
}

void broadcast_message(int sender, const char *message) {
    for (int i = 0; i < num_clients; i++) {
        if (i != sender) {
            send_utf8_message(client_sockets[i], message);
        }
    }
}

void *handle_client(void *arg) {
    int client_socket = *(int *)arg;
    char message[1024];
    while (1) {
        int bytes_received = recv(client_socket, message, sizeof(message), 0);
        if (bytes_received <= 0) {
            // Le joueur s'est déconnecté
            close(client_socket);
            break;
        }
        message[bytes_received] = '\0';
        printf("Message reçu : %s\n", message);
        broadcast_message(client_socket, message);
    }
    return NULL;
}

int main() {
    int server_socket;
    struct sockaddr_in server_addr, client_addr;
    socklen_t addr_size = sizeof(client_addr);

    server_socket = socket(AF_INET, SOCK_STREAM, 0);
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(12346);
    server_addr.sin_addr.s_addr = INADDR_ANY;

    bind(server_socket, (struct sockaddr *)&server_addr, sizeof(server_addr));
    listen(server_socket, 10);
    printf("Server waiting for connections...\n");

    while (num_clients < MAX_CLIENTS) {
        client_sockets[num_clients] = accept(server_socket, (struct sockaddr *)&client_addr, &addr_size);
        printf("Player %d connected\n", num_clients + 1);
        // Démarrer un thread pour gérer la communication avec ce joueur
        pthread_t client_thread;
        pthread_create(&client_thread, NULL, handle_client, &client_sockets[num_clients]);
        num_clients++;
    }

    // Attendre la fin de tous les threads clients (vous devriez le faire ici)
    for (int i = 0; i < num_clients; i++) {
        close(client_sockets[i]);
    }

    close(server_socket);

    return 0;
}

