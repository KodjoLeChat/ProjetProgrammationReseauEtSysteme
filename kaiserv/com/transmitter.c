#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <errno.h>
#include <sys/select.h>
#include "queue.h"
#include <curl/curl.h> // Ajouter par Pérès
#include <jansson.h> // Ajouter par Pérès

/*
Il faut installer les dépendances suivantes :

sudo apt-get install -y libcurl4-openssl-dev libjansson-dev

Il faut compiler le programme de la manière suivante :

gcc transmitter.c queue.c -o transmitter -lcurl -ljansson

*/


#define MAX_CLIENTS 10
#define BUFFER_SIZE 1024
//#define TCP_PORT 2024
//#define UDP_PORT 8000
#define MAX_BUFFER 1024


// Fonction pour extraire le username et le token d'une chaîne JSON ajoutéé par Pérès
void extractUsernameAndToken(const char *json_data, char *username, char *token) {
    // Analyser la chaîne JSON
    json_error_t error;
    json_t *root = json_loads(json_data, 0, &error);

    if (root == NULL) {
        fprintf(stderr, "Erreur lors de l'analyse JSON : %s\n", error.text);
        return;
    }

    // Récupérer le "username"
    json_t *username_json = json_object_get(root, "username");
    if (json_is_string(username_json)) {
        const char *username_str = json_string_value(username_json);
        strncpy(username, username_str, BUFFER_SIZE - 1);
        username[BUFFER_SIZE - 1] = '\0';
    } else {
        fprintf(stderr, "Erreur lors de la récupération du 'username'.\n");
    }

    // Récupérer le "token"
    json_t *token_json = json_object_get(root, "token");
    if (json_is_string(token_json)) {
        const char *token_str = json_string_value(token_json);
        strncpy(token, token_str, BUFFER_SIZE - 1);
        token[BUFFER_SIZE - 1] = '\0';
    } else {
        fprintf(stderr, "Erreur lors de la récupération du 'token'.\n");
    }

    // Libérer la mémoire
    json_decref(root);
}

struct MemoryStruct {
    char *memory;
    size_t size;
};

size_t WriteMemoryCallback(void *contents, size_t size, size_t nmemb, void *userp) {
    size_t realsize = size * nmemb;
    struct MemoryStruct *mem = (struct MemoryStruct *)userp;

    mem->memory = realloc(mem->memory, mem->size + realsize + 1);
    if (mem->memory == NULL) {
        fprintf(stderr, "Pas assez de mémoire (realloc a returné NULL)\n");
        return 0;
    }

    memcpy(&(mem->memory[mem->size]), contents, realsize);
    mem->size += realsize;
    mem->memory[mem->size] = 0;

    return realsize;
}

int check_token_validity(const char *username, const char *token) {
    CURL *curl;
    CURLcode res;

    struct MemoryStruct chunk;
    chunk.memory = malloc(1); 
    chunk.size = 0;

    curl_global_init(CURL_GLOBAL_DEFAULT);

    curl = curl_easy_init();
    if (curl) {
        char url[256];
        snprintf(url, sizeof(url), "http://localhost:5000/check_token");

        struct curl_slist *headers = NULL;
        headers = curl_slist_append(headers, "Content-Type: application/json");

        char post_fields[512];
        snprintf(post_fields, sizeof(post_fields), "{\"username\":\"%s\",\"token\":\"%s\"}", username, token);

        curl_easy_setopt(curl, CURLOPT_URL, url);
        curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
        curl_easy_setopt(curl, CURLOPT_POSTFIELDS, post_fields);

       
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteMemoryCallback);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, (void *)&chunk);

        res = curl_easy_perform(curl);

        if (res != CURLE_OK) {
            fprintf(stderr, "curl_easy_perform() failed: %s\n", curl_easy_strerror(res));
            free(chunk.memory);
            curl_easy_cleanup(curl);
            curl_global_cleanup();
            return 0;  // Échec de la requête
        }

        // Traitement de la réponse JSON
        json_error_t error;
        json_t *root = json_loads(chunk.memory, 0, &error);

        if (root == NULL) {
            fprintf(stderr, "Erreur lors de l'analyse JSON : %s\n", error.text);
            free(chunk.memory);
            curl_easy_cleanup(curl);
            curl_global_cleanup();
            return 0;  // Échec de l'analyse JSON
        }

        json_t *valid_json = json_object_get(root, "valid");
        int is_valid = json_is_true(valid_json);

        // Libération de la mémoire
        json_decref(root);
        free(chunk.memory);

        curl_easy_cleanup(curl);
        curl_global_cleanup();

        printf("is_valid in fonction: %d\n", is_valid);

        return is_valid;
    }

    return 0;  // Échec de l'initialisation de curl
}



