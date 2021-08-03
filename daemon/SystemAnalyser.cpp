#include "SystemAnalyser.h"
#include <memory>
#include <iostream>
using namespace std;

SystemAnalyser::SystemAnalyser(){
}

void SystemAnalyser::RunCommand(const char* command){
        array<char,128> buffer;
        string result;

        unique_ptr<FILE,decltype(&pclose)> pipe(popen(command,"r"), pclose);
        if(!pipe){
                throw runtime_error("popen() failed");
        }
        while(fgets(buffer.data(), buffer.size(), pipe.get()) != nullptr){
                result += buffer.data();
        }

        StoreOutput(result);
}

void SystemAnalyser::StoreOutput(string result){
        outputStore = result;

}


void SystemAnalyser::Display(){
        cout << outputStore << endl;
}

SystemAnalyser::~SystemAnalyser(){
}
           
