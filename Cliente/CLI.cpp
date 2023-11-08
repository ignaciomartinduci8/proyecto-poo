//
// Created by Usuario on 23/10/2023.
//

#include "CLI.h"

void CLI::loop() {

    string command;
    vector<string> command_segments;
    string segment;

    cout << endl;
    cout << "============================================================================" << endl;
    cout << "Iniciando cliente..."<<endl;
    cout << "============================================================================" << endl << endl;

    while(1){

        command_segments.clear();
        Cliente* cliente;

        if(!isConnected) {

            cout << "--> Sistema desconectado, ingrese /connect [IP] [PUERTO] para conectar, o /exit para cerrar el programa"<< endl;
            getline(cin, command);
            istringstream stream(command);

            while (stream >> segment) {

                command_segments.push_back(segment);

            }

            if(command_segments.size() == 0){

                continue;
            }

            if (command_segments.at(0) == "/exit") {

                cout << "--> Cerrando programa..." << endl;
                exit(EXIT_SUCCESS);

            }

            if (command_segments.at(0) == "/connect") {

                try {

                    if (command_segments.size() == 3) {

                        cliente = new Cliente(command_segments.at(1), stoi(command_segments.at(2)));
                        this->isConnected = true;


                    } else {

                        cout << "--> Error: numero invalido de argumentos." << std::endl;

                    }

                } catch (const invalid_argument &e) {

                    cout << "--> Error: argumento invalido. " << e.what() << endl;

                } catch (const out_of_range &e) {

                    cout << "--> Error: fuera de rango. " << e.what() << endl;
                }

            }
            else{

                cout << "--> Comando desconocido" << endl;

            }

        //cierre if de chequeo de conexion
        }
        else{


        }


    //cierre de while
    }
//cierre de método
}

CLI::CLI(){

    this->loop();

}