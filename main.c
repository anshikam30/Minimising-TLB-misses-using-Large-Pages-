#include "work.h"
#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <fcntl.h>
#include <unistd.h>
#define PAGE_SIZE (2 * 1024 * 1024) // 2 MiB
#define MAX_PAGES 8 // Maximum number of large pages
void allocate_large_pages(int num_pages, long base_addresses[]) {
    for (int i = 0; i < num_pages; i++) {
        // Map the memory for each base address using mmap
        void *addr = mmap((void*)base_addresses[i], PAGE_SIZE,
                          PROT_READ | PROT_WRITE,
                          MAP_PRIVATE | MAP_ANONYMOUS | MAP_FIXED| MAP_HUGETLB,
                          -1, 0);
        if (addr == MAP_FAILED) {
            perror("mmap failed");
            exit(EXIT_FAILURE);
        }
    }
}
int main(int argc, char *argv[]) {
  if (argc != 2) {
    fprintf(stderr, "Usage: main 24095 \n");
    return EXIT_FAILURE;
  }
  work_init(atoi(argv[1]));
    // Read large page addresses from largepages.txt
    long base_addresses[MAX_PAGES];
    int n = 0; // Variable to hold the number of large pages to use

    // Open the file containing large page addresses
    FILE *file = fopen("largepages.txt", "r");
    if (!file) {
        perror("Could not open largepages.txt");
        return EXIT_FAILURE;
    }

    // Read addresses from the file
    while (fscanf(file, "%ld", &base_addresses[n]) == 1 && n < MAX_PAGES) {
        n++;
    }
    fclose(file);

    // Allocate large pages using the read addresses
    allocate_large_pages(n, base_addresses);

  
  if (work_run() == 0) {
    printf("Work completed successfully\n");
  }

  return 0;
}
