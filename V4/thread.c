#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <arpa/inet.h>
#include <ifaddrs.h>
#include <unistd.h>
#include <pthread.h>
#include <time.h>

// Structure pour représenter une adresse IP
typedef struct IPAddress {
    char address[INET_ADDRSTRLEN];
    struct IPAddress* next;
} IPAddress;

// Structure représentant les données du jeu
typedef struct {
    int joueur_id;           // Identifiant du joueur
    char playerAddress[INET_ADDRSTRLEN];  // Adresse IP du joueur
    // Ajoutez d'autres données du jeu ici
} GameData;

// Fonction pour ajouter une adresse IP à la liste
IPAddress* addIPAddress(IPAddress* list, const char* address) {
    IPAddress* newNode = (IPAddress*)malloc(sizeof(IPAddress));
    if (!newNode) {
        perror("Allocation de mémoire a échoué");
        exit(EXIT_FAILURE);
    }

    strcpy(newNode->address, address);
    newNode->next = list;

    return newNode;
}

// Fonction pour afficher toutes les adresses IP dans la liste
void printIPAddresses(IPAddress* list) {
    printf("Liste des adresses IP sur le LAN :\n");
    while (list != NULL) {
        printf("%s\n", list->address);
        list = list->next;
    }
}

// Fonction pour récupérer les adresses IP sur le LAN et les stocker dans la liste
IPAddress* getLocalIPAddresses(IPAddress* list) {
    struct ifaddrs *ifap, *ifa;

    if (getifaddrs(&ifap) == -1) {
        perror("Erreur lors de la récupération des interfaces");
        exit(EXIT_FAILURE);
    }

    for (ifa = ifap; ifa != NULL; ifa = ifa->ifa_next) {
        if (ifa->ifa_addr != NULL && (ifa->ifa_addr->sa_family == AF_INET || ifa->ifa_addr->sa_family == AF_INET6)) {
            char ipAddr[INET_ADDRSTRLEN];
            void *addr;

            if (ifa->ifa_addr->sa_family == AF_INET) {
                addr = &((struct sockaddr_in *)ifa->ifa_addr)->sin_addr;
            } else {
                addr = &((struct sockaddr_in6 *)ifa->ifa_addr)->sin6_addr;
            }

            inet_ntop(ifa->ifa_addr->sa_family, addr, ipAddr, INET_ADDRSTRLEN);

            // Ajouter l'adresse IP à la liste
            list = addIPAddress(list, ipAddr);

            // Afficher le nom de l'interface
            printf("Nom de l'interface : %s\n", ifa->ifa_name);
        }
    }

    freeifaddrs(ifap);

    return list;
}

// Fonction pour envoyer des données du jeu à chaque joueur du LAN sauf soi-même
void sendGameDataToOthers(const GameData* gameData, const IPAddress* playerAddressList, int port) {
    int sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    if (sock == -1) {
        perror("Erreur lors de la création de la socket UDP");
        exit(EXIT_FAILURE);
    }

    struct sockaddr_in destAddr;
    memset(&destAddr, 0, sizeof(destAddr));
    destAddr.sin_family = AF_INET;
    destAddr.sin_port = htons(port);

    while (playerAddressList != NULL) {
        // Vérifier si l'adresse IP est différente de celle du joueur actuel
        if (strcmp(playerAddressList->address, gameData->playerAddress) != 0) {
            if (inet_pton(AF_INET, playerAddressList->address, &(destAddr.sin_addr)) <= 0) {
                perror("Erreur lors de la conversion de l'adresse IP");
                close(sock);
                exit(EXIT_FAILURE);
            }

            // Envoyer les données du jeu à l'adresse IP du joueur
            if (sendto(sock, gameData, sizeof(GameData), 0, (struct sockaddr*)&destAddr, sizeof(destAddr)) == -1) {
                perror("Erreur lors de l'envoi des données du jeu");
            }
        }

        playerAddressList = playerAddressList->next;
    }

    close(sock);
}

#include <time.h>

// Fonction pour attendre un court laps de temps (en millisecondes)
void wait(int milliseconds) {
    clock_t start_time = clock();
    while (clock() < start_time + milliseconds * CLOCKS_PER_SEC / 1000);
}

