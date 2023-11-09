//
// Created by Usuario on 09/11/2023.
//

#include "CLI.h"

CLI::CLI() {

    std::cout << BLUE << "===============================================================\n" << RESET << std::endl;
    std::cout << "Iniciando cliente de srvicio RPC" << std::endl;
    std::cout << BLUE << "===============================================================\n" << RESET << std::endl;

    this->waitUsername();
}

void CLI::waitUsername() {

    std::cout << BLUE << "-->" << "Ingrese su nombre de usuario: ";
    std::cin >> this->username;

}

void CLI::waitConnection() {

    while(!this->isConnected) {

        std::cout << BLUE << "-->" << "Ingrese la IP del servidor: ";
        std::cin >> this->ip;
        std::cout << BLUE << "-->" << "Ingrese el puerto del servidor: ";
        std::cin >> this->port;
        this->isConnected = this->connectToServer();
    }

}

bool CLI::connectToServer() {

    try {

        const char *host = new char[this->ip.length() + 1];


        XmlRpcClient c(host, this->port);
        this->client = c;
        std::cout << "Conexión exitosa al servidor." << std::endl;
        return true;

    } catch (XmlRpcException& error) {
        std::cerr << RED << "Error al conectar al servidor: " << error.getMessage() << RESET << std::endl;
        return false;
    }


}