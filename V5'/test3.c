#include <stdio.h>
#include <stdlib.h>
#include <pcap.h>
#include <netinet/ip.h>
#include <netinet/if_ether.h>
#include <arpa/inet.h>
#include <sys/types.h>

#define MAX_IP_COUNT 100

struct UniqueIPs {
    struct in_addr ips[MAX_IP_COUNT];
    int count;
};


// Fonction pour vérifier si une adresse IP est en double
// Retourne 1 si l'adresse IP est en double, sinon 0
int is_duplicate(struct in_addr *ip, struct UniqueIPs *unique_ips) {
    for (int i = 0; i < unique_ips->count; i++) {
        if (ip->s_addr == unique_ips->ips[i].s_addr) {
            return 1; // Doublon trouvé
        }
    }
    return 0; // Aucun doublon trouvé
}

// Fonction pour ajouter une adresse IP unique à la liste
void add_unique_ip(struct in_addr *ip, struct UniqueIPs *unique_ips) {
    if (unique_ips->count < MAX_IP_COUNT) {
        unique_ips->ips[unique_ips->count++] = *ip;
    }
}

// Fonction de gestion des paquets capturés
// Extrait l'en-tête Ethernet et l'en-tête IP du paquet
// Vérifie si l'adresse IP source appartient au sous-réseau spécifié
// Imprime l'adresse IP si elle est unique dans la liste
void packet_handler(u_char *user_data, const struct pcap_pkthdr *pkthdr, const u_char *packet) {
    struct ether_header *eth_header = (struct ether_header *)packet;
    struct ip *ip_header = (struct ip *)(packet + sizeof(struct ether_header));

    // Vérifie si le type Ethernet est IP
    if (ntohs(eth_header->ether_type) == ETHERTYPE_IP) {
        // Vérifie si l'adresse IP source n'est pas en double
        if (!is_duplicate(&ip_header->ip_src, (struct UniqueIPs *)user_data)) {
            // Imprime l'adresse IP si elle est unique et l'ajoute à la liste
            printf("Adresse IP : %s\n", inet_ntoa(ip_header->ip_src));
            add_unique_ip(&ip_header->ip_src, (struct UniqueIPs *)user_data);
        }
    }
}

// Fonction principale pour capturer et imprimer les adresses IP uniques dans un sous-réseau spécifié
// Ouvre le périphérique de capture en temps réel
// Compile et applique le filtre pour capturer uniquement les paquets du sous-réseau spécifié
// Utilise une structure pour stocker les adresses IP uniques
// Boucle de capture et traitement des paquets
// Ferme le périphérique de capture à la fin

// Fonction principale pour capturer et imprimer les adresses IP uniques dans un sous-réseau spécifié
void capture_and_print_subnet(const char *interface, const char *subnet) {
    char errbuf[PCAP_ERRBUF_SIZE];
    pcap_t *handle;

    // Ouvre le périphérique de capture en temps réel
    handle = pcap_open_live(interface, BUFSIZ, 1, 1000, errbuf);

    if (handle == NULL) {
        fprintf(stderr, "Impossible d'ouvrir le périphérique %s : %s\n", interface, errbuf);
        exit(EXIT_FAILURE);
    }

    // Compile et applique le filtre pour capturer uniquement les paquets du sous-réseau spécifié
    struct bpf_program fp;
    char filter_exp[256];
    snprintf(filter_exp, sizeof(filter_exp), "net %s", subnet);

    if (pcap_compile(handle, &fp, filter_exp, 0, PCAP_NETMASK_UNKNOWN) == -1) {
        fprintf(stderr, "Impossible de compiler le filtre %s : %s\n", filter_exp, pcap_geterr(handle));
        exit(EXIT_FAILURE);
    }

    if (pcap_setfilter(handle, &fp) == -1) {
        fprintf(stderr, "Impossible d'appliquer le filtre %s : %s\n", filter_exp, pcap_geterr(handle));
        exit(EXIT_FAILURE);
    }

    // Utilise une structure pour stocker les adresses IP uniques
    struct UniqueIPs unique_ips = { .count = 0 };

    // Boucle de capture et traitement des paquets
    pcap_loop(handle, 0, packet_handler, (u_char *)&unique_ips);

    // Ferme le périphérique de capture
    pcap_close(handle);
}

int main() {
    // Replace "your_network_interface" with the actual network interface name
    capture_and_print_subnet("enp0s3", "10.0.2.0/24");
    return 0;
}



