//
// Created by Usuario on 23/10/2023.
//

#include "Cliente.h"

void Cliente::connect() {

    try {

        this->client = new XmlRpcClient(this->IP.c_str(), this->PORT, nullptr);

        XmlRpcValue noArgs, result;

        if(this->client->execute("system.listMethods", noArgs, result)) {

            for(int i = 0; i < result.size(); i++){

                this->methods.push_back(result[i]);

            }

        }else{

            cerr << RED << "-->" << RESET << " Error al obtener los metodos" << endl;

        }

    }catch (const XmlRpc::XmlRpcException& e) {

        cerr << RED << "-->" << RESET << " Error al conectar: " << e.getMessage() << endl;

    }


}

Cliente::Cliente(string IP, int PORT) {

    this->IP = IP;
    this->PORT = PORT;

    this->connect();

}

vector<string> Cliente::getMethods() {

    return this->methods;

}

void Cliente::executeMethod(std::string method, vector <std::string> outParams) {

    XmlRpcValue noArgs, result;

    char *cstr = new char[method.length() + 1];

    this->client->execute("connect", noArgs, result);

    cout << BLUE << "-->" << RESET << " Resultado: " << result << endl;

}

