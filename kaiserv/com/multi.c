#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <string.h>
#include "queue.h"

#define MCAST_ADDR "224.0.0.1"
#define MCAST_PORT 8888
#define MCAST_TTL 255
#define BUFFER_SIZE 1024

// Structure to represent a player
struct Player {
  char name[20];
  int score;
};

void initialize_player(struct Player *player) {
  printf("Enter your name (up to 19 characters): ");
  fgets(player->name, sizeof(player->name), stdin);
  player->name[strcspn(player->name, "\n")] = '\0';  // Remove the newline character
  player->score = 0;
}

void create_game_message(const struct Player *player, char *buf) {
  // Modified: Include player's name in the game message
  sprintf(buf, "Player %s, SCORE:%d", player->name, player->score);
}

void process_received_message(const char *message, struct Player *player) {
  printf("Received: %s\n", message);

  // For demonstration purposes, let's assume the message format is "Player <name>, SCORE:<score>"
  char name[20];
  int received_score;

  if (sscanf(message, "Player %19s, SCORE:%d", name, &received_score) == 2) {
    printf("Received message from %s with score: %d\n", name, received_score);

    // Update player information
    if (strcmp(name, player->name) == 0) {
      player->score = received_score;
      printf("Updated local player's score: %d\n", player->score);
    }
  } else {
    printf("Invalid message format\n\n\n");
  }
}

void get_local_ip(struct in_addr *local_addr) {
  int sockfd;
  struct sockaddr_in addr;

  // Create a socket
  sockfd = socket(AF_INET, SOCK_DGRAM, 0);
  if (sockfd < 0) {
    perror("socket");
    exit(1);
  }

  // Set the destination address to Google's public DNS server
  memset(&addr, 0, sizeof(addr));
  addr.sin_family = AF_INET;
  addr.sin_addr.s_addr = inet_addr("8.8.8.8");
  addr.sin_port = htons(53);

  // Connect the socket to the destination address
  if (connect(sockfd, (struct sockaddr *)&addr, sizeof(addr)) < 0) {
    perror("connect");
    close(sockfd);
    exit(1);
  }

  // Get the local IP address from the connected socket
  socklen_t addrlen = sizeof(addr);
  if (getsockname(sockfd, (struct sockaddr *)&addr, &addrlen) < 0) {
    perror("getsockname");
    close(sockfd);
    exit(1);
  }

  // Close the socket
  close(sockfd);

  // Copy the local IP address to the provided structure
  *local_addr = addr.sin_addr;
}

