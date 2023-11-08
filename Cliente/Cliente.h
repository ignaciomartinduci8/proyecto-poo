//
// Created by Usuario on 23/10/2023.
//

#ifndef PROYECTO_CLIENTE_H
#define PROYECTO_CLIENTE_H

#include <iostream>
#include <stdlib.h>
#include <windows.h>
#include <string>
using namespace std;
#include "./RPCfiles/XmlRpc.h"
using namespace XmlRpc;


class Cliente {

private:

    string IP;
    int PORT;

public:

    Cliente(string IP, int port);

    void connect();

};


#endif //PROYECTO_CLIENTE_H
