//
// Created by Usuario on 23/10/2023.
//

#include "Servidor.h"

void Servidor::connect() {

    try {

        XmlRpcClient c(this->IP.c_str(), this->PORT, nullptr);
        cout << "Conexion exitosa" << endl;

        XmlRpcValue result;

        if(c.execute("system.prueba", 2, result)) {

            cout << "\nResultado:\n " << result << "\n\n";

        }else{

            cout << "Error en la llamada a 'prueba'\n\n";

        }

    }catch (const XmlRpc::XmlRpcException& e) {

        cerr << "Error al conectar: " << e.getMessage() << endl;

    }


}

Servidor::Servidor(string IP, int PORT) {

    this->IP = IP;
    this->PORT = PORT;

    this->connect();

}