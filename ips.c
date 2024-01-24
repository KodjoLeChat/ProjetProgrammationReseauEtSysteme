#include <stdio.h>
#include <stdlib.h>
#include <pcap.h>
#include <netinet/ip.h>
#include <netinet/if_ether.h>
#include <arpa/inet.h>
#include <sys/types.h>
#include <string.h>

#define MAX_IP_COUNT 100
#define IP_Filter "192.168.226."

// Structure to store unique IP addresses
struct UniqueIPs {
    struct in_addr ips[MAX_IP_COUNT];
    int count;
};

// Function to check if an IP address is a duplicate
int is_duplicate(struct in_addr *ip, struct UniqueIPs *unique_ips) {
    for (int i = 0; i < unique_ips->count; i++) {
        if (ip->s_addr == unique_ips->ips[i].s_addr) {
            return 1; // Duplicate found
        }
    }
    return 0; // No duplicate found
}

// Function to add a unique IP address to the list
void add_unique_ip(struct in_addr *ip, struct UniqueIPs *unique_ips) {
    if (unique_ips->count < MAX_IP_COUNT) {
        unique_ips->ips[unique_ips->count++] = *ip;
    }
}

// Function to handle captured packets
void packet_handler(u_char *user_data, const struct pcap_pkthdr *pkthdr, const u_char *packet) {
    struct ether_header *eth_header = (struct ether_header *)packet;
    struct ip *ip_header = (struct ip *)(packet + sizeof(struct ether_header));

    // Check if the Ethernet type is IP
    if (ntohs(eth_header->ether_type) == ETHERTYPE_IP) {
        // Check if the source IP address starts with IP_Filter
        if (strncmp(IP_Filter, inet_ntoa(ip_header->ip_src), strlen(IP_Filter)) == 0) {
            // Check if the IP address is not a duplicate
            if (!is_duplicate(&ip_header->ip_src, (struct UniqueIPs *)user_data)) {
                // Print or save the IP address if it is unique and add it to the list
                printf("IP Address: %s\n", inet_ntoa(ip_header->ip_src));
                add_unique_ip(&ip_header->ip_src, (struct UniqueIPs *)user_data);
            }
        }
    }
}

// Main function to capture and print or save unique IP addresses in a specified subnet
void capture_and_print_subnet(const char *interface) {
    char errbuf[PCAP_ERRBUF_SIZE];
    pcap_t *handle;

    // Open the capture device in real-time mode
    handle = pcap_open_live(interface, BUFSIZ, 1, 1000, errbuf);

    if (handle == NULL) {
        fprintf(stderr, "Could not open device %s: %s\n", interface, errbuf);
        exit(EXIT_FAILURE);
    }

    // Use a structure to store unique IP addresses
    struct UniqueIPs unique_ips = { .count = 0 };

    // Loop for capturing and processing packets
    pcap_loop(handle, 0, packet_handler, (u_char *)&unique_ips);

    // Close the capture device
    pcap_close(handle);
}

// Main function of the program
int main() {
    // Call the function to capture and print or save IP addresses in the specified subnet
    capture_and_print_subnet("vmnet8");
    return 0;
}
