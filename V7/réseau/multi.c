#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <pcap.h>
#include <netinet/ip.h>
#include <netinet/if_ether.h>
#include <arpa/inet.h>
#include <unistd.h>

#define PORT 2024
#define MAX_BUFFER 1024
#define MAX_IP_COUNT 100
#define ANNOUNCEMENT_PORT 12345  // Port pour les annonces

// Structure pour stocker les informations sur les joueurs
struct PlayerInfo {
    struct in_addr ip;
    // Ajoutez d'autres informations pertinentes sur le joueur ici
};

// Structure pour stocker les adresses IP uniques
struct UniqueIPs {
    struct in_addr ips[MAX_IP_COUNT];
    int count;
};

// Fonction pour envoyer des annonces
void send_announcement(const char *interface, struct in_addr my_ip) {
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
    if (sendto(sock, &my_ip, sizeof(my_ip), 0, (struct sockaddr *)&addr, sizeof(addr)) == -1) {
        perror("sendto");
    }

    close(sock);
}

// Fonction pour vérifier si une adresse IP est une duplication
int is_duplicate(struct in_addr *ip, struct UniqueIPs *unique_ips) {
    for (int i = 0; i < unique_ips->count; i++) {
        if (ip->s_addr == unique_ips->ips[i].s_addr) {
            return 1; // Duplication trouvée
        }
    }
    return 0; // Pas de duplication trouvée
}

// Fonction pour ajouter une adresse IP unique à la liste
void add_unique_ip(struct in_addr *ip, struct UniqueIPs *unique_ips) {
    if (unique_ips->count < MAX_IP_COUNT) {
        unique_ips->ips[unique_ips->count++] = *ip;
    }
}

// Gestionnaire de paquets
void packet_handler(u_char *user_data, const struct pcap_pkthdr *pkthdr, const u_char *packet) {
    struct ether_header *eth_header = (struct ether_header *)packet;
    struct ip *ip_header = (struct ip *)(packet + sizeof(struct ether_header));

    if (ntohs(eth_header->ether_type) == ETHERTYPE_IP) {
        // Si vous détectez une annonce spéciale, ajoutez l'adresse IP à la liste des joueurs
        if (ntohs(ip_header->ip_dst.s_addr) == ANNOUNCEMENT_PORT) {
            if (!is_duplicate(&ip_header->ip_src, (struct UniqueIPs *)user_data)) {
                printf("Joueur détecté - IP : %s\n", inet_ntoa(ip_header->ip_src));
                add_unique_ip(&ip_header->ip_src, (struct UniqueIPs *)user_data);
            }
        }
    }
}

// Fonction pour capturer et imprimer les adresses IP uniques
void capture_and_print_unique_ips(const char *network_ip, const char *subnet_mask) {
    char errbuf[PCAP_ERRBUF_SIZE];
    pcap_t *handle;

    // Construire la chaîne de filtre avec l'adresse IP et le masque de sous-réseau
    char filter_exp[100];
    snprintf(filter_exp, sizeof(filter_exp), "net %s mask %s", network_ip, subnet_mask);

    // Ouvrir le périphérique de capture
    handle = pcap_open_live("any", BUFSIZ, 1, 1000, errbuf);

    if (handle == NULL) {
        fprintf(stderr, "Impossible d'ouvrir le périphérique : %s\n", errbuf);
        exit(EXIT_FAILURE);
    }

    // Compiler et définir le filtre pour capturer uniquement les paquets de la plage spécifiée
    struct bpf_program fp;
    if (pcap_compile(handle, &fp, filter_exp, 0, PCAP_NETMASK_UNKNOWN) == -1) {
        fprintf(stderr, "Impossible de compiler le filtre %s : %s\n", filter_exp, pcap_geterr(handle));
        exit(EXIT_FAILURE);
    }

    if (pcap_setfilter(handle, &fp) == -1) {
        fprintf(stderr, "Impossible d'installer le filtre %s : %s\n", filter_exp, pcap_geterr(handle));
        exit(EXIT_FAILURE);
    }

    // Utiliser une structure pour stocker les adresses IP uniques
    struct UniqueIPs unique_ips = { .count = 0 };

    // Capturer et traiter les paquets
    pcap_loop(handle, 0, packet_handler, (u_char *)&unique_ips);

    // Fermer le périphérique de capture
    pcap_close(handle);
}


// Fonction pour la boucle de découverte des joueurs
void player_discovery_loop(const char *interface, struct in_addr my_ip) {
    // Utiliser une boucle pour envoyer des annonces périodiquement
    while (1) {
        send_announcement(interface, my_ip);
        sleep(5);  // Envoyer toutes les 5 secondes par exemple
    }
}

int main() {
    // Remplacez "your_network_interface" par le nom réel de l'interface réseau
    capture_and_print_unique_ips("192.168.226.0", "255.255.255.0");

    return 0;
}


/**int main() {
    int playerSocket;
    struct sockaddr_in playerAddr;

    // Création de la socket
    playerSocket = socket(AF_INET, SOCK_STREAM, 0);

    // Configuration de l'adresse du joueur
    memset(&playerAddr, 0, sizeof(playerAddr));
    playerAddr.sin_family = AF_INET;
    playerAddr.sin_addr.s_addr = INADDR_ANY;
    playerAddr.sin_port = htons(PORT);

    // Connexion à d'autres joueurs
    connectToOtherPlayers(playerSocket, playerAddr);

    // Échange d'informations de jeu
    exchangeGameInfo(playerSocket);

    // Gestion des déconnexions et reconnexions
    handleDisconnectsAndReconnects(playerSocket, playerAddr);

    // Échange de messages de jeu
    exchangeGameMessages(playerSocket);

    // Fermeture de la socket à la fin de la partie
    close(playerSocket);

    return 0;
}**/