void run_game(struct Player *player, int TCP_PORT) {

    // file pour organiser les messages entrants
    struct Queue incomingQueue;
    initializeQueue(&incomingQueue);

    // file pour organiser les messages sortants
    struct Queue outgoingQueue;
    initializeQueue(&outgoingQueue);

  int sockfd, tcpServerSocket, newSocket; //socket for sending
  int recvfd; //socket for receiving
  int valread;
  struct sockaddr_in addr, tcpServerAddr;
  char buf[100];

    char buffer[BUFFER_SIZE];
    char incomingBuffer[BUFFER_SIZE];
    char outgoingBuffer[BUFFER_SIZE];

// create tcp socket for communication with netstat
    if ((tcpServerSocket = socket(AF_INET, SOCK_STREAM, 0)) == -1) {
        perror("TCP Socket creation failed");
        exit(EXIT_FAILURE);
    }

  // Create a socket for sending
  sockfd = socket(AF_INET, SOCK_DGRAM, 0);
  if (sockfd < 0) {
    perror("socket");
    exit(1);
  }

// Set the tcp address for communication with host
    memset(&tcpServerAddr, 0, sizeof(tcpServerAddr));
    tcpServerAddr.sin_family = AF_INET;
    tcpServerAddr.sin_addr.s_addr = INADDR_ANY;
    tcpServerAddr.sin_port = htons(TCP_PORT);

  // Set the multicast address for sending
  memset(&addr, 0, sizeof(addr));
  addr.sin_family = AF_INET;
  addr.sin_addr.s_addr = inet_addr(MCAST_ADDR);
  addr.sin_port = htons(MCAST_PORT);

  // Join the multicast group for sending
  struct ip_mreq mreq;
  mreq.imr_multiaddr.s_addr = inet_addr(MCAST_ADDR);
  mreq.imr_interface.s_addr = htonl(INADDR_ANY);

  if (setsockopt(sockfd, IPPROTO_IP, IP_ADD_MEMBERSHIP, &mreq, sizeof(mreq)) < 0) {
    perror("setsockopt (send)");
    exit(1);
  }

  // Create a socket for receiving
  recvfd = socket(AF_INET, SOCK_DGRAM, 0);
  if (recvfd < 0) {
    perror("socket (recv)");
    exit(1);
  }

  // Allow reusing the address and port
    int reuse = 1;
    if (setsockopt(recvfd, SOL_SOCKET, SO_REUSEADDR, &reuse, sizeof(reuse)) < 0) {
        perror("setsockopt (recv)");
        exit(1);
    }

  // Set the multicast address for receiving
  struct sockaddr_in recv_addr;
  memset(&recv_addr, 0, sizeof(recv_addr));
  recv_addr.sin_family = AF_INET;
  recv_addr.sin_addr.s_addr = htonl(INADDR_ANY);
  recv_addr.sin_port = htons(MCAST_PORT);

// bind the tcptsocket for communication with netstat
 if (bind(tcpServerSocket, (struct sockaddr*)&tcpServerAddr, sizeof(tcpServerAddr)) == -1) {
        perror("TCP Bind failed");
        exit(EXIT_FAILURE);
    }

  // Bind the socket for receiving to the multicast address
  if (bind(recvfd, (struct sockaddr *)&recv_addr, sizeof(recv_addr)) < 0) {
    perror("bind (recv)");
    exit(1);
  }

  // Join the multicast group for receiving
  if (setsockopt(recvfd, IPPROTO_IP, IP_ADD_MEMBERSHIP, &mreq, sizeof(mreq)) < 0) {
    perror("setsockopt (recv)");
    exit(1);
  }

    // Listen for incoming TCP connections
    if (listen(tcpServerSocket, 5) == -1) {
        perror("Listen failed");
        exit(EXIT_FAILURE);
    }

  // Debugging: Print socket information
  struct in_addr local_addr;
  get_local_ip(&local_addr);
  printf("Local IP Address: %s\n", inet_ntoa(local_addr));
  printf("Multicast Group Address: %s\n", MCAST_ADDR);
  printf("Multicast Port: %d\n", MCAST_PORT);

  printf("Server listening on TCP port %d and is part of multicast group %s\n", TCP_PORT, MCAST_ADDR);

socklen_t addrlen = sizeof(tcpServerAddr);
 if ((newSocket = accept(tcpServerSocket, (struct sockaddr *)&tcpServerAddr, (socklen_t*)&addrlen)) < 0) {
                perror("Erreur lors de l'acceptation de la connexion");
                exit(EXIT_FAILURE);
            }

  // Game loop
  while (1) {
    // Create a game message
    //create_game_message(player, buf);

    // Debugging: Print the game message
    //printf("Sending: %s\n", buf);

    if ((valread = read(newSocket, buffer, sizeof(buffer))) == 0) {
                    
        printf("Client déconnecté, socket fd : %d\n", newSocket);
        close(newSocket);
        newSocket = 0;
    } else {
                    
        buffer[valread] = '\0';

        // ajouter le message entrant dans la file
        enqueue(&outgoingQueue, buffer);
        printf("receiving from netstat and Sending to multicast group: %s\n", buffer);

        strncpy(outgoingBuffer, dequeue(&outgoingQueue), BUFFER_SIZE);

        // Send the game message
        ssize_t bytes_sent = sendto(sockfd, outgoingBuffer, strlen(outgoingBuffer) + 1, 0, (struct sockaddr *)&addr, sizeof(addr));
        if (bytes_sent == -1) {
            perror("sendto");
        } else {
            printf("Sent %zd bytes\n", bytes_sent);
        }
    }
        // Receive and process messages
        struct sockaddr_in sender_addr;
        socklen_t addrlen = sizeof(sender_addr);
        ssize_t bytes_received = recvfrom(recvfd, buf, sizeof(buf), 0, (struct sockaddr *)&sender_addr, &addrlen);
        printf("Received bytes %ld\n", bytes_received);

        if (bytes_received > 0) {
            buf[bytes_received] = '\0';  // Null-terminate the received message
            
           // process_received_message(buf, player);

            // reception du message dans la queue
            enqueue(&incomingQueue, buf);
            printf("Received message from multicast - %s\n", buf);
            
            // recuperer le premier message en tete de file et le mettre dans incomingBuffer
            strncpy(incomingBuffer, dequeue(&incomingQueue), BUFFER_SIZE);

            // envoyer le message via tcp a netstat
            if (newSocket > 0) {
                send(newSocket, incomingBuffer, bytes_received, 0);
            } 
        }
    

    sleep(.5); // Send and receive messages every 1 second
  }

  // Close the sockets
  close(sockfd);
  close(recvfd);
}

int main(int argc, char *argv[]) {

  // Check if the expected number of command-line arguments is provided
    if (argc < 2) {
        fprintf(stderr, "Usage: %s <argument>\n", argv[0]);
        return 1; // Return a non-zero value to indicate an error
    }
  
  // Player information
  struct Player player;
  initialize_player(&player);

int arg_port = atoi(argv[1]);

  // Run the game
  run_game(&player, arg_port);

  return 0;
}