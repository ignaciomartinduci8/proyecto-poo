//
// Created by Usuario on 23/10/2023.
//

#ifndef PROYECTO_CLIENTE_H
#define PROYECTO_CLIENTE_H

#define RESET   "\033[0m"
#define RED     "\033[1;31m"
#define BLUE    "\033[1;34m"
#define IDENT   ">         "

#include <iostream>
#include <stdlib.h>
#include <vector>
#include <windows.h>
#include <string>
using namespace std;
#include "./RPCfiles/XmlRpc.h"
using namespace XmlRpc;


class Cliente {

private:

    string IP;
    int PORT;
    string USER;
    vector<string> methods;
    XmlRpcClient *client;

public:

    Cliente(string IP, int port);

    void connect();

    vector<string> getMethods();

    void executeMethod(string method, vector<string> params);

};


#endif //PROYECTO_CLIENTE_H
