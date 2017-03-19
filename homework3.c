#include<stdio.h>
#include<time.h>
#include<unistd.h>
#include<signal.h>
#include<stdlib.h>
#include<linux/inotify.h>

void init_Daemon(void);
int main(){
    init_Daemon();
    int fd;
    fd = inotify_init();
    if(fd < 0){
        printf("inotify_init error.");
        exit(1);
    }
    wd = inotify_add_watch(fd, "/proc", IN_MODIFY | IN_CREATE | IN_DELETE);
}
void init_Daemon(void){
    pid_t child1;
    int i;
    child1 = fork();
    if(child1 < 0){
        printf("create process failed.");
        exit(1);
    }
    else if(child1 > 0){
        exit(0);
    }
}
