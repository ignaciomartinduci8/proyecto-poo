//
// Created by Usuario on 23/10/2023.
//

#ifndef PROYECTO_CLI_H
#define PROYECTO_CLI_H
#include <iostream>
#include <string>
#include <vector>
using namespace std;

class CLI {

private:

    bool isConnected = false;
    string IP;
    int PORT;


public:

    CLI();
    void loop();




};


#endif //PROYECTO_CLI_H
