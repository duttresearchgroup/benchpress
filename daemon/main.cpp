#include <iostream>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <string.h>
#include "SystemAnalyser.h"
#include <memory>
using namespace std;

int main(int argc, char* argv[]){
        FILE *fp=NULL;
        pid_t process_id;
        pid_t sid;
        char freq[100];

        process_id = fork();

        if(process_id<0){
                printf("fork fail\n");
                exit(1);
        }
        else if(process_id>0){
                printf("In Parent Process \n");
                exit(0);
        }

        umask(0);

        sid = setsid();

        if(sid<0){
                exit(1);
        }

        chdir("/");

        close(STDIN_FILENO);
        close(STDOUT_FILENO);
        close(STDERR_FILENO);

        fp = fopen("log_hw.txt","w");
	auto system = make_unique<SystemAnalyser>();
        while(1){
		string s;
                fprintf(fp,"Hello World \n");
                fprintf(fp,"------\n");
		system->RunCommand("grep MHz /proc/cpuinfo");
		
		s = system->outputStore;
		const char *pStr = s.c_str();
		fprintf(fp,pStr);
                sleep(1);
                fflush(fp);
}
        fclose(fp);
        return 0;

}
                            
