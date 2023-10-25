#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <pthread.h>

typedef struct {
    int socket;
    char* client_id;
} SocketInfo;

int connected_player[10]; // 10 limite de joeur connected

void initialize_players_spot(int *connected_player){
    for (int i = 0; i < sizeof(connected_player); i++){
    connected_player[i] = 0;
}
}

int indice = 0;
SocketInfo socket_info;

char *uniqueID();

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

            for (int i = 0; i < sizeof(connected_player); i++){
                if((connected_player[i] != 0) && (connected_player[i] != client_socket)){
                     if (send(connected_player[i], message, strlen(message), 0) < 0) {
                            perror("Error sending data");
                        }
                }
            }
           
        }
    }

    return NULL;
}

int main() {
    int server_socket, client_socket;
    struct sockaddr_in server_address, client_address;
    socklen_t client_address_length = sizeof(client_address);
    
    // Initialize players
    initialize_players_spot(connected_player);

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
        //socket_info.socket = client_socket;
        //socket_info.client_id = uniqueID();
        connected_player[indice++] = client_socket;
        //printf("le numero de socket est: %d et le numero client est: %s\n", socket_info.socket, socket_info.client_id);
        for (int i = 0; i < sizeof(client_socket); i++){
            if(connected_player[i] != 0)
            printf("id client connecte %d\n", connected_player[i]);
        }
        if (client_socket < 0) {
            perror("Error accepting connection");
            continue;
        }

        pthread_t client_thread;
        if (pthread_create(&client_thread, NULL, client_handler, &client_socket) != 0) {
            perror("Error creating client thread");
            close(client_socket);
        }

    }

    close(server_socket);

    return 0;
}

char *uniqueID(){

     // Get the current timestamp
    time_t current_time;
    time(&current_time);
    
    // Convert the timestamp to a string
    char timestamp_str[20];
    snprintf(timestamp_str, sizeof(timestamp_str), "%ld", current_time);
    
    // Generate a random number
    int random_number = rand();
    
    // Convert the random number to a string
    char random_number_str[20];
    snprintf(random_number_str, sizeof(random_number_str), "%d", random_number);
    
        // Calculate the length of the unique ID
    int length = snprintf(NULL, 0, "%s%s", timestamp_str, random_number_str) + 1;
    
    // Allocate memory for the unique ID
    char *unique_id = (char *)malloc(length);
    
    // Check if memory allocation was successful
    if (unique_id != NULL) {
        // Concatenate the timestamp and random number to create the unique ID
        snprintf(unique_id, length, "%s%s", timestamp_str, random_number_str);
    }
    
    return unique_id;
}
