//
// Created by Usuario on 23/10/2023.
//

#include "Cliente.h"

void Cliente::connect() {

    try {

        XmlRpcClient c(this->IP.c_str(), this->PORT, nullptr);
        cout << "Conexion exitosa" << endl;

        XmlRpcValue noArgs, result;

        if(c.execute("system.listMethods", noArgs, result)) {

            cout << "\nResultado:\n " << result << "\n\n";

        }else{

            cout << "Error en la llamada a 'prueba'\n\n";

        }

    }catch (const XmlRpc::XmlRpcException& e) {

        cerr << "Error al conectar: " << e.getMessage() << endl;

    }


}

Cliente::Cliente(string IP, int PORT) {

    this->IP = IP;
    this->PORT = PORT;

    this->connect();

}