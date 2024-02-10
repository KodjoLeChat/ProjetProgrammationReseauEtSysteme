#include <stdio.h>
#include <stdlib.h>
#include "queue.h"

// Définition de la structure pour un élément de la file
/*struct Node {
    int data;
    struct Node* next;
};

// Définition de la structure pour la file
struct Queue {
    struct Node* front; // pointe vers l'avant de la file
    struct Node* rear;  // pointe vers l'arrière de la file
};*/

/*int main() {
    struct Queue myQueue;
    initializeQueue(&myQueue);

    enqueue(&myQueue, "number 70");
    enqueue(&myQueue, "number 10");
    enqueue(&myQueue, "number 20");
    enqueue(&myQueue, "number 30");
    enqueue(&myQueue, "number 40");
    enqueue(&myQueue, "number 50");

    printf("File d'attente : ");
    displayQueue(&myQueue);

    printf("Elément retiré : %s\n", dequeue(&myQueue));
    printf("Elément retiré : %s\n", dequeue(&myQueue));
    printf("Elément retiré : %s\n", dequeue(&myQueue));

    printf("File d'attente après retrait : ");
    displayQueue(&myQueue);

    return 0;
}*/

// Fonction pour initialiser une file vide
void initializeQueue(struct Queue* queue) {
    queue->front = queue->rear = NULL;
}

// Fonction pour vérifier si la file est vide
int isEmpty(struct Queue* queue) {
    return queue->front == NULL;
}

// Fonction pour ajouter un élément à la file
void enqueue(struct Queue* queue, char* value) {
    struct Node* newNode = (struct Node*)malloc(sizeof(struct Node));
    if (!newNode) {
        fprintf(stderr, "Erreur d'allocation mémoire\n");
        exit(EXIT_FAILURE);
    }

    newNode->data = value;
    newNode->next = NULL;

    if (isEmpty(queue)) {
        queue->front = queue->rear = newNode;
    } else {
        queue->rear->next = newNode;
        queue->rear = newNode;
    }
}

// Fonction pour retirer un élément de la file
char* dequeue(struct Queue* queue) {
    if (isEmpty(queue)) {
        fprintf(stderr, "La file est vide\n");
        exit(EXIT_FAILURE);
    }

    struct Node* temp = queue->front;
    char* value = temp->data;

    queue->front = temp->next;
    free(temp);

    if (queue->front == NULL) {
        queue->rear = NULL;
    }

    return value;
}

// Fonction pour afficher les éléments de la file
void displayQueue(struct Queue* queue) {
    if (isEmpty(queue)) {
        printf("La file est vide\n");
        return;
    }

    struct Node* current = queue->front;
    while (current != NULL) {
        printf("%s ", current->data);
        current = current->next;
    }
    printf("\n");
}


