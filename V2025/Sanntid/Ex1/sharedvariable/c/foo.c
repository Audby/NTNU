// Compile with `gcc foo.c -Wall -std=gnu99 -lpthread`, or use the makefile
// The executable will be named `foo` if you use the makefile, or `a.out` if you use gcc directly

#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

pthread_mutex_t lock;

int i = 0;

// øker en million ganger med 1
void* increment(void* arg) {
    for (int j = 0; j < 1000000; j++) {
        // Legger til lås på mutex for å forsikre 
        // at kun denne tråden får tilgang på variabelen
        pthread_mutex_lock(&lock); // Lock
        i++;
        pthread_mutex_unlock(&lock); //Unlock
    }
    return NULL;
}

// reduserer en million ganger med 1
void* decrement(void* arg) {
    for (int j = 0; j < 1000000; j++) {
        // Samme som for increment
        pthread_mutex_lock(&lock); // Lock
        i--;
        pthread_mutex_unlock(&lock); // Unlock 
    }
    return NULL;
}

int main(void) {
    pthread_mutex_init(&lock, NULL); // Må initialisere mutex før bruk

    pthread_t t1, t2; // Variabler for trådene

    // Opprettelse av tråder med pekere og i tillegg
    // errormelding dersom trådene ikke kunne opprettes
    if (pthread_create(&t1, NULL, increment, NULL)) {
        fprintf(stderr, "Creating t1 failed\n");
        return 1;
    }
    if (pthread_create(&t2, NULL, decrement, NULL)) {
        fprintf(stderr, "Creating t2 failed\n");
        return 1;
    }

    // Venter på at andre tråd er ferdig
    pthread_join(t1, NULL);
    pthread_join(t2, NULL);

    pthread_mutex_destroy(&lock);

    printf("The magic number is: %d\n", i);
    return 0;
}


