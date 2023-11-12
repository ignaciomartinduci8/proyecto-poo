//
// Created by Usuario on 09/11/2023.
//

#include "CLI.h"

CLI::CLI() {

    std::cout << BLUE << "===============================================================\n" << RESET;
    std::cout << "Iniciando cliente de servicio RPC" << std::endl;
    std::cout << BLUE << "===============================================================\n" << RESET << std::endl;

    std::srand(std::time(0));
    this->ID = (std::rand() % 90000000 + 10000000);
    std::cout << BLUE << "-->" << RESET << " ID de cliente: " << this->ID << std::endl;

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
            std::cout << GREEN << "-->" << RESET << "  - Mensaje del servidor - \n" << result << std::endl;

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
void CLI::printMethods() {
    std::vector<std::string> tempMethods;
    int columns = 5;
    int w = 18;

    std::cout << BLUE << "============================ Metodos disponibles ============================\n" << RESET;

    for (int i = 0; i < this->methods.size(); i++) {
        tempMethods.push_back(this->methods[i]);

        if (tempMethods.size() == columns || i == this->methods.size() - 1) {
            for (int j = 0; j < tempMethods.size(); j++) {
                std::cout << BLUE << "|" << RESET << " " << std::setw(w) << tempMethods[j] << " ";
            }

            if (tempMethods.size() < columns) {
                std::cout << std::setw((columns - tempMethods.size()) * w) << " ";
            }

            std::cout << "\n";
            tempMethods.clear();
        }
    }

    std::cout << BLUE << "-->" << RESET << " Para desconectarse del servidor ingrese 'disconnect'" << std::endl;
    std::cout << BLUE << "============================================================================\n" << RESET;
}

void CLI::programLoop() {
    std::string command;

    while (this->isConnected) {

        this->printMethods();

        std::cout << BLUE << "-->" << RESET << " Ingrese un comando: ";

        std::getline(std::cin >> std::ws, command);

        this->commandController(command);

    }
}

void CLI::commandController(std::string command) {

    XmlRpcValue args, result;
    std::vector<std::string> segments;

    std::istringstream iss(command);
    std::string segment;

    while (iss >> segment) {
        segments.push_back(segment);
    }

    const char* XmlCommand = segments[0].c_str();

    for (int i = 1; i < segments.size(); i++) {
        args[i - 1] = segments[i].c_str();
    }

    if(segments[0] == "disconnect" || segments[0] == "userLeaves" || segments[0] == "connectSerial" || segments[0] == "disableEffector" || segments[0] == "disableMotors" || segments[0] == "disconnectSerial" || segments[0] == "enableEffector" || segments[0] == "enableMotors" || segments[0] == "goHome" || segments[0] == "setRobotMode" || segments[0] == "moveEffector" || segments[0] == "togglelearn") {

        args[segments.size() - 1] = this->ID;

    }

    if(command == "disconnect"){

        std::cout << GREEN << "-->" << RESET << " Desconectando del servidor..." << std::endl;
        this->client->execute("userLeaves", args, result);
        std::cout << GREEN << "-->" << RESET << "  - Mensaje del servidor - \n" << result << std::endl;
        this->isConnected = false;

        return;
    }

    if(segments[0] == "uploadAutomaticFile"){

            std::ifstream file(args[0]);
            std::string str;
            std::string fileContent;
            while (std::getline(file, str))
            {
                fileContent += str + "\r\n";
            }
            args[segments.size()] = fileContent.c_str();

            std::cout << "SE ENVIA EL ARCHIVO: " << args[0] << std::endl;
            std::cout << "CONTENIDO:" << args[1] << std::endl;

        }

    this->argsCheck(XmlCommand, args);

    std::cout << GREEN << "-->" << RESET << " Ejecutando servicio: " << segments[0] << std::endl;

    for (int i = 1; i < segments.size(); i++) {
        std::cout << GREEN << "-->" << RESET << " Argumento " << i << ": " << segments[i] << std::endl;
    }

    try{

        if (this->client->execute(XmlCommand, args, result)) {

            std::cout << GREEN << "-->" << RESET << " Resultado: " << std::endl;

            if (result.getType() == XmlRpcValue::TypeArray) {
                for (int i = 0; i < result.size(); i++) {

                    std::cout << GREEN << "-->" << RESET << " " << result[i] << std::endl;
                }
            } else {

                std::cout << GREEN << "-->" << RESET << " " << result << std::endl;
            }

        }
        else {

            std::cout << RED << "-->" << RESET << " Error 1 en la llamada a '" << segments[0] << "'" << std::endl;

        }

    }
    catch(XmlRpcException& e){

        std::cout << RED << "-->" << RESET << " Error 2 en la llamada a '" << segments[0] << "'" << std::endl;
        std::cout << RED << "-->" << RESET << " " << e.getMessage() << std::endl;

    }
    catch(const char* msg){

        std::cout << RED << "-->" << RESET << " Error 3 en la llamada a '" << segments[0] << "'" << std::endl;
        std::cout << RED << "-->" << RESET << " " << msg << std::endl;

    }
    catch(...){

        std::cout << RED << "-->" << RESET << " Error 4 en la llamada a '" << segments[0] << "'" << std::endl;

    }

}

bool CLI::argsCheck(const char *XmlCommand, XmlRpcValue args) {

    XmlRpcValue command, result;

    command[0] = XmlCommand;

    std::cout << RED << "CONTROL DE ARGUMENTOS" << RESET << std::endl;

    this->client->execute("system.methodSignature", command, result);

    std::cout << RED << "--> " << RESET << result <<  std::endl;

    std::cout << RED << "FIN CONTROL DE ARGUMENTOS" << RESET << std::endl;

}