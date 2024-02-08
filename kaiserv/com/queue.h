#include <stdio.h>
#include <stdlib.h>

// Définition de la structure pour un élément de la file
struct Node {
    char* data;
    struct Node* next;
};

// Définition de la structure pour la file
struct Queue {
    struct Node* front; // pointe vers l'avant de la file
    struct Node* rear;  // pointe vers l'arrière de la file
};

// Fonction pour initialiser une file vide
void initializeQueue(struct Queue* queue) ;

// Fonction pour vérifier si la file est vide
int isEmpty(struct Queue* queue) ;

// Fonction pour ajouter un élément à la file
void enqueue(struct Queue* queue, char* value) ;

// Fonction pour retirer un élément de la file
char* dequeue(struct Queue* queue) ;

// Fonction pour afficher les éléments de la file
void displayQueue(struct Queue* queue) ;
