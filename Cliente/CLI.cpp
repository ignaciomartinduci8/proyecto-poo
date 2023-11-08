//
// Created by Usuario on 23/10/2023.
//

#include "CLI.h"

#define RESET   "\033[0m"
#define RED     "\033[1;31m"
#define BLUE    "\033[1;34m"
#define IDENT   ">         "

void CLI::loop() {

    string command;
    vector <string> command_segments;
    string segment;
    vector<string> params;

    cout << endl;
    cout << BLUE << "============================================================================" << endl;
    cout << BLUE << "Iniciando cliente..." << endl;
    cout << BLUE << "============================================================================" << RESET << endl << endl;

    while (1) {

        command_segments.clear();

        if (!isConnected) {

            cout
                    << BLUE << "-->" << RESET << " Sistema desconectado, ingrese /connect [IP] [PUERTO] para conectar, o /exit para cerrar el programa"
                    << endl;
            getline(cin, command);
            istringstream stream(command);

            while (stream >> segment) {

                command_segments.push_back(segment);

            }

            if (command_segments.size() == 0) {

                continue;
            }

            if (command_segments.at(0) == "/exit") {

                cout << BLUE << "-->" << RESET <<" Cerrando programa..." << endl;
                exit(EXIT_SUCCESS);

            }

            if (command_segments.at(0) == "/connect") {

                try {

                    if (command_segments.size() == 3) {

                        cout << BLUE << "-->" << RESET << " Conectando a " << command_segments.at(1) << ":" << command_segments.at(2) << endl;
                        this->cliente = new Cliente(command_segments.at(1), stoi(command_segments.at(2)));
                        cout << BLUE << "-->" << RESET << " Conexion exitosa" << endl;
                        this->isConnected = true;


                    } else {

                        cerr << RED << "-->" << RESET << " Error: numero invalido de argumentos." << std::endl;

                    }

                }
                catch (const invalid_argument &e) {

                    cerr << RED << "-->" << RESET << " Error: argumento invalido. " << e.what() << endl;
                    throw;

                } catch (const out_of_range &e) {

                    cerr << RED << "-->" << " Error: fuera de rango. " << e.what() << endl;
                    throw;
                }

            } else {

                cerr << RED << "-->" << RESET <<" Error: Comando desconocido" << endl;

            }

            //cierre if de chequeo de conexion
        }

        else {


            cout << BLUE << "-->" << RESET << " Sistema conectado, esperando comandos. /help " << endl;
            cin >> command;

            if(command == "/help"){
                cout << BLUE << "-->" << RESET << " Comandos disponibles: " << endl;
                cout << BLUE << "-->" << RESET << " /listMethods: lista los metodos disponibles en el servidor" << endl;
                cout << BLUE << "-->" << RESET << " /execute [nombre del metodo] [parametros]: ejecuta el metodo con los parametros indicados" << endl;
                cout << BLUE << "-->" << RESET << " /disconnect: desconecta del servidor" << endl;
                cout << BLUE << "-->" << RESET << " /exit: cierra el programa" << endl;
            }

            command_segments.clear();
            params.clear();

            istringstream stream(command);

            while (stream >> segment) {

                command_segments.push_back(segment);

            }

            if(command == "/listMethods"){

                vector<string>methods =  this->cliente->getMethods();

                cout << BLUE << "-->" << RESET << " Metodos disponibles: " << endl;
                for (int i = 0; i < methods.size(); i++) {

                    cout << IDENT << methods[i] << endl;

                }

            }

            if(command_segments.size() == 0){

                continue;

            }

            if(command_segments[0] == "/disconnect"){

                this->isConnected = false;
                cout << BLUE << "-->" << RESET << " Desconectado del servidor" << endl;

            }

            if(command_segments[0] == "/exit"){

                cout << BLUE << "-->" << RESET << " Cerrando programa..." << endl;
                exit(EXIT_SUCCESS);

            }

            if(command_segments[0] == "/execute"){

                if (command_segments.size() > 2){

                    for (int i = 2; i < command_segments.size(); i++) {

                        params.push_back(command_segments[i]);

                    }

                }

                this->cliente->executeMethod(command_segments[1], params);

            }

        }
    }
}

CLI::CLI(){

    this->loop();

}