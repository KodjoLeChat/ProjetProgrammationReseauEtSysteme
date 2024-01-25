#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <errno.h>
#include <sys/select.h>

#define MAX_CLIENTS 10
#define BUFFER_SIZE 1024
#define TCP_PORT 2024
#define UDP_PORT 8000
#define MAX_BUFFER 1024



void send_udp_message_to_tcp_client(const char *message, int tcpClientSocket) {
    // Send the UDP message to the TCP client
    send(tcpClientSocket, message, strlen(message), 0);
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

int main() {
    int tcpServerSocket, newSocket, udpServerSocket;
    struct sockaddr_in tcpServerAddr, udpServerAddr, broadcast_address;
    fd_set readfds;
    char buffer[BUFFER_SIZE];
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
    broadcast_udp_message("Hello my besto friendo", udpServerSocket, UDP_PORT);
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
		    int bytesRead = recvfrom(udpServerSocket, buffer, BUFFER_SIZE, 0, (struct sockaddr*)&clientAddr, &len);
		    if (bytesRead == -1) {
		        perror("UDP Recvfrom failed");
		        exit(EXIT_FAILURE);
		    }
		    printf("Received UDP message from %s:%d - %.*s\n",
		           inet_ntoa(clientAddr.sin_addr), ntohs(clientAddr.sin_port), bytesRead, buffer);

		    // Check if the IP address has already been sent the file
		    if (!ip_exists(&ip_list_sent, clientAddr)) {
		        // Send the save.sav file to the client over UDP
		        send_file_over_udp("test.txt", udpServerSocket, clientAddr);
		        // Add the IP address to the list so the file is not sent again
		        add_ip(&ip_list_sent, clientAddr);
		    }

		    // Send the UDP message to the TCP client
		    if (python_client_socket > 0) {
		        send_udp_message_to_tcp_client(buffer, python_client_socket);
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
                    
                    // send(python_client_socket, "Message reçu avec succès\n", strlen("Message reçu avec succès\n"), 0);
                send_udp_to_ip_list(buffer, valread, udpServerSocket, &ip_list_sent);
                    
                if (udpServerSocket > 0) {
                    // TODO Ayet
                    // Ajout des adresses des joueurs dans une liste
                    // faire une boucle while pour envoyer msg a tous les joueurs
                    memset(&broadcast_address, 0, sizeof(broadcast_address));
                    broadcast_address.sin_family = AF_INET;
                    broadcast_address.sin_port = htons(UDP_PORT);
                    inet_pton(AF_INET, "192.168.0.101", &(broadcast_address.sin_addr));
                    
                    printf("the message: %s", buffer);
    
                    sendto(udpServerSocket, buffer, strlen(buffer), 0, (struct sockaddr*)&broadcast_address, sizeof(broadcast_address));

                }
                }
            
        }
    }

    close(tcpServerSocket);
    close(udpServerSocket);

    return 0;
}
