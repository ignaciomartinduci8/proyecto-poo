//
// Created by Usuario on 23/10/2023.
//

#ifndef PROYECTO_SERVIDOR_H
#define PROYECTO_SERVIDOR_H

#include <iostream>
#include <stdlib.h>
#include <windows.h>
#include <string>
using namespace std;
#include "./RPCfiles/XmlRpc.h"
using namespace XmlRpc;


class Servidor {

private:

    string IP;
    int PORT;

public:

    Servidor(string IP, int port);

    void connect();

};


#endif //PROYECTO_SERVIDOR_H
