//
// Created by Usuario on 09/11/2023.
//

#include "CLI.h"

CLI::CLI() {

    std::cout << BLUE << "===============================================================\n" << RESET;
    std::cout << "Iniciando cliente de servicio RPC" << std::endl;
    std::cout << BLUE << "===============================================================\n" << RESET << std::endl;

    this->waitUsername();
    this->waitConnection();

    this->programLoop();
}

void CLI::waitUsername() {

    std::cout << BLUE << "-->" << RESET << " Ingrese su nombre de usuario: ";
    std::cin >> this->username;

}

void CLI::waitConnection() {

    while(!this->isConnected) {

        std::cout << BLUE << "-->" << RESET << " Ingrese la IP del servidor: ";
        std::cin >> this->ip;
        std::cout << BLUE << "-->" << RESET << " Ingrese el puerto del servidor: ";
        std::cin >> this->port;
        this->isConnected = this->connectToServer();
    }

}

bool CLI::connectToServer() {

    try{

        XmlRpcClient* c = new XmlRpcClient(this->ip.c_str(), this->port, nullptr);
        this->client = c;

        XmlRpcValue noArgs, result;

        if (this->client->execute("system.listMethods", noArgs, result)){
            std::cout << GREEN << "-->" << RESET << " Conectado al servidor" << std::endl;

            for (int i = 0; i < result.size(); i++) {
                this->methods.push_back(std::string(result[i]));
            }

            XmlRpcValue oneArg;
            oneArg[0] = this->username;

            this->client->execute("setUsername", oneArg, result);
            std::cout << GREEN << "-->" << RESET << " Mensaje del servidor: " << result << std::endl;

            return true;
        }
        else {
            std::cerr << RED << "-->" << RESET << " No se pudo conectar al servidor" << std::endl;
            return false;
        }

    }
    catch(const char* msg){
        std::cerr << msg << std::endl;
        return false;
    }

}

void CLI::printMethods(){

    std::vector<std::string> tempMethods;
    int columns = 5;
    int w = 18;

    std::cout << BLUE << "============================ Metodos disponibles ============================\n" << RESET;

    for(int i = 0; i < this->methods.size(); i++){

        tempMethods.push_back(this->methods[i]);

        if(tempMethods.size() == columns){

            for(int j = 0; j < tempMethods.size(); j++){

                std::cout << BLUE << "|" << RESET << " " << std::setw(w) << tempMethods[j] << std::setw(w) << " ";

            }

            std::cout << std::endl;
            tempMethods.clear();

        }
        else if(i == this->methods.size() - 1){

            for(int j = 0; j < tempMethods.size(); j++){

                std::cout << BLUE << "|" << RESET << " " << std::setw(w) << tempMethods[j] << std::setw(w) << " ";

                if(tempMethods.size() == columns){
                    std::cout << std::endl;
                    std::cout << BLUE << "|" << RESET << " " << std::setw(w) << "disconnect" << " ";
                }else{
                    std::cout << BLUE << "|" << RESET << " " << std::setw(w) << "disconnect" << " ";
                }

            }
            std::cout << std::endl;
            tempMethods.clear();

        }
        else{

            continue;

        }


    }
    std::cout << BLUE << "============================================================================\n" << RESET;


}

void CLI::programLoop(){

    std::string command;


    while(this->isConnected){

        this->printMethods();

        std::cout << BLUE << "-->" << RESET << " Ingrese el nombre del metodo que desea ejecutar: ";
        std::cin >> command;

        this->commandController(command);

    }


}

void CLI::commandController(std::string command) {


    XmlRpcValue noArgs, result;

    this->client->execute("system.methodHelp", "enableEffector", result);

    std::cout << result << std::endl;

    for(int i = 0; i< this->methods.size(); i++){
        if(command == this->methods[i] or command == "disconnect"){

            break;

        }
        if(i == this->methods.size() - 1){

            std::cout << RED << "-->" << RESET << " El metodo ingresado no existe." << std::endl;
            return;

        }
    }

    const char* XmlCommand = command.c_str();

    if (command == "disconnect"){

        this->isConnected = false;
        std::cout << GREEN << "-->" << RESET << " Desconectado del servidor" << std::endl;

    }



}