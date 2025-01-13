// Compile with `gcc foo.c -Wall -std=gnu99 -lpthread`, or use the makefile
// The executable will be named `foo` if you use the makefile, or `a.out` if you use gcc directly

#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

pthread_mutex_t lock;

int i = 0;

void* increment(void* arg) {
    for (int j = 0; j < 1000000; j++) {
        pthread_mutex_lock(&lock);
        i++;
        pthread_mutex_unlock(&lock); 
    }
    return NULL;
}

void* decrement(void* arg) {
    for (int j = 0; j < 1000000; j++) {
        pthread_mutex_lock(&lock);
        i--;
        pthread_mutex_unlock(&lock);  
    }
    return NULL;
}

int main(void) {
    pthread_mutex_init(&lock, NULL);

    pthread_t t1, t2;

    if (pthread_create(&t1, NULL, increment, NULL)) {
        fprintf(stderr, "Error creating thread\n");
        return 1;
    }
    if (pthread_create(&t2, NULL, decrement, NULL)) {
        fprintf(stderr, "Error creating thread\n");
        return 1;
    }

    pthread_join(t1, NULL);
    pthread_join(t2, NULL);

    pthread_mutex_destroy(&lock);

    printf("The magic number is: %d\n", i);
    return 0;
}


