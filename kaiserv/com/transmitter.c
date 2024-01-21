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

    // Listen for incoming TCP connections
    if (listen(tcpServerSocket, 5) == -1) {
        perror("Listen failed");
        exit(EXIT_FAILURE);
    }

    printf("Server listening on TCP port %d and UDP port %d\n", TCP_PORT, UDP_PORT);

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
            socklen_t len = sizeof(struct sockaddr_in);

            int bytesRead = recvfrom(udpServerSocket, buffer, BUFFER_SIZE, 0, (struct sockaddr*)&udpServerAddr, &len);

            if (bytesRead == -1) {
                perror("UDP Recvfrom failed");
                exit(EXIT_FAILURE);
            }

            printf("Received UDP message from %s:%d - %.*s\n",
                   inet_ntoa(udpServerAddr.sin_addr), ntohs(udpServerAddr.sin_port), bytesRead, buffer);

            if (python_client_socket > 0) {
                send(python_client_socket, buffer, bytesRead, 0);
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
