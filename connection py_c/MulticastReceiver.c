#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <string.h>

#define MCAST_ADDR "224.0.0.1"
#define MCAST_PORT 8888

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


void process_received_message(const char *message, struct Player *player) {
    printf("Received: %s\n", message);

    char name[20];
    int received_score;

    // if (sscanf(message, "{\"name\":\"%19s\",\"score\":%d}", name, &received_score) == 2) {
    //     printf("Received message from %s with score: %d\n", name, received_score);

    //     if (strcmp(name, player->name) == 0) {
    //         player->score = received_score;
    //         printf("Updated local player's score: %d\n", player->score);
    //     }
    // } else {
    //     printf("Invalid message format\n");
    // }
}

void run_game(struct Player *player) {
    int recvfd;
    struct sockaddr_in recv_addr;
    char buf[100];

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
    memset(&recv_addr, 0, sizeof(recv_addr));
    recv_addr.sin_family = AF_INET;
    recv_addr.sin_addr.s_addr = htonl(INADDR_ANY);
    recv_addr.sin_port = htons(MCAST_PORT);

    // Bind the socket for receiving to the multicast address
    if (bind(recvfd, (struct sockaddr *)&recv_addr, sizeof(recv_addr)) < 0) {
        perror("bind (recv)");
        exit(1);
    }

    // Debugging: Print socket information
    printf("Multicast Group Address: %s\n", MCAST_ADDR);
    printf("Multicast Port: %d\n", MCAST_PORT);

    // Game loop
    while (1) {
        // Receive and process messages
        struct sockaddr_in sender_addr;
        socklen_t addrlen = sizeof(sender_addr);
        ssize_t bytes_received = recvfrom(recvfd, buf, sizeof(buf), 0, (struct sockaddr *)&sender_addr, &addrlen);

        if (bytes_received > 0) {
            buf[bytes_received] = '\0';  // Null-terminate the received message

            // Process the received message
            process_received_message(buf, player);
        }

        sleep(1); // Receive messages every 1 second
    }

    // Close the socket
    close(recvfd);
}

int main() {
    struct Player player;
    initialize_player(&player);

    run_game(&player);

    return 0;
}
