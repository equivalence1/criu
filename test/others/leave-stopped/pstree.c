#include <stdio.h>
#include <limits.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>
#include <pthread.h>
#include <sys/stat.h>
#include <sys/types.h>

const size_t THREADS_N = 3;
const size_t TREE_HEIGHT = 3;

static void *hang(void *arg)
{
	(void)arg;
	while (1)
		sleep(UINT_MAX);
}

static void create_threads(void)
{
	for (size_t i = 1; i < THREADS_N; i++) {
		pthread_t thread;
		pthread_create(&thread, NULL, hang, NULL);
	}
}

int main(void)
{
	/**
	 * just building full binary tree of processes
	 */
	for (size_t i = 1; i < TREE_HEIGHT; i++) {
		if (fork()) {
			if (fork())
				break;
		}
	}

	create_threads();

	hang(NULL);
}