void send_udp_message_to_tcp_client(const char *message, int tcpClientSocket) {
    int message_length = strlen(message);

    send(tcpClientSocket, message, message_length, 0); // Puis envoyer le message
}


void broadcast_udp_message(const char *message, int udpSocket, int udpPort) {
    struct sockaddr_in targetAddr;
    memset(&targetAddr, 0, sizeof(targetAddr));
    targetAddr.sin_family = AF_INET;
    targetAddr.sin_port = htons(udpPort);

    // Define the range of IPs for broadcasting
    for (int i = 1; i <= 255; i++) {
        char ip[20];
        sprintf(ip, "192.168.1.%d", i); // Adjust subnet as necessary
        inet_pton(AF_INET, ip, &targetAddr.sin_addr);

        sendto(udpSocket, message, strlen(message), 0, (struct sockaddr*)&targetAddr, sizeof(targetAddr));
    }
}

struct ip_node {
    struct sockaddr_in addr;
    struct ip_node* next;
};

struct ip_list {
    struct ip_node* head;
};


void send_udp_to_ip_list(const char *message, int message_length, int udpSocket, struct ip_list* list) {
    struct ip_node* current = list->head;
    while (current != NULL) {
        sendto(udpSocket, message, message_length, 0,
               (struct sockaddr*)&current->addr, sizeof(current->addr));
        current = current->next;
    }
}
void add_ip(struct ip_list* list, struct sockaddr_in addr) {
    struct ip_node* new_node = (struct ip_node*)malloc(sizeof(struct ip_node));
    if (new_node == NULL) {
        perror("Failed to allocate memory for new node");
        exit(EXIT_FAILURE);
    }
    new_node->addr = addr;
    new_node->next = list->head;
    list->head = new_node;
}

int ip_exists(struct ip_list* list, struct sockaddr_in addr) {
    struct ip_node* current = list->head;
    while (current != NULL) {
        if (current->addr.sin_addr.s_addr == addr.sin_addr.s_addr) {
            return 1;  // IP exists in the list
        }
        current = current->next;
    }
    return 0;  // IP does not exist in the list
}

void send_file_over_udp(const char *file_name, int udpSocket, struct sockaddr_in clientAddr) {
    FILE *file = fopen(file_name, "rb");
    if (file == NULL) {
        perror("Error opening file");
        return;
    }

    char file_buffer[MAX_BUFFER];
    size_t bytes_read;

    while ((bytes_read = fread(file_buffer, 1, MAX_BUFFER, file)) > 0) {
        sendto(udpSocket, file_buffer, bytes_read, 0, (struct sockaddr*)&clientAddr, sizeof(clientAddr));
    }

    fclose(file);
    printf("File sent successfully.\n");
}

