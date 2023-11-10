//
// Created by Usuario on 09/11/2023.
//

#ifndef PROYECTO_CLI_H
#define PROYECTO_CLI_H


#include "./RPCfiles/XmlRpc.h"
using namespace XmlRpc;
#include <iostream>
#include <string>
#include <iomanip>
#include <vector>

//definir colores
#define RESET   "\033[0m"
#define RED     "\033[31m"
#define GREEN   "\033[32m"
#define BLUE    "\033[34m"

class CLI {

private:

    bool isConnected = false;
    std::string username;
    int port;
    std::string ip;
    XmlRpcClient* client = nullptr;
    std::vector<std::string> methods;

public:

    CLI();

    void waitUsername();

    void waitConnection();

    bool connectToServer();

    void programLoop();

    void printMethods();

    void commandController(std::string command);

};


#endif //PROYECTO_CLI_H
