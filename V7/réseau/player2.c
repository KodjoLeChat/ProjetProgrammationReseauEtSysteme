#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <arpa/inet.h>
#include <unistd.h>

#define MAX_IP_COUNT 100
#define ANNOUNCEMENT_PORT 12345  // Port pour les annonces

// Structure pour stocker les adresses IP uniques
struct UniqueIPs {
    struct in_addr ips[MAX_IP_COUNT];
    int count;
};

// Fonction pour envoyer des annonces
void send_announcement(const char *network_ip, const char *subnet_mask) {
    int sock;
    struct sockaddr_in addr;

    // Créer une socket UDP
    sock = socket(AF_INET, SOCK_DGRAM, 0);
    if (sock == -1) {
        perror("socket");
        exit(EXIT_FAILURE);
    }

    // Configurer l'adresse pour l'envoi broadcast
    memset(&addr, 0, sizeof(addr));
    addr.sin_family = AF_INET;
    addr.sin_port = htons(ANNOUNCEMENT_PORT);
    addr.sin_addr.s_addr = htonl(INADDR_BROADCAST);  // Envoyer en broadcast

    // Envoyer l'annonce
    if (sendto(sock, network_ip, strlen(network_ip), 0, (struct sockaddr *)&addr, sizeof(addr)) == -1) {
        perror("sendto");
    }

    close(sock);
}

// Fonction pour vérifier si une adresse IP est une duplication
int is_duplicate(const char *ip, struct UniqueIPs *unique_ips) {
    for (int i = 0; i < unique_ips->count; i++) {
        if (strcmp(ip, inet_ntoa(unique_ips->ips[i])) == 0) {
            return 1; // Duplication trouvée
        }
    }
    return 0; // Pas de duplication trouvée
}

// Fonction pour ajouter une adresse IP unique à la liste
void add_unique_ip(const char *ip, struct UniqueIPs *unique_ips) {
    if (unique_ips->count < MAX_IP_COUNT) {
        inet_pton(AF_INET, ip, &unique_ips->ips[unique_ips->count]);
        unique_ips->count++;
    }
}

// Fonction pour la boucle de découverte des joueurs
void player_discovery_loop(const char *network_ip, const char *subnet_mask) {
    // Utiliser une boucle pour envoyer des annonces périodiquement
    struct UniqueIPs unique_ips = { .count = 0 };

    while (1) {
        send_announcement(network_ip, subnet_mask);
        sleep(5);  // Envoyer toutes les 5 secondes par exemple
    }
}

int main() {
    // Remplacez "192.168.226.0" par la plage d'adresses IP de votre choix
    const char *network_ip = "192.168.226.0";
    const char *subnet_mask = "255.255.255.0";

    // Lancez la boucle de découverte des joueurs dans un thread ou un processus séparé
    // Vous pouvez également lancer cette boucle dans un autre programme sur un autre ordinateur
    player_discovery_loop(network_ip, subnet_mask);

    return 0;
}