int main(int argc, char *argv[]) {

    // verifie si le numero de port est fourni
    if (argc < 3) {
        fprintf(stderr, "Usage: %s <client port nbr (2024)> <udp port nbr(8000) >\n", argv[0]);
        return 1; // en cas d'erreur
    }

    int TCP_PORT = atoi(argv[1]);
    int UDP_PORT = atoi(argv[2]);

    // file pour organiser les messages entrants
    struct Queue incomingQueue;
    initializeQueue(&incomingQueue);

    // file pour organiser les messages sortants
    struct Queue outgoingQueue;
    initializeQueue(&outgoingQueue);

    int tcpServerSocket, newSocket, udpServerSocket;
    struct sockaddr_in tcpServerAddr, udpServerAddr, broadcast_address;
    fd_set readfds;
    char buffer[BUFFER_SIZE];
    char incomingBuffer[BUFFER_SIZE];
    char outgoingBuffer[BUFFER_SIZE];
    int maxSocket, valread;
    int python_client_socket = 0;

    if ((tcpServerSocket = socket(AF_INET, SOCK_STREAM, 0)) == -1) {
        perror("TCP Socket creation failed");
        exit(EXIT_FAILURE);
    }

    if ((udpServerSocket = socket(AF_INET, SOCK_DGRAM, 0)) == -1) {
        perror("UDP Socket creation failed");
        exit(EXIT_FAILURE);
    }

    memset(&tcpServerAddr, 0, sizeof(tcpServerAddr));
    memset(&udpServerAddr, 0, sizeof(udpServerAddr));

    tcpServerAddr.sin_family = AF_INET;
    tcpServerAddr.sin_addr.s_addr = INADDR_ANY;
    tcpServerAddr.sin_port = htons(TCP_PORT);

    udpServerAddr.sin_family = AF_INET;
    udpServerAddr.sin_addr.s_addr = INADDR_ANY;
    udpServerAddr.sin_port = htons(UDP_PORT);

    if (bind(tcpServerSocket, (struct sockaddr*)&tcpServerAddr, sizeof(tcpServerAddr)) == -1) {
        perror("TCP Bind failed");
        exit(EXIT_FAILURE);
    }

    if (bind(udpServerSocket, (struct sockaddr*)&udpServerAddr, sizeof(udpServerAddr)) == -1) {
        perror("UDP Bind failed");
        exit(EXIT_FAILURE);
    }
    broadcast_udp_message("", udpServerSocket, UDP_PORT);
    // Listen for incoming TCP connections
    if (listen(tcpServerSocket, 5) == -1) {
        perror("Listen failed");
        exit(EXIT_FAILURE);
    }

    printf("Server listening on TCP port %d and UDP port %d\n", TCP_PORT, UDP_PORT);


    struct ip_list ip_list_sent = {NULL};
    while (1) {
        FD_ZERO(&readfds);
        FD_SET(tcpServerSocket, &readfds);
        FD_SET(udpServerSocket, &readfds);
        
        if(python_client_socket > 0){
            FD_SET(python_client_socket, &readfds);
        }
        

        maxSocket = (tcpServerSocket > udpServerSocket) ? tcpServerSocket : udpServerSocket;

        int activity = select(FD_SETSIZE, &readfds, NULL, NULL, NULL);

        if ((activity < 0) && (errno != EINTR)) {
            perror("Select error");
        }

        socklen_t addrlen = sizeof(tcpServerAddr);

        if (FD_ISSET(tcpServerSocket, &readfds)) {
            
            if ((newSocket = accept(tcpServerSocket, (struct sockaddr *)&tcpServerAddr, (socklen_t*)&addrlen)) < 0) {
                perror("Erreur lors de l'acceptation de la connexion");
                exit(EXIT_FAILURE);
            }

            printf("Nouvelle connexion, socket fd : %d, adresse : %s, port : %d\n",
                   newSocket, inet_ntoa(tcpServerAddr.sin_addr), ntohs(tcpServerAddr.sin_port));

            python_client_socket = newSocket;
            
        }

        if (FD_ISSET(udpServerSocket, &readfds)) {
		struct sockaddr_in clientAddr;
		socklen_t len = sizeof(clientAddr);
            memset(buffer, 0, BUFFER_SIZE); // Effacer le buffer avant de recevoir
            
		    int bytesRead = recvfrom(udpServerSocket, buffer, BUFFER_SIZE, 0, (struct sockaddr*)&clientAddr, &len);
		    if (bytesRead == -1) {
		        perror("UDP Recvfrom failed");
		        exit(EXIT_FAILURE);
		    }

            enqueue(&incomingQueue, buffer);

		    printf("Received UDP message from %s:%d - %.*s\n",
		    inet_ntoa(clientAddr.sin_addr), ntohs(clientAddr.sin_port), bytesRead, buffer);

            char username[MAX_BUFFER];
            char token[MAX_BUFFER];
            extractUsernameAndToken(buffer, username, token);

            int is_valid_token = 0;

            is_valid_token = check_token_validity(username, token);

            printf("is_valid_token: %d\n", is_valid_token);
            if (is_valid_token == 1) {
                printf("Token is valid!\n");
                // Construire le message "OK"
                const char *ok_message = "OK";

                // Envoyer le message "OK" au client
                sendto(udpServerSocket, ok_message, strlen(ok_message), 0,
                (struct sockaddr*)&clientAddr, sizeof(clientAddr));
            } else {
                printf("Token is NOT valid!\n");
            }

            printf("Token: %s\n", token);

            printf("Username: %s\n", username);

            printf("Buffer: %s\n", buffer);

            printf("IP: %s\n", inet_ntoa(clientAddr.sin_addr));

            printf("len: %d\n", len);

            int ip_exist = ip_exists(&ip_list_sent, clientAddr);

            printf("ip_exist: %d\n", ip_exist);

		    // Check if the IP address has already been sent the file
		    if (ip_exist == 0 && is_valid_token == 1) {
		        // Send the save.sav file to the client over UDP
		       // send_file_over_udp("test.txt", udpServerSocket, clientAddr);
		        // Add the IP address to the list so the file is not sent again
		        add_ip(&ip_list_sent, clientAddr);
		    }

            memset(incomingBuffer, 0, BUFFER_SIZE); // Effacer incomingbuffer avant de defiler
            strncpy(incomingBuffer, dequeue(&incomingQueue), BUFFER_SIZE);

		    // Send the UDP message to the TCP client
		    if (python_client_socket > 0) {
		        send_udp_message_to_tcp_client(incomingBuffer, python_client_socket);
		    }
        }


        if (FD_ISSET(python_client_socket, &readfds)) {
            if ((valread = read(python_client_socket, buffer, sizeof(buffer))) == 0) {
                    
                    printf("Client déconnecté, socket fd : %d\n", python_client_socket);
                    close(python_client_socket);
                    python_client_socket = 0;
                } else {
                    
                    buffer[valread] = '\0';
                    printf("Données reçues du client, socket fd : %d : %s\n", python_client_socket, buffer);
                
                enqueue(&outgoingQueue, buffer);
                    // send(python_client_socket, "Message reçu avec succès\n", strlen("Message reçu avec succès\n"), 0);
                memset(outgoingBuffer, 0, BUFFER_SIZE); // clean buffer

                strncpy(outgoingBuffer, dequeue(&outgoingQueue), BUFFER_SIZE);

                send_udp_to_ip_list(outgoingBuffer, valread, udpServerSocket, &ip_list_sent);
                    
                if (udpServerSocket > 0) {
                    printf("Dans updServerSocket\n");
                    // Spécifiez le port UDP 8001
                    broadcast_address.sin_port = htons(8001);

                    // Utilisez la ligne mise à jour pour l'envoi UDP avec le port 8001
                    sendto(udpServerSocket, buffer, strlen(buffer), 0, (struct sockaddr*)&broadcast_address, sizeof(broadcast_address));

                    // // TODO Ayet
                    // // Ajout des adresses des joueurs dans une liste
                    // // faire une boucle while pour envoyer msg a tous les joueurs
                    // memset(&broadcast_address, 0, sizeof(broadcast_address));
                    // broadcast_address.sin_family = AF_INET;
                    // broadcast_address.sin_port = htons(UDP_PORT);
                    // inet_pton(AF_INET, "192.168.0.101", &(broadcast_address.sin_addr));
                    
                    //printf("the message: %s", buffer);
    
                    //sendto(udpServerSocket, buffer, strlen(buffer), 0, (struct sockaddr*)&broadcast_address, sizeof(broadcast_address));

                }
                }
            
        }
    }

    close(tcpServerSocket);
    close(udpServerSocket);

    return 0;
}