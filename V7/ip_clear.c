#include <stdio.h>
#include <stdlib.h>
#include <pcap.h>
#include <netinet/ip.h>
#include <netinet/if_ether.h>
#include <arpa/inet.h>
#include <sys/types.h>
#include <string.h>
#include <pthread.h>  
#include <unistd.h>   

#define MAX_IP_COUNT 100

// Structure to store unique IP addresses
struct UniqueIPs {
    struct in_addr ips[MAX_IP_COUNT];
    int count; // nbr des adresses ips qu'on a trouvé 
};

// Function to check if an IP address is a duplicate
int is_duplicate(struct in_addr *ip, struct UniqueIPs *unique_ips) {
    for (int i = 0; i < unique_ips->count; i++) {
        if (ip->s_addr == unique_ips->ips[i].s_addr) { // on charche dans la structure unique id on parcoure le count des ips 
            return 1; // Duplicate found
        }
    }
    return 0; // No duplicate found
}

// Fonction pour envoyer des annonces
/*void send_announcement(const char *network_ip, const char *subnet_mask) {
    int sock;
    struct sockaddr_in addr;

    // Créer une socket UDP
    sock = socket(AF_INET, SOCK_DGRAM, 0);
    if (sock == -1) {
        perror("socket");
        exit(EXIT_FAILURE);
    } une fonction qui permet d'identifier les personnes qui sont entrain de jouer le jeu */

// Function to add a unique IP address to the list
void add_unique_ip(struct in_addr *ip, struct UniqueIPs *unique_ips) {
    if (unique_ips->count < MAX_IP_COUNT) {  
        unique_ips->ips[unique_ips->count++] = *ip;//je rajoute l'adresse ip au tableau de la structure 
    }
}

// Function to handle captured packets
void packet_handler(u_char *user_data, const struct pcap_pkthdr *pkthdr, const u_char *packet) {
    struct ether_header *eth_header = (struct ether_header *)packet;
    struct ip *ip_header = (struct ip *)(packet + sizeof(struct ether_header));

    // Check if the Ethernet type is IP
    if (ntohs(eth_header->ether_type) == ETHERTYPE_IP) {
        // Check if the source IP address is in the specified subnet
        const char *subnet = (const char *)user_data;
        if (strncmp(subnet, inet_ntoa(ip_header->ip_src), strlen(subnet)) == 0) {
            // Check if the IP address is not a duplicate
            if (!is_duplicate(&ip_header->ip_src, (struct UniqueIPs *)(user_data + strlen(subnet) + 1))) {
                // Print or save the IP address if it is unique and add it to the list
                printf("IP Address: %s\n", inet_ntoa(ip_header->ip_src));
                fflush(stdout);
                add_unique_ip(&ip_header->ip_src, (struct UniqueIPs *)(user_data + strlen(subnet) + 1));
            }
        }
    }
}

// Thread function for capturing packets on a specific interface
void *capture_thread(void *arg) {
    char errbuf[PCAP_ERRBUF_SIZE];
    pcap_t *handle;
    const char *interface = (const char *)arg;

    // Open the capture device in real-time mode for the specified interface
    handle = pcap_open_live(interface, BUFSIZ, 1, 1000, errbuf);

    if (handle == NULL) {
        fprintf(stderr, "Could not open device %s: %s\n", interface, errbuf);
        pthread_exit(NULL);
    }

    // Use a structure to store unique IP addresses for each interface
    struct UniqueIPs unique_ips = { .count = 0 };

    // Pass subnet information to the packet handler
    const char *subnet = "192.168.226.";  // Modify this as needed
    u_char user_data[sizeof(subnet) + sizeof(struct UniqueIPs)] = {0};
    strcpy((char *)user_data, subnet);

    // Loop for capturing and processing packets on the current interface
    pcap_loop(handle, 0, packet_handler, user_data);

    // Close the capture device for the current interface
    pcap_close(handle);

    pthread_exit(NULL);
}

// Main function to capture and print or save unique IP addresses in a specified subnet
void capture_and_print_subnet(const char *subnet) {
    char errbuf[PCAP_ERRBUF_SIZE];

    // Get a list of available interfaces
    pcap_if_t *alldevs;
    if (pcap_findalldevs(&alldevs, errbuf) == -1) {
        fprintf(stderr, "Error in pcap_findalldevs: %s\n", errbuf);
        exit(EXIT_FAILURE);
    }

    // Create a thread for each interface
    pthread_t threads[32];
    int thread_count = 0;

    for (pcap_if_t *dev = alldevs; dev != NULL; dev = dev->next) {
        // Create a thread for the current interface
        if (pthread_create(&threads[thread_count], NULL, capture_thread, (void *)dev->name) != 0) {
            fprintf(stderr, "Error creating thread for interface %s\n", dev->name);
            continue;  // Try the next interface
        }

        thread_count++;

        // Add a delay between thread creations to avoid issues with resource constraints.
        usleep(10000);
    }

    // Wait for all threads to finish
    for (int i = 0; i < thread_count; i++) {
        pthread_join(threads[i], NULL);
    }

    // Don't forget to free the list of interfaces when done
    pcap_freealldevs(alldevs);
}

// Main function of the program
int main() {
    // Call the function to capture and print or save IP addresses in the specified subnet
    const char *subnet = "192.168.226.";
    capture_and_print_subnet(subnet);
    return 0;
}
