//
// Created by Usuario on 23/10/2023.
//

#include "CLI.h"

void CLI::loop() {

    string command;
    vector<string> command_segments;
    string segment;

    while(1){

        if(!isConnected){

            cout << "Sistema desconectado, ingrese /connect [IP] [PUERTO] para conectar, o /exit para cerrar el programa" << endl;
            cin >> command;
            istringstream stream(command);

            while(getline(stream, segment, ' ')){

                command_segments.push_back(segment);

            }

            if(command_segments.at(0) == "/exit"){

                cout << "Cerrando programa..." << endl;
                exit(EXIT_SUCCESS);

            }
            if(command_segments.at(0) == "/connect"){

                if(command_segments.size() == 3){

                    this->PORT = stoi(command_segments.at(2));
                    this->IP = stoi(command_segments.at(1))

                }else{

                    cout << "Error en la cantidad de argumentos." << endl

                }

            }else{

                cout << "Comando desconocido" << endl;

            }



        }else{



        }



    }



}

CLI::CLI(){

    this->loop();

}