// Fonction pour recevoir des données du jeu
void receiveGameData(int port) {
    int sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    if (sock == -1) {
        perror("Erreur lors de la création de la socket UDP");
        exit(EXIT_FAILURE);
    }

    // Activer l'option SO_REUSEADDR
    int reuse = 1;
    if (setsockopt(sock, SOL_SOCKET, SO_REUSEADDR, &reuse, sizeof(reuse)) < 0) {
        perror("Erreur lors de la configuration de l'option SO_REUSEADDR");
        close(sock);
        exit(EXIT_FAILURE);
    }

    struct sockaddr_in serverAddr;
    memset(&serverAddr, 0, sizeof(serverAddr));
    serverAddr.sin_family = AF_INET;
    serverAddr.sin_port = htons(port);
    serverAddr.sin_addr.s_addr = INADDR_ANY;

    // Tentatives de liaison avec une pause entre chaque tentative
    int max_attempts = 5;  // Nombre maximal de tentatives
    int attempt_interval = 500;  // Intervalle entre les tentatives en millisecondes

    for (int attempt = 0; attempt < max_attempts; ++attempt) {
        if (bind(sock, (struct sockaddr*)&serverAddr, sizeof(serverAddr)) == 0) {
            // La liaison a réussi
            break;
        } else {
            perror("Erreur lors de la liaison de la socket");
            if (attempt < max_attempts - 1) {
                printf("Nouvelle tentative dans %d millisecondes...\n", attempt_interval);
                wait(attempt_interval);
            } else {
                // Si toutes les tentatives ont échoué, quitter le programme
                close(sock);
                exit(EXIT_FAILURE);
            }
        }
    }

    // Boucle pour recevoir continuellement des données du jeu
    while (1) {
        GameData receivedGameData;
        struct sockaddr_in senderAddr;
        socklen_t senderAddrLen = sizeof(senderAddr);

        ssize_t bytesReceived = recvfrom(sock, &receivedGameData, sizeof(GameData), 0,
                                         (struct sockaddr*)&senderAddr, &senderAddrLen);
        if (bytesReceived == -1) {
            perror("Erreur lors de la réception des données du jeu");
        } else {
            // Traiter les données du jeu reçues (par exemple, afficher l'identifiant du joueur)
            printf("Données reçues du joueur %d\n", receivedGameData.joueur_id);
        }
    }

    close(sock);
}



// Fonction pour le comportement du joueur dans un thread
// Fonction pour le comportement du joueur dans un thread
void* joueurThread(void* arg) {
    GameData* gameData = (GameData*)arg;

    // Logique du joueur ici
    // Utilisez gameData->joueur_id et gameData->playerAddress pour le joueur actuel
    printf("Thread du joueur %d démarré\n", gameData->joueur_id);
    
    // Exemple : Attendre un certain temps
    sleep(2);

    // Envoyer des données de test
    printf("Joueur %d envoie des données de test à tous les joueurs\n", gameData->joueur_id);
    GameData testGameData;
    testGameData.joueur_id = gameData->joueur_id;
    strcpy(testGameData.playerAddress, gameData->playerAddress);
    // Ajoutez d'autres données de test ici

    sendGameDataToOthers(&testGameData, NULL, 8881); // Le troisième paramètre doit être le port correct

    // Attendre un court moment pour laisser le temps aux autres joueurs d'envoyer leurs données
    sleep(1);

    // Recevoir des données de test
    printf("Joueur %d attend des données de test\n", gameData->joueur_id);
    // Vous pouvez traiter les données reçues ici, par exemple, afficher le contenu
    receiveGameData(8881); // Le paramètre doit être le port correct

    // Libérer la mémoire allouée pour les données du joueur
    free(gameData);

    return NULL;
}


int main() {
    IPAddress* addressList = NULL;

    // Récupérer et stocker les adresses IP sur le LAN
    addressList = getLocalIPAddresses(addressList);

    // Afficher les adresses IP
    printIPAddresses(addressList);

    // Envoyer et recevoir des données du jeu
    int port = 8880; // Port à utiliser pour la communication UDP


    int nombreDeJoueurs = 3;  // Spécifiez le nombre de joueurs souhaité
    pthread_t joueursThreads[nombreDeJoueurs];

    for (int i = 0; i < nombreDeJoueurs; ++i) {
        // Créer une copie des données du jeu pour chaque joueur
        GameData* joueurData = malloc(sizeof(GameData));
        joueurData->joueur_id = i + 1;  // Ajustez l'identifiant du joueur
        if (addressList != NULL) {
            strcpy(joueurData->playerAddress, addressList->address);
            addressList = addressList->next;
        }

        // Créer et lancer un thread pour le joueur
        if (pthread_create(&joueursThreads[i], NULL, joueurThread, (void*)joueurData) != 0) {
            perror("Erreur lors de la création du thread joueur");
            exit(EXIT_FAILURE);
        }
    }

    // Attendre la fin de tous les threads
    for (int i = 0; i < nombreDeJoueurs; ++i) {
        if (pthread_join(joueursThreads[i], NULL) != 0) {
            perror("Erreur lors de l'attente du thread joueur");
            exit(EXIT_FAILURE);
        }
    }

    // Lancer la réception des données du jeu en arrière-plan
    // (Note : Cette fonction est bloquante, il est recommandé de la lancer dans un thread séparé)
    receiveGameData(port);
    //port+=1;

    // Libérer la mémoire allouée pour les adresses IP
    while (addressList != NULL) {
        IPAddress* temp = addressList;
        addressList = addressList->next;
        free(temp);
    }

    return 0;
}
