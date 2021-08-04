#ifndef _SYSTEM_ANALYSER_H
#define _SYSTEM_ANALYSER_H

#include <string>
using namespace std;
class SystemAnalyser{
public:
        SystemAnalyser();
        virtual void RunCommand(const char* command);
        virtual void Display();
        virtual ~SystemAnalyser();
        virtual void  StoreOutput(string result);
        std::string outputStore;

};

#endif

